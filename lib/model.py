"""GANomaly
"""
# pylint: disable=C0301,E1101,W0622,C0103,R0902,R0915

##
from collections import OrderedDict
import os
import time
import numpy as np
from tqdm import tqdm
from torchvision.datasets import ImageFolder
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch.optim as optim
import torch.nn as nn
import torch.utils.data
import torchvision.utils as vutils

from lib.networks import NetG, NetD, weights_init
from lib.visualizer import Visualizer
from lib.loss import l2_loss
from lib.evaluate import evaluate
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig

class BaseModel():
    """ Base Model for ganomaly
    """
    def __init__(self, opt, dataloader):
        ##
        # Seed for deterministic behavior
        self.seed(opt.manualseed)

        # Initalize variables.
        self.opt = opt
        self.visualizer = Visualizer(opt)
        self.dataloader = dataloader
        self.trn_dir = os.path.join(self.opt.outf, self.opt.name, 'train')
        self.tst_dir = os.path.join(self.opt.outf, self.opt.name, 'test')
        self.device = torch.device("cuda:0" if self.opt.device != 'cpu' else "cpu")

    ##
    def set_input(self, input:torch.Tensor):
        """ Set input and ground truth

        Args:
            input (FloatTensor): Input data for batch i.
        """
        with torch.no_grad():
            self.input.resize_(input[0].size()).copy_(input[0])
            self.gt.resize_(input[1].size()).copy_(input[1])
            self.label.resize_(input[1].size())

            # Copy the first batch as the fixed input.
            if self.total_steps == self.opt.batchsize:
                self.fixed_input.resize_(input[0].size()).copy_(input[0])

    ##
    def seed(self, seed_value):
        """ Seed 
        
        Arguments:
            seed_value {int} -- [description]
        """
        # Check if seed is default value
        if seed_value == -1:
            return

        # Otherwise seed all functionality
        import random
        random.seed(seed_value)
        torch.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)
        np.random.seed(seed_value)
        torch.backends.cudnn.deterministic = True

    ##
    def get_errors(self):
        """ Get netD and netG errors.

        Returns:
            [OrderedDict]: Dictionary containing errors.
        """

        errors = OrderedDict([
            ('err_d', self.err_d.item()),
            ('err_g', self.err_g.item()),
            ('err_g_adv', self.err_g_adv.item()),
            ('err_g_con', self.err_g_con.item()),
            ('err_g_enc', self.err_g_enc.item())])

        return errors

    ##
    def get_current_images(self):
        """ Returns current images.

        Returns:
            [reals, fakes, fixed]
        """

        reals = self.input.data
        fakes = self.fake.data
        fixed = self.netg(self.fixed_input)[0].data

        return reals, fakes, fixed

    ##
    def save_weights(self, epoch):
        """Save netG and netD weights for the current epoch.

        Args:
            epoch ([int]): Current epoch number.
        """
        weight_dir = os.path.join(self.opt.outf, self.opt.name, 'train', 'weights')
        if not os.path.exists(weight_dir): os.makedirs(weight_dir)
        print(weight_dir)
        torch.save({'epoch': epoch + 1, 'state_dict': self.netg.state_dict()},
                   '%s/netG.pth' % (weight_dir))
        torch.save({'epoch': epoch + 1, 'state_dict': self.netd.state_dict()},
                   '%s/netD.pth' % (weight_dir))

    ##
    def train_one_epoch(self, epochNUM):
        """ Train the model for one epoch.
        """

        self.netg.train()
        epoch_iter = 0
        ii = 0
        num = len(self.dataloader['train'])
        for data in tqdm(self.dataloader['train'], leave=False, total=len(self.dataloader['train'])):
            self.opt.signalInfo.emit(10 + 0.8 * 85 * (epochNUM / self.opt.niter)*(ii/num),"")
            self.total_steps += self.opt.batchsize
            epoch_iter += self.opt.batchsize

            self.set_input(data)
            # self.optimize()
            self.optimize_params()

            if self.total_steps % self.opt.print_freq == 0:
                errors = self.get_errors()
                if self.opt.display:
                    counter_ratio = float(epoch_iter) / len(self.dataloader['train'].dataset)
                    self.visualizer.plot_current_errors(self.epoch, counter_ratio, errors)

            if self.total_steps % self.opt.save_image_freq == 0:
                reals, fakes, fixed = self.get_current_images()
                self.visualizer.save_current_images(self.epoch, reals, fakes, fixed)
                if self.opt.display:
                    self.visualizer.display_current_images(reals, fakes, fixed)
            ii += 1

        message = ">> Training model %s. Epoch %d/%d" % (self.name, self.epoch+1, self.opt.niter)
        print(message)
        #self.opt.showText.append(message+"\n");
        # self.visualizer.print_current_errors(self.epoch, errors)

    ##
    def train(self):
        """ Train the model
        """

        ##
        # TRAIN
        self.total_steps = 0
        best_auc = 0
        best_info = None

        # Train for niter epochs.
        print(">> Training model %s." % self.name)
        self.opt.signalInfo.emit(-1,">> Training model {}.".format(self.name))
        i = 0
        for self.epoch in range(self.opt.iter, self.opt.niter):
            # Train for one epoch
            self.opt.signalInfo.emit(-1,'正在进行第{}个epoch的训练....'.format(i + 1))
            num = self.train_one_epoch(i+1)
            i += 1
            # self.save_weights(self.epoch)
            self.opt.signalInfo.emit(10 + 0.8*85* (i / self.opt.niter),'第{}个epoch的训练完毕！\n正在对该epoch进行测试....'.format(i))
            res,info = self.test()
            if res['AUC'] > best_auc:
                best_auc = res['AUC']
                best_info = info
                self.save_weights(self.epoch)
            infoSTR = ""
            for key,value in info.items():
                infoSTR += str(key)+":"+str(value)+"\n"
            self.opt.signalInfo.emit(10 + 85* (i/ self.opt.niter), '测试完毕！\n第{}个epoch训练结果：\n{}'.format(i, infoSTR))
            # self.visualizer.print_current_performance(res, best_auc)
        print(">> Training model %s.[Done]" % self.name)
        self.opt.signalInfo.emit(-1,">> Training model {}.[Done]".format(self.name))
        # dict_info = {}
        # dict_info['minVal'] = 0.1
        # dict_info['maxVal'] = 0.8
        # dict_info['proline'] = 0.40
        # dict_info['auc'] = 0.93
        # dict_info['Avg Run Time (ms/batch)'] = 9
        # best_info = dict_info
        return best_info

    ##
    def test(self):
        """ Test GANomaly model.

        Args:
            dataloader ([type]): Dataloader for the test set

        Raises:
            IOError: Model weights not found.
        """

        with torch.no_grad():
            # Load the weights of netg and netd.
            if self.opt.load_weights:
                path = "./output/{}/{}/train/weights/netG.pth".format(self.name.lower(), self.opt.dataset)
                pretrained_dict = torch.load(path)['state_dict']

                try:
                    self.netg.load_state_dict(pretrained_dict)
                except IOError:
                    raise IOError("netG weights not found")
                print('   Loaded weights.')

            self.opt.phase = 'test'
            #self.opt.showProcess.setValue(80)
            # Create big error tensor for the test set.
            self.an_scores = torch.zeros(size=(len(self.dataloader['test'].dataset),), dtype=torch.float32, device=self.device)
            self.gt_labels = torch.zeros(size=(len(self.dataloader['test'].dataset),), dtype=torch.long,    device=self.device)
            self.latent_i  = torch.zeros(size=(len(self.dataloader['test'].dataset), self.opt.nz), dtype=torch.float32, device=self.device)
            self.latent_o  = torch.zeros(size=(len(self.dataloader['test'].dataset), self.opt.nz), dtype=torch.float32, device=self.device)

            # print("   Testing model %s." % self.name)
            self.times = []
            self.total_steps = 0
            epoch_iter = 0

            for i, data in enumerate(self.dataloader['test'], 0):
                self.total_steps += self.opt.batchsize
                epoch_iter += self.opt.batchsize
                time_i = time.time()
                self.set_input(data)
                self.fake, latent_i, latent_o = self.netg(self.input)

                error = torch.mean(torch.pow((latent_i-latent_o), 2), dim=1)
                time_o = time.time()

                self.an_scores[i*self.opt.batchsize : i*self.opt.batchsize+error.size(0)] = error.reshape(error.size(0))
                self.gt_labels[i*self.opt.batchsize : i*self.opt.batchsize+error.size(0)] = self.gt.reshape(error.size(0))
                self.latent_i [i*self.opt.batchsize : i*self.opt.batchsize+error.size(0), :] = latent_i.reshape(error.size(0), self.opt.nz)
                self.latent_o [i*self.opt.batchsize : i*self.opt.batchsize+error.size(0), :] = latent_o.reshape(error.size(0), self.opt.nz)

                self.times.append(time_o - time_i)

                # Save test images.
                if self.opt.save_test_images:
                    dst = os.path.join(self.opt.outf, self.opt.name, 'test', 'images')
                    if not os.path.isdir(dst):
                        os.makedirs(dst)
                    real, fake, _ = self.get_current_images()
                    vutils.save_image(real, '%s/real_%03d.eps' % (dst, i+1), normalize=True)
                    vutils.save_image(fake, '%s/fake_%03d.eps' % (dst, i+1), normalize=True)


            # Measure inference time.
            self.times = np.array(self.times)
            self.times = np.mean(self.times[:100] * 1000)

            # Scale error vector between [0, 1]
            print(torch.min(self.an_scores))
            print(torch.max(self.an_scores))
            maxNUM = torch.max(self.an_scores)
            minNUM = torch.min(self.an_scores)
            self.an_scores = (self.an_scores - torch.min(self.an_scores)) / (torch.max(self.an_scores) - torch.min(self.an_scores))
            # auc, eer = roc(self.gt_labels, self.an_scores)



            # -------------- 处理阈值 ------------------
            print('-------------- 处理阈值 ------------------')
            print(len(self.gt_labels))
            plt.ion()
            scores = {}
            ##plt.ion()
            # Create data frame for scores and labels.
            scores['scores'] = self.an_scores
            scores['labels'] = self.gt_labels
            hist = pd.DataFrame.from_dict(scores)
            #hist.to_csv("histogram.csv")

            # Filter normal and abnormal scores.
            abn_scr = hist.loc[hist.labels == 1]['scores']
            nrm_scr = hist.loc[hist.labels == 0]['scores']
            # Create figure and plot the distribution.
            ##fig, axes = plt.subplots(figsize=(4, 4))

            b = []
            c = []

            # for i in range(1000):
            #     b.append(nrm_scr[i])
            # for j in range(1000, 3011):
            #     c.append(abn_scr[j])
            print('asasddda')
            print(len(nrm_scr))
            print(len(abn_scr))

            for i in nrm_scr:
                b.append(i)

            for j in abn_scr:
                c.append(j)

            ##sns.distplot(nrm_scr, label=r'Normal Scores', color='r', bins=100, hist=True)

            ##sns.distplot(abn_scr, label=r'Abnormal Scores', color='b', bins=100, hist=True)

            nrm = np.zeros((50), dtype=np.int)
            minfix = 0.4
            abn = np.zeros((50), dtype=np.int)
            abmin = 30
            for k in np.arange(0, 1, 0.02):
                kint = int(k * 50)
                for j in range(len(nrm_scr)):
                    if b[j] >= k and b[j] < (k + 0.02):
                        nrm[kint] = nrm[kint] + 1
                for j in range(len(abn_scr)):
                    if c[j] >= k and c[j] < (k + 0.02):
                        abn[kint] = abn[kint] + 1
            print(nrm)
            print(abn)

            # startInd = 3
            # for k in range(0,20):
            #     if abs(nrm[k] - abn[k]) <= 3:
            #         continue
            #     else:
            #         startInd = k
            # max_dist = (len(nrm) + len(abn))*0.28
            # for k in range(startInd, 20):
            #     if abs(nrm[k] - abn[k]) < 5:
            #         #max_dist = abs(nrm[k] - abn[k])
            #         minfix = round((k / 20) + 0.02, 3)
            #         break

            # for k in range(3, 17):
            #     # print(nrm[k])
            #     # print(abn[k])
            #     # print('----')
            #     if abs(nrm[k]-abn[k]) > abmin and not (nrm[k] == 0 and abn[k] == 0):
            #         abmin = abs(nrm[k] - abn[k])
            #         minfix = round((k / 20) + 0.02, 3)
            max_dist = (len(nrm) + len(abn)) * 0.25
            for k in range(0,50):
                num1 = np.sum(nrm[0:k])
                num2 = np.sum(abn[k::])
                if (num1 + num2) >= max_dist:
                    minfix = round((k / 50) + 0.05, 3)
                    max_dist = num1+num2

            proline = minfix
            print(proline)

            print(self.gt_labels[0:20])
            print(self.an_scores[0:20])

            print('-------------  处理阈值 END --------------')
            # -------------  处理阈值 END --------------


            auc = evaluate(self.gt_labels, self.an_scores, metric=self.opt.metric)
            performance = OrderedDict([('Avg Run Time (ms/batch)', self.times), ('AUC', auc)])

            if self.opt.display_id > 0 and self.opt.phase == 'test':
                counter_ratio = float(epoch_iter) / len(self.dataloader['test'].dataset)
                self.visualizer.plot_performance(self.epoch, counter_ratio, performance)


            #  --- 写入文件 ---

            dict_info = {}
            dict_info['minVal'] = float(minNUM.item())
            dict_info['maxVal'] = float(maxNUM.item())
            dict_info['proline'] = float(proline)
            dict_info['auc'] = float(auc)
            dict_info['Avg Run Time (ms/batch)'] = float(self.times)

            #self.opt.showText.append(str(performance));
            #self.opt.showProcess.setValue(100)
            return performance, dict_info



    def FinalTest(self, minVal, maxVal,threshold=0.2):
        path = "./output/{}/{}/train/weights/netG.pth".format('ganomaly', self.opt.dataset)
        print('***'*10)
        print(path)
        print('***' * 10)
        pretrained_dict = torch.load(path)['state_dict']
        #self.opt.showText.append('Loading Weights...')
        self.opt.signalInfo.emit(-1, '加载权重...')
        try:
            self.netg.load_state_dict(pretrained_dict)
        except IOError:
            raise IOError("netG weights not found")
        print('   Loaded weights.')
        #self.opt.showText.append('LoadedWeights')
        self.opt.signalInfo.emit(5,"权重加载完毕！\n正在加载图片....")
        #self.opt.showText.append('正在加载图片...')
        path2 = self.opt.dataroot + '/final_test/'
        transform = transforms.Compose([transforms.Resize(self.opt.isize),
                                        transforms.CenterCrop(self.opt.isize),
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)), ])

        testdata = ImageFolder(os.path.join(path2), transform)

        #print(testdata)
        testdata2 = torch.utils.data.DataLoader(dataset=testdata,
                                                batch_size=1,
                                                shuffle=False,
                                                num_workers=int(self.opt.workers),
                                                drop_last=True)
        #print(testdata2)

        self.opt.signalInfo.emit(10, "图片加载完毕！\n正在进行检测....")
        testFilesName = os.listdir(self.opt.dataroot+'/final_test/0')
        testFilesRes = {}
        testFilesResNor = {}
        testFilesResAbn = {}

        for i, data2 in enumerate(testdata2, 0):
            self.set_input(data2)
            self.fake, latent_i, latent_o = self.netg(self.input)
            error = torch.mean(torch.pow((latent_i - latent_o), 2), dim=1)
            #print(error)
            testscore = (error - minVal) / (maxVal - minVal)
            testFilesRes[testFilesName[i]] = testscore.item()
            if testscore.item() >= threshold:
                testFilesResAbn[testFilesName[i]] = testscore.item()
            else:
                testFilesResNor[testFilesName[i]] = testscore.item()
            self.opt.signalInfo.emit(10+(i+1)/len(testFilesName)*88,"")
            #self.opt.showProcess.setValue()

        # print(testFilesRes)
        # print(testFilesResNor)
        # print(testFilesResAbn)
        self.opt.signalInfo.emit(100, "图片检测完毕!")
        #self.opt.signal.emit(len(testFilesResNor), len(testFilesResAbn))
        torch.cuda.empty_cache()



        return testFilesResNor,testFilesResAbn


##
class Ganomaly(BaseModel):
    """GANomaly Class
    """

    @property
    def name(self): return 'Ganomaly'

    def __init__(self, opt, dataloader):
        super(Ganomaly, self).__init__(opt, dataloader)

        # -- Misc attributes
        self.epoch = 0
        self.times = []
        self.total_steps = 0

        ##
        # Create and initialize networks.
        self.netg = NetG(self.opt).to(self.device)
        self.netd = NetD(self.opt).to(self.device)
        self.netg.apply(weights_init)
        self.netd.apply(weights_init)

        ##
        if self.opt.resume != '':
            print("\nLoading pre-trained networks.")
            self.opt.iter = torch.load(os.path.join(self.opt.resume, 'netG.pth'))['epoch']
            self.netg.load_state_dict(torch.load(os.path.join(self.opt.resume, 'netG.pth'))['state_dict'])
            self.netd.load_state_dict(torch.load(os.path.join(self.opt.resume, 'netD.pth'))['state_dict'])
            print("\tDone.\n")

        self.l_adv = l2_loss
        self.l_con = nn.L1Loss()
        self.l_enc = l2_loss
        self.l_bce = nn.BCELoss()

        ##
        # Initialize input tensors.
        self.input = torch.empty(size=(self.opt.batchsize, 3, self.opt.isize, self.opt.isize), dtype=torch.float32, device=self.device)
        self.label = torch.empty(size=(self.opt.batchsize,), dtype=torch.float32, device=self.device)
        self.gt    = torch.empty(size=(opt.batchsize,), dtype=torch.long, device=self.device)
        self.fixed_input = torch.empty(size=(self.opt.batchsize, 3, self.opt.isize, self.opt.isize), dtype=torch.float32, device=self.device)
        self.real_label = torch.ones (size=(self.opt.batchsize,), dtype=torch.float32, device=self.device)
        self.fake_label = torch.zeros(size=(self.opt.batchsize,), dtype=torch.float32, device=self.device)
        ##
        # Setup optimizer
        if self.opt.isTrain:
            self.netg.train()
            self.netd.train()
            self.optimizer_d = optim.Adam(self.netd.parameters(), lr=self.opt.lr, betas=(self.opt.beta1, 0.999))
            self.optimizer_g = optim.Adam(self.netg.parameters(), lr=self.opt.lr, betas=(self.opt.beta1, 0.999))

    ##
    def forward_g(self):
        """ Forward propagate through netG
        """
        self.fake, self.latent_i, self.latent_o = self.netg(self.input)

    ##
    def forward_d(self):
        """ Forward propagate through netD
        """
        self.pred_real, self.feat_real = self.netd(self.input)
        self.pred_fake, self.feat_fake = self.netd(self.fake.detach())

    ##
    def backward_g(self):
        """ Backpropagate through netG
        """
        self.err_g_adv = self.l_adv(self.feat_fake, self.feat_real)
        self.err_g_con = self.l_con(self.fake, self.input)
        self.err_g_enc = self.l_enc(self.latent_o, self.latent_i)
        self.err_g = self.err_g_adv * self.opt.w_adv + \
                     self.err_g_con * self.opt.w_con + \
                     self.err_g_enc * self.opt.w_enc
        self.err_g.backward(retain_graph=True)

    ##
    def backward_d(self):
        """ Backpropagate through netD
        """
        # Real - Fake Loss
        self.err_d_real = self.l_bce(self.pred_real, self.real_label)
        self.err_d_fake = self.l_bce(self.pred_fake, self.fake_label)

        # NetD Loss & Backward-Pass
        self.err_d = (self.err_d_real + self.err_d_fake) * 0.5
        self.err_d.backward()

    ##
    def reinit_d(self):
        """ Re-initialize the weights of netD
        """
        self.netd.apply(weights_init)
        print('   Reloading net d')

    def optimize_params(self):
        """ Forwardpass, Loss Computation and Backwardpass.
        """
        # Forward-pass
        self.forward_g()
        self.forward_d()

        # Backward-pass
        # netg
        self.optimizer_g.zero_grad()
        self.backward_g()
        self.optimizer_g.step()

        # netd
        self.optimizer_d.zero_grad()
        self.backward_d()
        self.optimizer_d.step()
        if self.err_d.item() < 1e-5: self.reinit_d()
