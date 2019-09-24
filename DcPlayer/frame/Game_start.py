import os
import sys
sys.path.append("..")
import GlobalConfig as gl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from model import net


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1386, 747)
        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(580, 160, 160, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        #设置按钮字体和大小
        font = QtGui.QFont()
        font.setFamily('宋体')
        font.setBold(True)
        font.setPointSize(25)
        font.setWeight(75)
        #开始游戏按钮
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        #self.pushButton_2.setStyleSheet('QPushButton{border-image:url(22.png)}')
        self.pushButton_2.setFont(font)

        self.verticalLayout.addWidget(self.pushButton_2)
        #退出按钮
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFont(font)
        self.verticalLayout.addWidget(self.pushButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.close)
        self.pushButton_2.clicked.connect(self.startGame)#点击触发开始有些事件

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "开始游戏"))
        self.pushButton.setText(_translate("MainWindow", "退出"))
    
    def startGame(self):
        use_gpu = False#设置是否使用GPU
        model , flag = net.load_model(use_gpu = use_gpu)#加载模型
        gl.GL_Model = model#将模型放在全局变量中





