# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\CZT\Desktop\Hi-Dancer\Test\StartDance.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import time
from MyTimer import *
from PyQt5.Qt import QUrl, QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from model import net
from core import tools
import myGlobal as gl
from Backend import *
import mxnet
import numpy as np
import threading
from DanceMatching import *


class Ui_Dialog(QtWidgets.QDialog):

    def __init__(self,parent=None):
        super().__init__(parent) #父类的构造函数
        self.model,flag = net.load_model(use_gpu=False)       #加载模型
        self.timer_camera = QtCore.QTimer() #定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture()       #视频流
        self.CAM_NUM = 0                    #为0时表示视频流来自笔记本内置摄像头
        self.danceMatching = DanceMatching()#实例化一个姿态检测类，也是线程类
        self.setupUi()
        self.slot_init()


    def setupUi(self):
        self.resize(1386,747)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.setFont(font)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(180, 670, 301, 41))
  
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(890, 670, 291, 41))

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(33, 21, 1301, 51))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        #摄像视频组件设定
        self.label_show_camera = QtWidgets.QLabel(self)   #定义显示视频的Label  
        self.label_show_camera.setGeometry(QtCore.QRect(20, 80, 670, 480))
        #视频播放组件设定
        self.video_widget = QVideoWidget(self)              # 1
        self.video_widget.setGeometry(700,80,670,480)
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.video_widget)       # 2
        self.player.setVolume(80)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle("Dialog")
        self.pushButton.setText( "开始")
        self.pushButton_2.setText("返回")
        self.label.setText("hello world!")

    '''初始化所有槽函数'''
    def slot_init(self):
        self.pushButton.clicked.connect(self.button_open_camera_clicked)    #若该按键被点击，则调用button_open_camera_clicked()
        self.timer_camera.timeout.connect(self.show_camera) #若定时器结束，则调用show_camera()
        #self.pushButton_2.clicked.connect(self.close)#若该按键被点击，则调用close()，注意这个close是父类QtWidgets.QWidget自带的，会关闭程序
        self.danceMatching.update_date.connect(self.change_label)
        self.danceMatching.now_to_getImages.connect(self.get_camera_images)


    '''槽函数之一'''
    def change_label(self,poseScore):
        '''
            通过传入的匹配得分，来修改label的显示
        '''
        showStr = '小脑有问题'
        if poseScore == 0:
            showStr = '小脑有问题'
        elif poseScore == 2:
            showStr = "再接再厉"
        elif poseScore == 4:
            showStr = '有点意思'
        elif poseScore == 6:
            showStr = "哎呦，不错哦！"
        elif poseScore == 8:
            showStr = '完美！！'
        elif poseScore == 10:
            showStr = '此舞只应天上有，人间哪得几回闻。'
        showStr = showStr + ' score + ' + str(poseScore)
        self.label.setText(showStr)

    def button_open_camera_clicked(self):
        '''
            打开摄像头，并同时播放视频，同时进行姿态检测
        '''
        if self.timer_camera.isActive() == False:   #若定时器未启动
            flag = self.cap.open(self.CAM_NUM) #参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:       #flag表示open()成不成功
                msg = QtWidgets.QMessageBox.warning(self,'warning',"请检查相机于电脑是否连接正确",buttons=QtWidgets.QMessageBox.Ok)
            else:
                self.pushButton.setText('关闭')
                self.timer_camera.start(30)  #定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                time.sleep(0.03)
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(gl.GL_VPath))) #设置视频资源
                self.player.play()#视频播放
                self.danceMatching.start()   #开始姿态检测
                
        else:
            self.timer_camera.stop()  #关闭定时器
            self.cap.release()        #释放视频流
            self.label_show_camera.clear()  #清空视频显示区域
            self.player.pause()       #视频暂停
            self.player.setPosition(0)  #设置播放进度为初始
            self.danceMatching.isEnd = True #设置线程需要被关闭，以达到关闭姿态匹配线程的目的
            self.pushButton.setText('开始')
        
       
 
    def show_camera(self):
        '''
            读取摄像头的一帧图片，并显示
        '''
        flag,self.image = self.cap.read()  #从视频流中读取
        show = cv2.resize(self.image,(640,480))     #把读到的帧的大小重新设置为 640x480
        show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB) #视频色彩转换回RGB，这样才是现实的颜色
        showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888) #把读取到的视频数据变成QImage形式
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))  #往显示视频的Label里 显示QImage
        
        
    def get_camera_images(self):
        '''
            截取摄像头图片，存入全局变量中
        '''
        reactTimer = MyTimer()
        waitTimer = MyTimer()
        reactTime = 0.5
        imageSize = (640,480)
        images = []
        reactTime = int(reactTime*1000)
        reactTimer.start(reactTime)
        waitTime = 100

        while reactTimer.isTimeOut() == False :
            waitTimer.start(waitTime)
            flag , image = self.cap.read()
            image = cv2.resize(image,imageSize)
            images.append(image)
            waitTimer.waitTimeOut()

        gl.GL_Images = images
        gl.GL_Images_Length = images.__len__()
        print("length={}".format(images.__len__()))



