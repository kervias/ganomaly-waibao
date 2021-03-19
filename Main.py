from GUI_MAIN import *
import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from multiprocessing import freeze_support
freeze_support()
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from myLib.kernel import Kernel
from PyQt5.QtWidgets import QMessageBox
import gc
import copy
#from win32com.shell import shell, shellcon
from shutil import rmtree

class Main(GUI_MainWindow):
    signal_startToTrain = pyqtSignal(dict)      # 信号：开始训练
    signal_startToTest = pyqtSignal(dict)       # 信号：开始测试
    signal_stopTrainOrTest = pyqtSignal()       # 信号: 停止训练或测试
    signal_trainFinished = pyqtSignal(dict)         # 信号：训练完成
    signal_transportINFO = pyqtSignal(int, str)     # 信号：传递信息
    signal_testFinished = pyqtSignal(dict,dict,dict)          # 信号：测试完成
    signal_requestUpdateModelData = pyqtSignal(dict,list,int)   #更新模型数据

    signal_refresh = pyqtSignal()

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.init_GUIData()
        self.init_customEvent()
        self.init_Data()
        self.label_img.setSignal(self.signal_refresh)
        self.resizeEvent(None)

    def init_GUIData(self):
        self.Widget_ModelTrain = None
        self.Widget_ModelTest = None
        self.Widget_ModelDisplay = None
        self.Widget_ProgressBar = None
        self.label_showNum.setText("安视有限责任公司")
        self.currImg = './Images/as1.png'
        # self.label_img.setStyleSheet("QLabel{background:white;}"
        #                          "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
        #                          )

        # jpg = QtGui.QPixmap(path+"/"+picList[1])#.scaled(self.label_img.size(),QtCore.Qt.KeepAspectRatio)#QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        # self.label_img.setPixmap(jpg)

        #
        # print(path)

        # self.listWidget_nor.setStyleSheet("QListWidget{border:1px solid gray; color:black; }"
        #                    "QListWidget::Item{padding-top:20px; padding-bottom:4px; }"
        #                    "QListWidget::Item:hover{background:skyblue; }"
        #                    "QListWidget::item:selected{background:lightgray; color:red; }"
        #                    "QListWidget::item:selected:!active{border-width:0px; background:lightgreen; }"
        #                    )
        # self.listWidget_nor.setStyleSheet("QListWidget{border:1px solid gray; color:black;}"
        #                                   "QListWidget::Item{border-radius:8px;padding-top:5px; padding-bottom:5px; }"
        #                                   "QListWidget::item:selected{background-color:#00be6e; }"
        #                                   )




    def init_Data(self):
        # 内核类实例：控制关键数据
        self.kernel = Kernel()

        # 暂存数据，主要用于界面的显示
        self.modelsData = self.kernel.get_modelData()
        self.testData = {}
        self.currInd_NOR = 0
        self.currInd_ABN = 0
        self.picList = {}
        self.currModelName = ''
        self.test_path = ''#'E:\\ProjectSet\\Pycharm\\WAIBAO\\Code01\\APP_GANomaly\\data\\cus_mnist\\final_test\\0'
        #self.listWidget_nor.addItem('1.jpg')
        self.img_nameList_nor = None
        self.img_nameList_abn = None


    def init_customEvent(self):
        # 菜单栏 Action 事件
        self.action_trainModel.triggered.connect(self.event_openWidget_ModelTrain)
        self.action_testPic.triggered.connect(self.event_openWidget_ModelTest)
        self.action_showModel.triggered.connect(self.event_openWidget_ModelDisplay)

        # 自定义信号事件
        self.signal_startToTrain.connect(self.slot_startToTrain)
        self.signal_startToTest.connect(self.slot_startToTest)
        self.signal_transportINFO.connect(self.slot_updateInfo)
        self.signal_testFinished.connect(self.slot_TestFinished)
        self.signal_trainFinished.connect(self.slot_TrainFinished)
        self.signal_requestUpdateModelData.connect(self.slot_updateModelData)
        self.signal_stopTrainOrTest.connect(self.slot_stopTrainOrTest)
        self.signal_refresh.connect(self.resizeEvent)

        # 基本事件
        self.listWidget_nor.currentItemChanged.connect(self.event_select_imgNOR)
        self.listWidget_abn.currentItemChanged.connect(self.event_select_imgABN)

        self.btn_modelInfo_1.released.connect(self.showTrainInfo)
        self.btn_testResult_1.released.connect(self.showTestInfo)



    def slot_startToTrain(self, params):
        # params['progressBar'] = self.Widget_ProgressBar.progressBar
        # params['showInfo'] = self.Widget_ProgressBar.textBrowser

        self.event_openWidget_ProgressBar('train')
        params['signalInfo'] = self.signal_transportINFO
        params['signal'] = self.signal_trainFinished
        if self.kernel.isTrain == False and self.kernel.isTest == False:
            self.kernel.isTrain = True
            self.Widget_ProgressBar.progressBar.setValue(0)
            self.Widget_ProgressBar.textBrowser.setText('')
            self.Widget_ProgressBar.show()
            self.kernel.startTrain(params)


    def slot_startToTest(self, params):
        self.event_openWidget_ProgressBar('test')
        params['signalInfo'] = self.signal_transportINFO
        params['signal'] = self.signal_testFinished
        if self.kernel.isTrain == False and self.kernel.isTest == False:
            self.kernel.isTest = True
            self.Widget_ProgressBar.progressBar.setValue(0)
            self.Widget_ProgressBar.textBrowser.setText('')
            self.Widget_ProgressBar.show()
            self.kernel.startTest(params)




    def slot_updateInfo(self, num, info): #更新进度条数据
        if num >= 0:
            self.Widget_ProgressBar.progressBar.setValue(num)
        if info != "":
            self.Widget_ProgressBar.textBrowser.append(info)


    def slot_TestFinished(self,resNor, resAbn, option):
        self.testData['nor'] = resNor
        self.testData['abn'] = resAbn
        self.kernel.set_testData(copy.deepcopy(self.testData))
        self.test_path = option['path'] + '/final_test/0'
        self.currModelName = option['modelName']


        # 加载每张图片
        self.img_nameList_nor = [i for i in self.testData['nor']]
        self.img_nameList_abn = [i for i in self.testData['abn']]
        # self.tabWidget.setCurrentIndex(0)
        # img = QtGui.QPixmap(self.test_path+img_nameList_nor[0])
        # self.label_img.setPixmap(img)

        # 加载ListItem数据
        self.listWidget_nor.clear()
        self.listWidget_abn.clear()
        ii = 0
        for i in self.img_nameList_nor:
            self.listWidget_nor.addItem(i)
            self.listWidget_nor.item(ii).setToolTip(str(self.testData['nor'][i]))
            geshi = i[-3::]
            self.listWidget_nor.item(ii).setIcon(QtGui.QIcon('./Images/imgs/'+geshi+'.png'))
            ii += 1
        ii = 0
        for i in self.img_nameList_abn:
            self.listWidget_abn.addItem(i)
            self.listWidget_abn.item(ii).setToolTip(str(self.testData['abn'][i]))
            geshi = i[-3::]
            self.listWidget_abn.item(ii).setIcon(QtGui.QIcon('./Images/imgs/' + geshi + '.png'))
            ii += 1

        self.kernel.isTested = True
        self.kernel.isTest = False
        # self.Widget_ProgressBar.close()
        # del self.Widget_ProgressBar
        # self.Widget_ProgressBar = None
        # gc.collect()

        self.Widget_ProgressBar.state = False

        self.Widget_ProgressBar.btn_stop.setText("完成")
        self.Widget_ProgressBar.close()



        QMessageBox.information(self, "消息", "所有图片均已检测完毕！\n"
                                            "其中检测为正常图片的有{}张, "
                                            "检测为异常图片的有{}张".format(str(len(resNor)), str(len(resAbn))))
        self.label_showNum.setText("null/"+str(len(resNor)))
        self.Widget_ProgressBar.exec()


    def slot_TrainFinished(self, resDict):
        self.modelsData[resDict['modelName']] = resDict
        self.kernel.set_OnemodelData(copy.deepcopy(resDict))
        self.kernel.isTrain = False
        self.Widget_ProgressBar.close()
        # del self.Widget_ProgressBar
        # gc.collect()
        # self.Widget_ProgressBar = None
        self.Widget_ProgressBar.state = False
        self.Widget_ProgressBar.btn_stop.setText("完成")
        self.Widget_ProgressBar.close()


        output = '模型{}已训练完毕！'.format(resDict['modelName'])
        QMessageBox.information(self, "消息", output, QMessageBox.Ok)
        self.Widget_ProgressBar.exec()


    def slot_updateModelData(self, newData, nameList, num):
        #对模型进行修改后的数据
        name = nameList[0]
        alterName = nameList[1]
        if self.kernel.isTest == True or self.kernel.isTrain == True:
            self.Widget_ModelDisplay.signal_isAllowed.emit(0, {})
        else:
            try:
                if num == 0: #修改
                    path = './output/ganomaly/' + name
                    path2 = './output/ganomaly/' + alterName
                    os.rename(path, path2)
                else: # 删除
                    path = './output/ganomaly/' + name
                    # res = shell.SHFileOperation((0, shellcon.FO_DELETE, path, None,
                    #                              shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,
                    #                              None,
                    #                              None))  # 删除文件到回收站

                    rmtree(path)
            except Exception as e:
                QMessageBox.warning(self, "错误", "未知错误{}".format(repr(e)), QMessageBox.Ok)


            self.modelsData = newData
            self.kernel.set_modelData(copy.deepcopy(newData))
            self.Widget_ModelDisplay.signal_isAllowed.emit(1, newData)



    def event_openWidget_ModelTrain(self):
        if self.kernel.isTrain == True:
            QMessageBox.warning(self, "警告", "当前正在训练，请训练完毕之后再进行训练", QMessageBox.Ok)
        elif self.kernel.isTest == True:
            QMessageBox.warning(self, "警告", "当前已经正在检测，请检测完毕之后再进行训练",  QMessageBox.Ok)
        else:
            self.Widget_ModelTrain = GUI_ModelTrain(signalList=[self.signal_startToTrain], modelInfo=copy.deepcopy(self.modelsData))
            self.Widget_ModelTrain.exec()

    def event_openWidget_ModelTest(self):
        if self.kernel.isTrain == True:
            QMessageBox.warning(self, "警告", "当前正在训练，请训练完毕之后再进行测试", QMessageBox.Ok)
        elif self.kernel.isTest == True:
            QMessageBox.warning(self, "警告", "当前已经正在检测，请检测完毕之后再进行测试",  QMessageBox.Ok)
        else:
            self.Widget_ModelTest = GUI_ModelTest(signalList=[self.signal_startToTest], modelInfo=copy.deepcopy(self.modelsData))
            self.Widget_ModelTest.exec()

    def event_openWidget_ModelDisplay(self):
        self.Widget_ModelDisplay = GUI_ModelDisplay(signalList=[self.signal_requestUpdateModelData], modelInfo=copy.deepcopy(self.modelsData))
        self.Widget_ModelDisplay.exec()

    def event_openWidget_ProgressBar(self, setting):
        if setting == 'train':
            info = ['训练进度']
            self.Widget_ProgressBar = GUI_ProgressBar(signalList=[self.signal_stopTrainOrTest],InfoList=info)
            self.Widget_ProgressBar.show()
        elif setting == 'test':
            info = ['检测进度']
            self.Widget_ProgressBar = GUI_ProgressBar(signalList=[self.signal_stopTrainOrTest],InfoList=info)
            self.Widget_ProgressBar.show()


    def event_select_imgNOR(self):
        item = self.listWidget_nor.currentItem()
        if item == None:
            return
        num = self.listWidget_nor.currentRow()

        name = item.text()
        img_path = self.test_path + '/' + name
        # img_data = QtGui.QPixmap(img_path)
        # self.label_img.setPixmap(img_data)
        self.currImg = img_path
        self.resizeEvent()
        self.label_showNum.setText(str(int(num) + 1)+"/"+str(len(self.testData['nor'])))


    def event_select_imgABN(self):
        item = self.listWidget_abn.currentItem()
        if item == None:
            return
        name = item.text()
        num = self.listWidget_abn.currentRow()

        img_path = self.test_path + '/' + name
        # img_data = QtGui.QPixmap(img_path)
        # self.label_img.setPixmap(img_data)
        self.currImg = img_path
        self.resizeEvent()
        self.label_showNum.setText(str(int(num) + 1) + "/" + str(len(self.testData['abn'])))

    def slot_stopTrainOrTest(self):
        if self.kernel.isTrain == True:
            self.kernel.kill_thread()
            self.kernel.isTrain = False
            self.Widget_ProgressBar.close()
            QMessageBox.information(self, "消息", "训练进程已终止",QMessageBox.Ok)
        elif self.kernel.isTest == True:
            self.kernel.kill_thread()
            self.kernel.isTest = False
            self.Widget_ProgressBar.close()
            QMessageBox.information(self, "消息", "检测进程已终止", QMessageBox.Ok)


    def showTestInfo(self): #显示检测信息
        if len(self.testData) != 0:
            info = "本次检测中，\n检测出正常图片{}张, \n异常图片{}张".format(str(len(self.testData['nor'])), str(len(self.testData['abn'])))
            QMessageBox.information(self, "检测信息", info, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "警告", "请先进行检测", QMessageBox.Ok)

    def showTrainInfo(self):
        if len(self.testData) != 0:
            name = self.currModelName
            myList = ['batchsize', 'niter', 'nz', 'workers']
            showinfp = '+ 本次检测采用的模型为:   {}\t\n+ 模型介绍：\n    {}\n+ 阈值：{}\n+ minVal：{}\n+ maxVal：{}\n+ auc：{}\n+ 训练参数：\n{}'.format(
                self.currModelName,self.modelsData[name]['desc'],
                str(self.modelsData[name]['proline']), str(self.modelsData[name]['minVal']),
                str(self.modelsData[name]['maxVal']), str(self.modelsData[name]['auc']),
                str('\n'.join(["    "+str(i) + ": " + str(j) for i, j in self.modelsData[name]['opt'].items() if i in myList])))
            QMessageBox.information(self, "模型信息", showinfp, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "警告", "请先进行检测", QMessageBox.Ok)


    def resizeEvent(self, event=None):
        # print(self.currImg)
        img = QtGui.QImage(self.currImg)
        width = img.width()
        height = img.height()
        per = (height+0.1) / (width+0.1)
        # print(per)
        # print(self.label_img.size())
        if per < 1:
            wid,hei = self.label_img.getWidth() * 0.87, per * self.label_img.getWidth() * 0.87
        else:
            per = 1/per
            wid,hei = self.label_img.getHeight() * 0.87 * per, self.label_img.getHeight() * 0.87

        jpg =  QtGui.QPixmap(self.currImg).scaled(wid,hei,QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        self.label_img.setPixmap(jpg)

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    # font = QtGui.QFont("仿宋", 9)
    # app.setFont(font)
    GAN = Main()
    GAN.show()
    sys.exit(app.exec_())

