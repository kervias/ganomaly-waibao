"""
TRAIN GANOMALY

. Example: Run the following command from the terminal.
    run train.py                             \
        --model ganomaly                        \
        --dataset UCSD_Anomaly_Dataset/UCSDped1 \
        --batchsize 32                          \
        --isize 256                         \
        --nz 512                                \
        --ngf 64                               \
        --ndf 64
"""


##
# LIBRARIES
from __future__ import print_function

from options import Options
from lib.data import load_data
from lib.model import Ganomaly

##
def train():
    """ Training
    """
    dataset = 'cus_mnist'
    dataroot = 'E:/ProjectSet/Pycharm/WAIBAO/Code01/GAN/data/cus_mnist'
    opt = Options().parse(dataset)

    opt.load_weights = False
    dataloader = load_data(opt)
    print(opt)

    # LOAD MODEL
    model = Ganomaly(opt, dataloader)
    model.train()


def test():
    """ Testing
    """
    dataset = 'cus_mnist'
    #dataroot = './data/cus_mnist'
    opt = Options().parse(dataset)
    opt.isTrain = False
    opt.load_weights = True

    ##
    # LOAD DATA
    dataloader = load_data(opt)
    print(opt)
    ##
    # LOAD MODEL
    model = Ganomaly(opt, dataloader)

    print(model.test())

def FinalTest():
    dataset = 'cus_mnist'
    # dataroot = './data/cus_mnist'
    opt = Options().parse(dataset)
    opt.isTrain = False
    opt.load_weights = True

    ##
    # LOAD DATA
    dataloader = load_data(opt)
    print(opt)
    ##
    # LOAD MODEL
    model = Ganomaly(opt, dataloader)
    ##
    # TRAIN MODEL
    # model.train()
    minVal = None
    maxVal = None
    threshold = None
    with open(opt.dataroot + '/performance.txt', 'r+', encoding='utf-8') as f:
        res = f.readline()
        res = res.split('&')
        res = [float(i) for i in res]
        minVal = res[0]
        maxVal = res[1]
        threshold = res[2]


    model.FinalTest(minVal, maxVal, threshold)





if __name__ == '__main__':
    train()
    #test()
    #FinalTest()

