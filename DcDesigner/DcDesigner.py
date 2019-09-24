# 该类继承DcDesigner_UI.py
# UI 设置均在父类中
# 本类实现界面的逻辑功能

import os
import sys
import json
import shutil
import cv2 as cv
import PyQt5 as Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import  *
from frame.DcDesigner_UI import Ui_MainWindow
from model import net
from core import tools

class DcDesigner(QMainWindow, Ui_MainWindow):

    SAVE_PATH = "../poseinfo"

    def __init__(self):
        super(DcDesigner, self).__init__()
        self.play = False
        self.isFirst = True
        self.videoLength = 0.1
        self.videoCapTure = None
        self.saveAction = SaveAction(self)
        # 初始化UI
        self.setupUi(self)
        self.menuBar.setNativeMenuBar(False)
        self.showCenter()
        self.load_model()
        # 播放器
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.videoWidget)
        # 槽绑定
        self.chooseVideo.triggered.connect(self.chooseVideoFile)
        self.playOrStop.clicked.connect(self.playAndStop)
        self.player.positionChanged.connect(self.setSlide)
        self.horizontalSlider.sliderReleased.connect(self.changePosition)
        self.addAction.clicked.connect(self.saveAction.start)

    def load_model(self):
        '''
        加载模型 并弹出提示 
        '''
        QMessageBox.information(self, "提示", "模型即将加载,请等待...初次使用软件会自动后台下载模型...")
        self.model, flag = net.load_model(use_gpu=False)

    def showCenter(self):  
        '''
        将主程序显示于屏幕中心
        '''  
        desktopGeometry = QApplication.desktop()
        mainWindowWidth = desktopGeometry.width()
        mainWindowHeight = desktopGeometry.height()

        rect = self.geometry()
        windowWidth = rect.width()
        windowHeight = rect.height()

        x = (mainWindowWidth - windowWidth) / 2
        y = (mainWindowHeight - windowHeight) / 2

        self.move(x, y)

    def chooseVideoFile(self):
        videoPathQT = QFileDialog.getOpenFileUrl()[0]
        print("*****************************")
        print(videoPathQT)
        self.videoPath = str(videoPathQT)[27:-2]    # 这个地方有毒 ubuntu是26 Window是27...
        print(self.videoPath)
        print(QMediaContent(videoPathQT))
        self.player.setMedia(QMediaContent(videoPathQT))
        self.videoCapTure = cv.VideoCapture(self.videoPath)
        self.isFirst = True
        self.poseInfo = {"videopath": os.path.join(self.SAVE_PATH, "video", os.path.basename(self.videoPath))}   # 存放整个视频动作信息
        self.info = []  # 存放每张图片动作信息
        
    def playAndStop(self):
        if not self.play:
            # 开始播放import net
            self.playOrStop.setText("暂停")
            self.play = True
            self.player.play()
            # 设置进度条长度
            self.videoLength = self.player.duration()
        else:
            # 暂停
            self.playOrStop.setText("播放")
            self.play = False
            self.player.pause()

    def setSlide(self):
        '''
        播放进度与进度条绑定
        '''
        self.horizontalSlider.setMaximum(self.videoLength)
        self.horizontalSlider.setValue(self.player.position())
        self.frameID.setText(str(self.player.position()))

    def changePosition(self):
        '''
        进度条改变视频位置改变
        '''
        self.player.setPosition(self.horizontalSlider.value())

    def moveVideo(self, oldPath, newPath="../poseinfo/video"):
        '''
        将视频文件搬运到指定位置： ../poseinfo/video
        '''
        if not os.path.exists(newPath):
            os.mkdir(newPath)

        shutil.copy(oldPath, newPath)

        
class SaveAction(QThread):
    def __init__(self, widget):
        super(SaveAction, self).__init__()
        self.widget = widget

    def run(self):
        self.saveAction()

    def saveAction(self):
        '''
        保存当前帧拥有的动作骨架
        '''
        self.playPause()
        if self.widget.videoCapTure == None or self.widget.videoPath == None:
            QMessageBox.warning(self.widget, "警告！", "请选择视频文件！")
            return None

        self.widget.videoCapTure.set(cv.CAP_PROP_POS_MSEC, int(self.widget.player.position()))    # 通过ms进行定位
        ret, frame = self.widget.videoCapTure.read()   # 获取帧 

        # 骨架信息预测
        pred, img = net.detection(self.widget.model, frame, False)  # TODO: 在这一行卡死
        if pred == None:
            QMessageBox.warning(self.widget, "警告", "当前图像中未检测到人体，无法保存动作！")
            return None
        if self.widget.isFirst:
            self.widget.dist, skeleton = tools.normalization(pred['pred_coords'][0])
            self.widget.isFirst = False
            # 移动视频文件
            self.widget.moveVideo(self.widget.videoPath)
        else:
            dist, skeleton = tools.normalization(pred['pred_coords'][0], dis=self.widget.dist)

        # 信息写入文件
        infoItem = {
            "timeid": int(self.widget.horizontalSlider.value()),
            "reactime": self.widget.reacTime.text(),
            "score": (self.widget.Score.currentIndex()+1) * 2,
            "posepoints": skeleton.asnumpy().tolist()
        }
        self.widget.info.append(infoItem)
        self.widget.poseInfo["info"] = self.widget.info
        savePath = os.path.realpath(os.path.join(self.widget.SAVE_PATH, os.path.basename(self.widget.videoPath)+".json"))
        with open(savePath, "w") as f:
            f.write(json.dumps(self.widget.poseInfo))

    def playPause(self):
        self.widget.playOrStop.setText("播放")
        self.widget.play = False
        self.widget.player.pause()

if __name__ == "__main__":
    os.environ["MXNET_CUDNN_AUTOTUNE_DEFAULT"] = str(0)
    app = QApplication(sys.argv)
    Dc = DcDesigner()
    Dc.show()
    sys.exit(app.exec_())
