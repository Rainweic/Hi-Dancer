# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gundou.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import os
import sys
sys.path.append("..")
import Backend
import GlobalConfig as gl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon,QStandardItem,QStandardItemModel
from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget, QMainWindow, QDesktopWidget, QAction, qApp, QListView

class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):

        #设置按钮字体和大小
        font_tu = QtGui.QFont()
        font_tu.setFamily('宋体')
        font_tu.setBold(True)
        font_tu.setPointSize(115)
        font_tu.setWeight(100)

        font = QtGui.QFont()
        font.setFamily('宋体')
        font.setBold(True)
        font.setPointSize(25)
        font.setWeight(100)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1386, 747)

        #########菜单#########
        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu('菜单')
        #主界面
        self.main_menubar = QAction('主界面', self)
        self.file.addAction(self.main_menubar)
        #退出按钮
        self.quit_menubar = QAction(QIcon('close.ico'), '退出', self)
        self.quit_menubar.setShortcut('ctrl+q')
        self.quit_menubar.setStatusTip('这是退出')
        self.file.addAction(self.quit_menubar)
        self.quit_menubar.triggered.connect(qApp.quit)
        # 初始化状态栏
        self.statusBar()
        #将菜单添加进界面显示
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        #########################################

        self.scrollArea = QtWidgets.QScrollArea(MainWindow)
        self.scrollArea.setGeometry(QtCore.QRect(20, 30, 1300, 747))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 360, 250))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 360, 250))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        gLayout = QGridLayout(self.scrollAreaWidgetContents)
        
        path = '../poseinfo'                                       #目录地址
        self.allInfo,demoImages = Backend.getVideosInfo(path)      #获取视频信息
        
        #listView组件设置
        self.listView = QListView()
        self.listView.setViewMode(QListView.ListMode)
        self.listView.setIconSize(QtCore.QSize(300,200))
        self.listView.setGridSize(QtCore.QSize(700,250))
        self.listView.setMaximumHeight(1200)
        self.listView.setMinimumHeight(250)
        self.listView.setResizeMode(QListView.Adjust)
        self.listView.setFont(font)

        model = QStandardItemModel()
        # i = 0
        # 此处暂时无法获取实现显示icon
        # for img in demoImages:
        #     item = QStandardItem(QIcon(img),self.allInfo[i]['videopath'])
        #     model.appendRow(item)
        #     i+=1
        for info in self.allInfo:
            item = QStandardItem(info['videopath'])
            model.appendRow(item)

        self.listView.setModel(model)
        self.listView.clicked.connect(self.loadInfo2Global)#点击item,将选择item对应的视频信息存到全局变量中

        gLayout.addWidget(self.listView)#将listview 加入到layout中
        self.scrollAreaWidgetContents.setLayout(gLayout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def loadInfo2Global(self,index):
        #将选择item对应的视频信息存到全局变量中
        Backend.saveJson2Global(self.allInfo[index.row()]['videopath'],self.allInfo[index.row()]['info'])
       

    
