# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from __future__ import print_function
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(120, 170, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 300, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(310, 90, 391, 341))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "开始"))


from options import Options
from lib.data import load_data
from lib.model import Ganomaly

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from Dialog import Ui_Dialog
import time
import inspect
import ctypes
import threading


class MyTest(threading.Thread):
    def __init__(self, modelName, opt, dataloader):
        threading.Thread.__init__(self)
        self.path = opt.dataroot  # 测试文件夹路径
        self.modelName = modelName # 选择的模型名称
        self.resultNor = None # 测试结果（正常样本）
        self.resultAbn = None # 测试结果（异常样本
        self.isTested = False # 是否被测试
        self.opt = opt
        self.dataloader = dataloader
        self.desc = '' #测试结果描述

    def setPath(self, path):
        self.path = path

    def setModelName(self, name):
        self.modelName = name

    def startTest(self): #开始测试
        # LOAD MODEL
        if self.isTested == True:
            print('已经测试过了')
        else:
            self.run()

    def run(self):
        opt = self.opt

        # model.testOne()
        model = Ganomaly(self.opt, self.dataloader)
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

    def getResAll(self): #获取所有测试结果
        pass

    def getResNor(self): #获取测试结果中的正常样本
        pass

    def getResAbn(self): #获取测试结果中的异常样本
        pass

    def __str__(self):
        return '测试类'

class Main(QtWidgets.QMainWindow,Ui_MainWindow):
    Signal_TrainFinished = pyqtSignal()
    Signal_FinalTestFinished = pyqtSignal(int, int)
    Signal_stopFinalTest = pyqtSignal()


    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.progressBar.setValue(0.0)
        self.pushButton.clicked.connect(self.buttonClick)
        self.Signal_TrainFinished.connect(self.trainFinished)
        self.Signal_FinalTestFinished.connect(self.finalTestFinished)
        self.Dialog01 = Ui_Dialog(None,self.Signal_stopFinalTest)
        self.isTest = False
        self.th1 = None
        self.TESTCLASS = None
        self.Signal_stopFinalTest.connect(self.stopFinalTest)
        #self.Dialog01.show()


    def train(self):
        """ Training
        """
        self.textEdit.append('开始训练...')
        dataset = 'cus_mnist_2'
        # dataroot = './data/cus_mnist'
        dataroot = 'E:\ProjectSet\Pycharm\WAIBAO\cus_mnist2'
        opt = Options().parse(dataset,dataroot)
        opt.signal = self.Signal_TrainFinished
        opt.load_weights = False
        dataloader = load_data(opt)
        print(opt)

        # LOAD MODEL
        opt.showProcess = self.progressBar
        opt.showText = self.textEdit
        model = Ganomaly(opt, dataloader)
        model.train()

    def test(self):
        self.textEdit.append('开始测试，得出阈值...')

        """ Testing
        """
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
        opt.showProcess = self.progressBar
        opt.showText = self.textEdit
        model = Ganomaly(opt, dataloader)

        print(model.test())

    def buttonClick(self):
        print('****')
        if not self.isTest:
            self.Dialog01.show()
            #self.th1 = threading.Thread(target=Main.FinalTest, args=(self,))
            #self.th1.start()
            self.FinalTest()
            self.isTest = True

        print('//////')

    def FinalTest(self):
        self.Dialog01.textEdit.append('正在检测所有图片..')
        dataset = 'cus_mnist'
        dataroot = './data/cus_mnist'
        opt = Options().parse(dataset,dataroot)
        opt.isTrain = False
        opt.load_weights = True
        opt.signal = self.Signal_FinalTestFinished
        ##
        # LOAD DATA
        dataloader = load_data(opt)
        print(opt)
        ##
        # LOAD MODEL
        #opt.showProcess = self.progressBar
        #opt.showText = self.textEdit
        opt.showProcess = self.Dialog01.progressBar
        opt.showText = self.Dialog01.textEdit

        self.TESTCLASS = MyTest("测试模型", opt, dataloader)
        self.TESTCLASS.start()
        print('GOOD')





        # model = Ganomaly(opt, dataloader)
        # ##
        # # TRAIN MODEL
        # # model.train()
        # minVal = None
        # maxVal = None
        # threshold = None
        # with open(opt.dataroot + '/performance.txt', 'r+', encoding='utf-8') as f:
        #     res = f.readline()
        #     res = res.split('&')
        #     res = [float(i) for i in res]
        #     minVal = res[0]
        #     maxVal = res[1]
        #     threshold = res[2]
        #
        # model.FinalTest(minVal, maxVal, threshold)

    def stopFinalTest(self):
        if self.isTest:
            self.stop_thread(self.TESTCLASS)
            self.isTest = False
            print('已关闭进程')
            self.Dialog01.close()



    def btn_click_start_train(self): #开始训练模型
        pass


    def btn_click_start_test(self): #开始测试模型
        pass

    def trainFinished(self):
        print('训练完毕')


    def finalTestFinished(self, num_nor, num_abn):
        self.Dialog01.close()
        QMessageBox.information(self, "检测结果","本次共检测了{}张图片。\n其中判定正常图片有{}张, 判定为异常的图片有{}张。".format(num_abn+num_nor, num_nor, num_abn))


    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread1):
        self._async_raise(thread1.ident, SystemExit)

if __name__=="__main__":
    # import sys
    # app = QtWidgets.QApplication(sys.argv)
    # app.setStyle('fusion')
    # ui = Main()
    # ui.show()
    # sys.exit(app.exec_())

    # import json
    # aa = {"minVal": 0.09832322597503662, "maxVal": 0.8099011182785034, "proline": 0.215, "auc": 0.9081267302685068, "Avg Run Time (ms/batch)": 8.838369491252493, "opt": {"batchsize": 64, "workers": 8, "droplast": True, "isize": 32, "nc": 3, "nz": 100, "ngf": 64, "ndf": 64, "extralayers": 0, "device": "gpu", "gpu_ids": [0], "ngpu": 1, "name": "ganomaly/model", "model": "ganomaly", "display_server": "http://localhost", "display_port": 8097, "display_id": 0, "display": False, "outf": "./output", "manualseed": -1, "abnormal_class": "car", "proportion": 0.1, "metric": "roc", "print_freq": 100, "save_image_freq": 100, "save_test_images": False, "load_weights": False, "resume": "", "phase": "test", "iter": 0, "niter": 1, "beta1": 0.5, "lr": 0.0002, "w_adv": 1, "w_con": 50, "w_enc": 1, "isTrain": True}, "modelName": "model", "weightPath": "E:/ProjectSet/Pycharm/WAIBAO/Code01/APP_GANomaly/data/cus_mnist"}
    # bb = {"minVal": 0.09832322597503662, "maxVal": 0.8099011182785034, "proline": 0.215, "auc": 0.9081267302685068, "Avg Run Time (ms/batch)": 8.838369491252493, "opt": {"batchsize": 64, "workers": 8, "droplast": True, "isize": 32, "nc": 3, "nz": 100, "ngf": 64, "ndf": 64, "extralayers": 0, "device": "gpu", "gpu_ids": [0], "ngpu": 1, "name": "ganomaly/model", "model": "ganomaly", "display_server": "http://localhost", "display_port": 8097, "display_id": 0, "display": False, "outf": "./output", "manualseed": -1, "abnormal_class": "car", "proportion": 0.1, "metric": "roc", "print_freq": 100, "save_image_freq": 100, "save_test_images": False, "load_weights": False, "resume": "", "phase": "test", "iter": 0, "niter": 1, "beta1": 0.5, "lr": 0.0002, "w_adv": 1, "w_con": 50, "w_enc": 1, "isTrain": True}, "modelName": "mode1l", "weightPath": "E:/ProjectSet/Pycharm/WAIBAO/Code01/APP_GANomaly/data/cus_mnist"}
    # dic = {}
    # dic[aa['modelName']] = aa
    # dic[bb['modelName']] = bb
    # with open('./output/modelsData/null.json', 'w') as f:
    #     json.dump(dic,f,sort_keys=True,indent=2)
    # from win32com.shell import shell, shellcon
    # filename = './output/ganomaly/modelxx'
    # res = shell.SHFileOperation((0, shellcon.FO_DELETE, filename, None,
    #                              shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION, None,
    #                              None))  # 删除文件到回收站
    import re
    pattern = '.*.(bmp|jpg|png|tif|jpeg)'
    print(re.match(pattern, '1.bm\n2.txt\n2.jpg'))