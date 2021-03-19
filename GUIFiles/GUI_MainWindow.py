# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_MainWindow_V03.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(959, 737)
        MainWindow.setStyleSheet("\n"
"  \n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color:snow;\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget_nor = QtWidgets.QListWidget(self.tab)
        self.listWidget_nor.setStyleSheet("\n"
"QScrollBar:vertical\n"
"{\n"
"    width:8px;\n"
"    background:rgba(0,0,0,0%);\n"
"    margin:0px,0px,0px,0px;\n"
"    padding-top:9px;  \n"
"    padding-bottom:9px;\n"
"}\n"
"QScrollBar::handle:vertical\n"
"{\n"
"    width:8px;\n"
"    background:rgba(0,0,0,25%);\n"
"    border-radius:4px;  \n"
"    min-height:20;\n"
"}\n"
"QScrollBar::handle:vertical:hover\n"
"{\n"
"    width:8px;\n"
"    background:rgba(0,0,0,50%); \n"
"    border-radius:4px;\n"
"    min-height:20;\n"
"}\n"
"QScrollBar::add-line:vertical   \n"
"{\n"
"    height:9px;width:8px;\n"
"   \n"
"    subcontrol-position:bottom;\n"
"}\n"
"QScrollBar::sub-line:vertical   \n"
"{\n"
"    height:9px;width:8px;\n"
"   \n"
"    subcontrol-position:top;\n"
"}\n"
"QScrollBar::add-line:vertical:hover  \n"
"{\n"
"    height:9px;width:8px;\n"
"   \n"
"    subcontrol-position:bottom;\n"
"}\n"
"QScrollBar::sub-line:vertical:hover  \n"
"{\n"
"    height:9px;width:8px;\n"
"    border-image:url(:/images/a/2.png);\n"
"    subcontrol-position:top;\n"
"}\n"
"QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical   \n"
"{\n"
"    background:rgba(0,0,0,10%);\n"
"    border-radius:4px;\n"
"}")
        self.listWidget_nor.setObjectName("listWidget_nor")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_nor.addItem(item)
        self.verticalLayout_2.addWidget(self.listWidget_nor)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listWidget_abn = QtWidgets.QListWidget(self.tab_2)
        self.listWidget_abn.setStyleSheet("\n"
"QScrollBar:vertical\n"
"{\n"
"    width:8px;\n"
"    background:rgba(0,0,0,0%);\n"
"    margin:0px,0px,0px,0px;\n"
"    padding-top:9px;  \n"
"    padding-bottom:9px;\n"
"}\n"
"QScrollBar::handle:vertical\n"
"{\n"
"    width:8px;\n"
"    background:rgba(0,0,0,25%);\n"
"    border-radius:4px;  \n"
"    min-height:20;\n"
"}\n"
"QScrollBar::handle:vertical:hover\n"
"{\n"
"    width:8px;\n"
"    background:rgba(0,0,0,50%); \n"
"    border-radius:4px;\n"
"    min-height:20;\n"
"}\n"
"QScrollBar::add-line:vertical   \n"
"{\n"
"    height:9px;width:8px;\n"
"   \n"
"    subcontrol-position:bottom;\n"
"}\n"
"QScrollBar::sub-line:vertical   \n"
"{\n"
"    height:9px;width:8px;\n"
"   \n"
"    subcontrol-position:top;\n"
"}\n"
"QScrollBar::add-line:vertical:hover  \n"
"{\n"
"    height:9px;width:8px;\n"
"   \n"
"    subcontrol-position:bottom;\n"
"}\n"
"QScrollBar::sub-line:vertical:hover  \n"
"{\n"
"    height:9px;width:8px;\n"
"    border-image:url(:/images/a/2.png);\n"
"    subcontrol-position:top;\n"
"}\n"
"QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical   \n"
"{\n"
"    background:rgba(0,0,0,10%);\n"
"    border-radius:4px;\n"
"}")
        self.listWidget_abn.setObjectName("listWidget_abn")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_abn.addItem(item)
        self.verticalLayout_3.addWidget(self.listWidget_abn)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setStyleSheet("")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_modelInfo_1 = QtWidgets.QPushButton(self.frame_3)
        self.btn_modelInfo_1.setObjectName("btn_modelInfo_1")
        self.horizontalLayout_2.addWidget(self.btn_modelInfo_1)
        spacerItem1 = QtWidgets.QSpacerItem(63, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btn_testResult_1 = QtWidgets.QPushButton(self.frame_3)
        self.btn_testResult_1.setObjectName("btn_testResult_1")
        self.horizontalLayout_2.addWidget(self.btn_testResult_1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.frame_3)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color:snow;\n"
" background: -webkit-radial-gradient(center, circle, #f0f0f0, #74a9ad);\n"
"    background: -moz-radial-gradient(center, circle, #f0f0f0, #74a9ad);\n"
"    background: -ms-radial-gradient(center, circle, #f0f0f0, #74a9ad);\n"
"    background: -o-radial-gradient(center, circle, #f0f0f0, #74a9ad);\n"
"   \n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.frame)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 655, 611))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.label_img = MyLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_img.sizePolicy().hasHeightForWidth())
        self.label_img.setSizePolicy(sizePolicy)
        #self.label_img.setStyleSheet("box-shadow: 0 0 5px #000; ")
        self.label_img.setObjectName("label_img")
        self.gridLayout.addWidget(self.label_img, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.label_showNum = QtWidgets.QLabel(self.frame)
        self.label_showNum.setObjectName("label_showNum")
        self.horizontalLayout_3.addWidget(self.label_showNum)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame, 0, 1, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 27)
        self.gridLayout_3.setColumnStretch(1, 73)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 959, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_trainModel = QtWidgets.QAction(MainWindow)
        self.action_trainModel.setObjectName("action_trainModel")
        self.action_testPic = QtWidgets.QAction(MainWindow)
        self.action_testPic.setObjectName("action_testPic")
        self.action_showModel = QtWidgets.QAction(MainWindow)
        self.action_showModel.setObjectName("action_showModel")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.action_version = QtWidgets.QAction(MainWindow)
        self.action_version.setObjectName("action_version")
        self.action_help = QtWidgets.QAction(MainWindow)
        self.action_help.setObjectName("action_help")
        self.menu.addAction(self.action_trainModel)
        self.menu.addAction(self.action_testPic)
        self.menu.addAction(self.action_showModel)
        self.menu_2.addAction(self.action_help)
        self.menu_2.addAction(self.action_version)
        self.menu_2.addAction(self.action_about)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.listWidget_nor.isSortingEnabled()
        self.listWidget_nor.setSortingEnabled(False)
        item = self.listWidget_nor.item(0)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(1)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(2)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(3)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(4)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(5)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(6)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(7)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(8)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(9)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(10)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(11)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(12)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(13)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(14)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(15)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(16)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(17)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(18)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(19)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(20)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(21)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(22)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(23)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(24)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(25)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(26)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(27)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_nor.item(28)
        item.setText(_translate("MainWindow", "New Item"))
        self.listWidget_nor.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "正常图片"))
        __sortingEnabled = self.listWidget_abn.isSortingEnabled()
        self.listWidget_abn.setSortingEnabled(False)
        item = self.listWidget_abn.item(0)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(1)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(2)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(3)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(4)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(5)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(6)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(7)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(8)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(9)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(10)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(11)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(12)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(13)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(14)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(15)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(16)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(17)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(18)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(19)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(20)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(21)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(22)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(23)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(24)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(25)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_abn.item(26)
        item.setText(_translate("MainWindow", "New Item"))
        self.listWidget_abn.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "异常图片"))
        self.btn_modelInfo_1.setText(_translate("MainWindow", "训练模型"))
        self.btn_testResult_1.setText(_translate("MainWindow", "检测结果"))
        self.label_img.setText(_translate("MainWindow", "图片"))
        self.label_showNum.setText(_translate("MainWindow", "1/10"))
        self.menu.setTitle(_translate("MainWindow", "设置"))
        self.menu_2.setTitle(_translate("MainWindow", "帮助"))
        self.action_trainModel.setText(_translate("MainWindow", "训练模型"))
        self.action_testPic.setText(_translate("MainWindow", "测试图片"))
        self.action_showModel.setText(_translate("MainWindow", "查看模型"))
        self.action_about.setText(_translate("MainWindow", "关于"))
        self.action_version.setText(_translate("MainWindow", "版本信息"))
        self.action_help.setText(_translate("MainWindow", "操作帮助"))


class MyLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.myWidth = 780
        self.myHeight = 800


    def getWidth(self):
        return self.myWidth

    def getHeight(self):
        return self.myHeight

    def setSignal(self, signal):
        self.signal = signal


    def resizeEvent(self, event=None):
        self.myWidth = self.width()
        self.myHeight = self.height()
        self.signal.emit()
