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



class DanceMatching(QtCore.QThread):

    update_date = QtCore.pyqtSignal(int)
    now_to_getImages = QtCore.pyqtSignal()

    def __init__(self,parent=None):
        super(DanceMatching,self).__init__(parent)

    def run(self):
        #获取全局变量数据并更新全局数据
        self.info = gl.GL_VInfo
        self.model = gl.GL_Model
        self.isEnd = False
        gl.GL_TalScore = 0
        #清空全局队列
        while gl.GL_CurScoreQueue.empty() == False:
            gl.GL_CurScoreQueue.get()
 
        startTimer = MyTimer()
        startTimer.start(1000)          #开始计时
        temp = 0
        
        for oneInfo in self.info:
        
            timeid = oneInfo['timeid']  #演示视频播放时间ms
            reactime = float(oneInfo['reactime'])   #反应时间
            poseSocre = oneInfo['score']        #分数
            posepoints = oneInfo['posepoints']  #关节点信息
            posepoints = mxnet.nd.array(posepoints)  #类型转换
            temp += 1
            print('*************这是第{}次'.format(temp))
            print("timeid={}".format(timeid))
            startTimer.resetWaitTime(timeid)        #设置等待时间
            startTimer.waitTimeOut()                #等待时间，相当于 sleep

            self.now_to_getImages.emit()            #发送截取视频图像的信号

            #等待截取的图片存入全局变量
            while bool(gl.GL_Images == []) | bool(gl.GL_Images.__len__() < gl.GL_Images_Length):
                if self.isEnd == True:#当需要线程关闭时，退出
                    break
                time.sleep(0.02)
            if self.isEnd == True:#当需要线程关闭时，退出
                break

            images = gl.GL_Images#获取全局变量 (截取的图片list)
            #跟新全局变量数据
            gl.GL_Images = []
            gl.GL_Images_Length = 0

            use_gpu = False
            maxScore = 0
            score = 0
            
            #给每一个图片匹配示范骨架，获取最大分数
            for image in images:
                if self.isEnd == True:
                    break
                playerPre , playerImage = net.detection(self.model, image, use_gpu) #模型预测骨架
                if playerPre != None:
                    playerDis ,playerSkeleton = tools.normalization(playerPre['pred_coords'][0])#结果归一化
                    score = tools.matching(playerSkeleton, posepoints, use_gpu=use_gpu)#计算匹配结果
                if maxScore < score:
                    maxScore = score

            if self.isEnd == True:
                break
            print("mxScore={}".format(maxScore))

            #当分数超过10，认定匹配成功
            if maxScore > 10:
                #将分数更新在全局变量中
                gl.GL_CurScoreQueue.put(poseSocre)
                gl.GL_TalScore += poseSocre

                self.update_date.emit(poseSocre)#发送信号，传递动作得分
            else :
                self.update_date.emit(0)#发送信号，传递动作得分

        startTimer.end()
        