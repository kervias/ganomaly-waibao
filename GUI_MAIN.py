from __future__ import print_function
import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

# --- GUI Import ---
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal

from GUIFiles.GUI_MainWindow import Ui_MainWindow as GUI_MainWindow_Pyuic
from GUIFiles.GUI_ModelDisplay import Ui_Form as GUI_ModelDisplay_Pyuic
from GUIFiles.GUI_ModelTrain import Ui_Form as GUI_ModelTrain_Pyuic
from GUIFiles.GUI_ModelTest import Ui_Form as GUI_ModelTest_Pyuic
from GUIFiles.GUI_Progress import Ui_Form as GUI_ProgressBar_Pyuic

import re
import copy


class GUI_MainWindow(QtWidgets.QMainWindow, GUI_MainWindow_Pyuic):
    def __init__(self, parent=None):
        super(GUI_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_customGUI()

    def init_customGUI(self):
        # 对界面进行修饰

        # img = QtGui.QImage("./Images/as1.png")
        # width = img.width()
        # height = img.height()
        # per = height/width
        #
        # print(self.width())
        # # self.label_img.setScaledContents(True)
        self.label_img.setAlignment(QtCore.Qt.AlignCenter)
        # # (self.label_img.width(),self.label_img.height())
        # jpg = QtGui.QPixmap("./Images/as1.png").scaled(500, per*500, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        # self.label_img.setPixmap(jpg)



        self.btn_modelInfo_1.setText("模型信息")
        self.setWindowTitle('安视')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Images/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.listWidget_nor.clear()
        self.listWidget_abn.clear()
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabIcon(0, QtGui.QIcon("./Images/nor.png"))
        self.tabWidget.setTabIcon(1, QtGui.QIcon("./Images/abn.png"))

        # self.setStyleSheet("#MainWindow{background-image:url(./Images/bg1.jpg);}")


        self.setStyleSheet(
            """
                QMenuBar{
                    background-color: rgb(230,235,245);
                }
                QMenuBar::item{
                    /*background-color: deepskyblue;*/
                    spacing:10px;
                    /* 条目内边框 */
                    /*padding:10px 20px;*/
                    
                    padding: 5px 7px;
                    /* 倒角 */
                    
                    
                    border-radius:4px;
                }
                
                
                QMenuBar::item::selected{
                    background-color: deepskyblue;
                }
                 QMenu::item{
                    
                 }
                 QMenu::item:selected { 
                     background-color:rgb(235,110,36);/*选中的样式*/
                     }
                     
                QMenu{
                    margin-top: 0px;
                }
                
            
                  
            """)


        # 给菜单朗添加图标
        self.action_trainModel.setIcon(QtGui.QIcon("./Images/train.png"))
        self.action_testPic.setIcon(QtGui.QIcon("./Images/test.png"))
        self.action_showModel.setIcon(QtGui.QIcon("./Images/show.png"))

        self.listWidget_nor.setStyleSheet(
            """
            
            QScrollBar:vertical
            {
                width:8px;
                background:rgba(0,0,0,0%);
                margin:0px,0px,0px,0px;
                padding-top:9px;  
                padding-bottom:9px;
            }
            QScrollBar::handle:vertical
            {
                width:8px;
                background:rgba(0,0,0,25%);
                border-radius:4px;  
                min-height:20;
            }
            QScrollBar::handle:vertical:hover
            {
                width:8px;
                background:rgba(0,0,0,50%); 
                border-radius:4px;
                min-height:20;
            }
            QScrollBar::add-line:vertical   
            {
                height:9px;width:8px;
               
                subcontrol-position:bottom;
            }
            QScrollBar::sub-line:vertical   
            {
                height:9px;width:8px;
               
                subcontrol-position:top;
            }
            QScrollBar::add-line:vertical:hover  
            {
                height:9px;width:8px;
               
                subcontrol-position:bottom;
            }
            QScrollBar::sub-line:vertical:hover  
            {
                height:9px;width:8px;
                border-image:url(:/images/a/2.png);
                subcontrol-position:top;
            }
            QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical   
            {
                background:rgba(0,0,0,10%);
                border-radius:4px;
            }
            """

        )

        self.listWidget_abn.setStyleSheet(
            """

            QScrollBar:vertical
            {
                width:8px;
                background:rgba(0,0,0,0%);
                margin:0px,0px,0px,0px;
                padding-top:9px;  
                padding-bottom:9px;
            }
            QScrollBar::handle:vertical
            {
                width:8px;
                background:rgba(0,0,0,25%);
                border-radius:4px;  
                min-height:20;
            }
            QScrollBar::handle:vertical:hover
            {
                width:8px;
                background:rgba(0,0,0,50%); 
                border-radius:4px;
                min-height:20;
            }
            QScrollBar::add-line:vertical   
            {
                height:9px;width:8px;

                subcontrol-position:bottom;
            }
            QScrollBar::sub-line:vertical   
            {
                height:9px;width:8px;

                subcontrol-position:top;
            }
            QScrollBar::add-line:vertical:hover  
            {
                height:9px;width:8px;

                subcontrol-position:bottom;
            }
            QScrollBar::sub-line:vertical:hover  
            {
                height:9px;width:8px;
                border-image:url(:/images/a/2.png);
                subcontrol-position:top;
            }
            QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical   
            {
                background:rgba(0,0,0,10%);
                border-radius:4px;
            }
            """

        )





class GUI_ModelTrain(QtWidgets.QDialog, GUI_ModelTrain_Pyuic):
    def __init__(self, parent=None, signalList=[], modelInfo={}):
        super(GUI_ModelTrain, self).__init__(parent)
        self.setupUi(self)
        self.signalList = signalList
        self.modelInfo = modelInfo
        self.init_customGUI()
        self.init_customEvents()
        self.init_defaultParams()


    def init_customGUI(self):
        # 对界面进行修饰
        pass

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Images/app.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)


        self.toolButton.setIcon(QtGui.QIcon("./Images/openFolder.png"))
        self.tabWidget.setTabIcon(0,QtGui.QIcon("./Images/setting1.png"))
        self.tabWidget.setTabIcon(1, QtGui.QIcon("./Images/setting2.png"))
        self.setStyleSheet(
            """
            QDialog{
                background-color: snow;
            }
             
            """
        )

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)



    def init_defaultParams(self):
        # 初始化默认参数
        num = len(self.modelInfo) + 1
        self.lineEdit_modelName.setText('model' + str(num))
        # self.textEdit_modelInfo.setToolTip('测试')
        self.lineEdit_1.setText('0.0002')
        self.lineEdit_2.setText('1')
        self.lineEdit_3.setText('100')
        self.lineEdit_4.setText('64')
        self.lineEdit_path.setText('')
        self.textEdit_modelInfo.setText('')
        self.tabWidget.setCurrentIndex(0)

    def init_customEvents(self):
        # 绑定相关事件
        self.btn_start.released.connect(self.event_emitSignalToTrain)
        self.btn_giveup.released.connect(self.event_cancelToTrain)
        self.toolButton.released.connect(self.event_openFolder)


    def event_emitSignalToTrain(self):
        ## 发送信号用于训练
        dict_params = {}
        # 1. 参数进行检查
        try:
            dict_params['-lr'] = float(self.lineEdit_1.text())
            dict_params['-batchsize'] = int(self.lineEdit_4.text())
            dict_params['-niter'] = int(self.lineEdit_2.text())
            dict_params['-nz'] = int(self.lineEdit_3.text())
            dict_params['name'] = self.lineEdit_modelName.text()
            dict_params['path'] = self.lineEdit_path.text()
            dict_params['info'] = self.textEdit_modelInfo.toPlainText()
        except Exception as e:
            QMessageBox.warning(self,"Error","参数设置错误：\n{}".format(repr(e)),QMessageBox.Ok)
            return

        # 未完待续...
        # 1. 模型名查重
        # 2. 路径的合法性
        # 3. 参数的合法性
        # 4. 发送信号
        # 1. 空值检查
        name = dict_params['name'].strip()
        info = dict_params['info'].strip()
        path1 = dict_params['path'].strip()
        if name == '':
            QMessageBox.warning(self, "警告", '名称不能为空', QMessageBox.Ok)
            return
        if info == '':
            QMessageBox.warning(self, "警告", '模型信息不能为空', QMessageBox.Ok)
            return
        if path1 == '':
            QMessageBox.warning(self, "警告", '路径不能为空', QMessageBox.Ok)
            return

        if not os.path.exists(path1):
            QMessageBox.warning(self, "警告", '该路径不存在', QMessageBox.Ok)
            return

        # 2. 重名检查
        nameList = [i for i in self.modelInfo]

        if name in nameList:
            QMessageBox.warning(self, "警告", "模型名不能与现有模型名重复", QMessageBox.Ok)
            return

        # 3. 命名合法性检查
        p = "^[^+-./><:\t\b@#$%*()\[\]][^/\t\b@><:#$%*()\[\]]{1,20}$"
        if not re.match(p, name):
            QMessageBox.warning(self, "警告", "模型名不合法或名称超出20字节限制", QMessageBox.Ok)
            return

        # 4. 路径合法性检查
        if(not self.isPathRight(dict_params['path'])):
            return


        self.signalList[0].emit(dict_params)
        self.close()
        # print(dict_params)

    def event_cancelToTrain(self):
        # 取消训练
        self.close()


    def event_openFolder(self):
        self.directory = QFileDialog.getExistingDirectory(self,"训练集文件夹","./")
        self.lineEdit_path.setText(self.directory)

    # 重写关闭窗口事件
    def closeEvent(self, QCloseEvent):
        # reply = QtWidgets.QMessageBox.question(self,
        #                                        '本程序',
        #                                        "是否要退出程序？",
        #                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        #                                        QtWidgets.QMessageBox.No)
        # if reply == QtWidgets.QMessageBox.Yes:
        #     event.accept()
        #     self.init_defaultParams()
        # else:
        #     event.ignore()

        self.init_defaultParams()


    def isPathRight(self, path): #检测路径合法性
        pathList = os.listdir(path)
        if 'train' not in pathList or 'test' not in pathList:
            QMessageBox.warning(self, "警告", "选择的路径应包含train和test文件夹",QMessageBox.Ok)
            return False

        pathList1 = os.listdir(path + '/train')
        pathList2 = os.listdir(path + '/test')

        if '0' not in pathList1 or '1' not in pathList2 or '0' not in pathList1:
            QMessageBox.warning(self, "警告", "子目录train文件夹中应包含0文件夹且子目录test文件夹中应包含0和1文件夹", QMessageBox.Ok)
            return False


        pathList = os.listdir(path + '/train/0')
        path1 =  '@'.join(pathList)

        flag = False
        if '.jpg' in path1 or '.png' in path1 or '.jpeg' in path1 or '.tif' in path1 or '.bmp' in path1:
            flag = True

        if flag == False:
            QMessageBox.warning(self, '警告', "指定目录中没有图片文件: ./train/0", QMessageBox.Ok)
            return False

        flag = False
        pathList = os.listdir(path + '/test/0')
        path1 = '@'.join(pathList)
        if '.jpg' in path1 or '.png' in path1 or '.jpeg' in path1 or '.tif' in path1 or '.bmp' in path1:
            flag = True
        if flag == False:
            QMessageBox.warning(self, '警告', "指定目录中没有图片文件：./test/0", QMessageBox.Ok)
            return False

        flag = False
        pathList = os.listdir(path + '/test/1')
        path1 = '@'.join(pathList)
        if '.jpg' in path1 or '.png' in path1 or '.jpeg' in path1 or '.tif' in path1 or '.bmp' in path1:
            flag = True

        if flag == False:
            QMessageBox.warning(self, '警告', "指定目录中没有图片文件：./test/1", QMessageBox.Ok)
            return False


        return True





class GUI_ModelTest(QtWidgets.QDialog, GUI_ModelTest_Pyuic):
    def __init__(self, parent=None,signalList=[], modelInfo={}):
        super(GUI_ModelTest, self).__init__(parent)
        self.setupUi(self)
        self.signalList = signalList
        self.modelInfo = modelInfo
        self.init_customGUI()
        self.modelInfo = modelInfo
        self.init_customEvents()
        self.init_defaultParams()


        #self.modelNameList = []


    def init_customGUI(self):
        # 对界面进行修饰
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Images/app.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.toolButton.setIcon(QtGui.QIcon("./Images/openFolder2.png"))
        # self.comboBox.setStyleSheet()

        self.setStyleSheet(
            """
            QDialog{
                background-color: snow;
            }
            """
        )

    def init_defaultParams(self):
        self.lineEdit_path.setText('')
        try:
            self.comboBox.currentIndexChanged.disconnect(self.event_selectModel)
            self.comboBox.clear()
            #self.modelNameList = []
            self.comboBox.addItem("--请选择--")
            self.textBrowser.setText('')
            if (len(self.modelInfo) != 0):
                for item_name,item_info in self.modelInfo.items():
                    self.comboBox.addItem(item_name)
                #self.modelNameList.append(item_name)
            self.comboBox.currentIndexChanged.connect(self.event_selectModel)
            self.comboBox.setCurrentIndex(0)
        except Exception as e:
            print(e)

    def init_customEvents(self):
        self.btn_start.released.connect(self.event_emitSignalToTest)
        self.comboBox.currentIndexChanged.connect(self.event_selectModel)
        self.btn_giveup.released.connect(self.event_cancelToTest)
        self.toolButton.released.connect(self.event_openFolder)

    def event_selectModel(self):
        name = self.comboBox.currentText()
        if name != '--请选择--':
            self.textBrowser.setText(self.modelInfo[name]['desc'])
        else:
            self.textBrowser.setText('')

    def event_emitSignalToTest(self):
        pass
        # 1. 检测路径合法性包括不能为空等
        # 2. 检测模型选择正确
        # 3. 发送信号给主程序

        path = self.lineEdit_path.text().strip()
        modelName = self.comboBox.currentText()

        dict_params = {}
        if path == '':
            QMessageBox.warning(self, "警告", "路径不能为空", QMessageBox.Ok)
            return

        if modelName == '--请选择--':
            QMessageBox.warning(self,"警告", "请选择一个模型", QMessageBox.Ok)
            return


        dict_params['path'] = path
        dict_params['modelName'] = modelName

        path1 = path
        if not os.path.exists(path1):
            QMessageBox.warning(self, "警告", '该路径不存在', QMessageBox.Ok)
            return

        if (not self.isPathRight(path1)):
            return

        self.signalList[0].emit(dict_params)
        self.close()
        #print(dict_params)


    def event_cancelToTest(self):
        self.close()

    def event_openFolder(self):
        directory = QFileDialog.getExistingDirectory(self, "检测图片文件夹", "./")
        self.lineEdit_path.setText(directory)

    def isPathRight(self, path):
        pathList = os.listdir(path)

        if not os.path.exists(path + '/final_test/0'):
            QMessageBox.warning(self, '警告', "指定目录中没有文件夹：./final_test/0", QMessageBox.Ok)
            return False

        pathList = os.listdir(path + '/final_test/0')
        path1 = '@'.join(pathList)

        flag = False
        if '.jpg' in path1 or '.png' in path1 or '.jpeg' in path1 or '.tif' in path1 or '.bmp' in path1:
            flag = True

        if flag == False:
            QMessageBox.warning(self, '警告', "指定目录中没有图片文件: ./final_test/0", QMessageBox.Ok)
            return False

        return True

    def closeEvent(self, QCloseEvent):
        self.init_defaultParams()



class GUI_ModelDisplay(QtWidgets.QDialog, GUI_ModelDisplay_Pyuic):
    signal_isAllowed = pyqtSignal(int,dict)

    def __init__(self, parent=None, signalList=[], modelInfo={}):
        super(GUI_ModelDisplay, self).__init__(parent)
        self.setupUi(self)

        self.init_customGUI()
        self.signalList = signalList
        self.modelInfo = modelInfo
        # self.modelInfo = {
        #     'model01': {'name': 'model01', 'info': 'mnist数据集', 'path': 'C:/ssd', 'trainInfo':'阈值'},
        #     'model02': {'name': 'model02', 'info': '自定义mnist数据集', 'path': 'C:/ssd2', 'trainInfo':'阈e32值'},
        #     'model03': {'name': 'model03', 'info': '自定义mnist数据集xxx', 'path': 'C:/ssd2', 'trainInfo': '阈dq值'},
        #     '模型': {'name': '模型', 'info': '自定义mnist数据集の', 'path': 'C:/ssd2', 'trainInfo': 'の2阈值'}
        # }

        self.init_customEvents()
        self.init_defaultParams()

    def init_customGUI(self):
        # 对界面进行修饰
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Images/app.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setStyleSheet(
            """
            QDialog{
                background-color: snow;
            }
            QListWidget::item::selected{
                background-color: deepskyblue;
            }
            """
        )

        self.toolButton.setStyleSheet(
            """
            border: 0px solid;
            """
        )
        self.toolButton.setIcon(QtGui.QIcon("./Images/search.png"))

    def init_customEvents(self):
        self.listWidget.currentItemChanged.connect(self.event_selectModel)
        self.btn_enter.released.connect(self.event_alterModel)
        self.lineEdit_search.textChanged.connect(self.event_search)
        self.btn_delete.released.connect(self.event_deleteModel)
        self.signal_isAllowed.connect(self.slot_allowUpdate)


    def init_defaultParams(self):
        self.listWidget.currentItemChanged.disconnect(self.event_selectModel)
        self.listWidget.clear()
        self.lineEdit_modelName.setText('')
        self.textEdit_modelInfo.setText('')
        self.textBrowser_trainInfo.setText('')
        if len(self.modelInfo) != 0:
            ii = 0
            for key in sorted(self.modelInfo):
                self.listWidget.addItem(key)
                self.listWidget.item(ii).setIcon(QtGui.QIcon('./Images/model.png'))
                ii +=1

        self.listWidget.currentItemChanged.connect(self.event_selectModel)



    def event_selectModel(self):
        item = self.listWidget.currentItem()
        name = item.text()
        self.lineEdit_modelName.setText(name)
        self.textEdit_modelInfo.setText(self.modelInfo[name]['desc'])
        showinfp = '>>阈值：{}\n>>minVal：{}\n>>maxVal：{}\n>>auc：{}\n>>训练参数：\n{}'.format(
            str(self.modelInfo[name]['proline']),str(self.modelInfo[name]['minVal']),
                                                     str(self.modelInfo[name]['maxVal']),str(self.modelInfo[name]['auc']),str('\n'.join([str(i)+":"+str(j) for i,j in self.modelInfo[name]['opt'].items()])))

        self.textBrowser_trainInfo.setText(showinfp)


    def event_alterModel(self):
        item = self.listWidget.currentItem()
        if item == None:
            QMessageBox.warning(self, "警告", "请选择一个模型", QMessageBox.Ok)
            return
        name = item.text()
        alterName = self.lineEdit_modelName.text().strip()
        alterInfo = self.textEdit_modelInfo.toPlainText().strip()
        # 1. 空值检查
        if alterName == '':
            QMessageBox.warning(self, "警告", '名称不能为空',QMessageBox.Ok)
            return
        if alterInfo == '':
            QMessageBox.warning(self, "警告", '模型信息不能为空',QMessageBox.Ok)
            return

        # 2. 重名检查
        nameList = [i for i in self.modelInfo]

        if alterName in nameList and alterName != name :
            QMessageBox.warning(self, "警告", "模型名不能与现有模型名重复", QMessageBox.Ok)
            return

        # 3. 命名合法性检查
        p = "^[^+-./><:\t\b@#$%*()\[\]][^/\t\b@><:#$%*()\[\]]{1,20}$"
        if not re.match(p, alterName):
            QMessageBox.warning(self, "警告", "模型名不合法或名称超出20字节限制", QMessageBox.Ok)
            return

        copy_info = copy.deepcopy(self.modelInfo)
        copy_info[alterName] = copy_info.pop(name)
        copy_info[alterName]['desc'] = alterInfo
        copy_info[alterName]['modelName'] = alterName

        self.signalList[0].emit(copy_info,[name,alterName],0)




    def event_deleteModel(self):
        item = self.listWidget.currentItem()
        if item == None:
            QMessageBox.warning(self, "警告", "请选择一个模型", QMessageBox.Ok)
            return

        reply = QMessageBox.question(self, "警告", "你确定要删除当前模型吗？",QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.No:
            return

        name = item.text()

        copy_info = copy.deepcopy(self.modelInfo)
        copy_info.pop(name)

        self.signalList[0].emit(copy_info,[name,""],1)
        self.init_defaultParams()



    def event_search(self):
        search_content = self.lineEdit_search.text()
        if search_content.strip() == "":
            search_content = ''
        print(search_content)
        self.listWidget.currentItemChanged.disconnect(self.event_selectModel)
        self.listWidget.clear()
        self.lineEdit_modelName.setText('')
        self.textEdit_modelInfo.setText('')
        self.textBrowser_trainInfo.setText('')
        if len(self.modelInfo) != 0:
            ii = 0
            for key in sorted(self.modelInfo):
                if search_content in key:
                    self.listWidget.addItem(key)
                    self.listWidget.item(ii).setIcon(QtGui.QIcon('./Images/model.png'))
                    ii += 1

        self.listWidget.currentItemChanged.connect(self.event_selectModel)


    def slot_allowUpdate(self, num, dic):
        if num == 0:
            QMessageBox.warning(self, "警告", "正在检测，暂不允许修改和删除模型", QMessageBox.Ok)
        else:
            self.modelInfo = dic
        self.init_defaultParams()

    def closeEvent(self, QCloseEvent):
        self.init_defaultParams()






class GUI_ProgressBar(QtWidgets.QDialog, GUI_ProgressBar_Pyuic):
    def __init__(self, parent=None,signalList=[],InfoList=[]):
        super(GUI_ProgressBar, self).__init__(parent)
        self.setupUi(self)
        self.init_customGUI()
        self.infoList = InfoList
        self.signalList = signalList
        self.state = True


    def init_customGUI(self):
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # 对界面进行修饰
        # print('ded32')
        # self.setWindowTitle(self.infoList[0])
        # print('dewh809fgywe9')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Images/app.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.btn_stop.released.connect(self.event_stop)



    def event_stop(self):
        if self.state == True:
            self.signalList[0].emit()
        else:
            self.close()






