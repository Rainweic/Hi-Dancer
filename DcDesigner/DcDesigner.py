# 该类继承DcDesigner_UI.py
# UI 设置均在父类中
# 本类实现界面的逻辑功能

import os
import sys
sys.path.append("..")
import json
import shutil
import cv2 as cv
import PyQt5 as Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import  *
from DcDesigner_UI import Ui_MainWindow
from model import net
from score import tools

class DcDesigner(QMainWindow, Ui_MainWindow):

    SAVE_PATH = "../poseinfo"

    def __init__(self):
        super(DcDesigner, self).__init__()
        self.play = False
        self.isFirst = True
        self.videoLength = 0.1
        self.videoCapTure = None
        # 初始化UI
        self.setupUi(self)
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
        self.addAction.clicked.connect(self.saveAction)

    def load_model(self):
        '''
        加载模型 并弹出提示 
        '''
        dialog = QDialog()
        dialog.setWindowTitle("提示")
        label = QLabel("模型加载中...\n初次使用会自动下载模型...", dialog)
        label.setWordWrap(True)
        closeButton = QPushButton("完成", dialog)
        closeButton.setEnabled(False)
        dialog.resize(250, 180)
        dialog.setWindowModality(Qt.WindowModal)
        dialog.show()
        closeButton.clicked.connect(dialog.close)
        self.model, flag = net.load_model(use_gpu=False)
        if flag:
            closeButton.setEnabled(True)

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
        self.videoPath = str(videoPathQT)[26:-2]
        print(self.videoPath)
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

    def moveVideo(oldPath, newPath="../poseinfo/video"):
        '''
        将视频文件搬运到指定位置： ../poseinfo/video
        '''
        if not os.path.exists(newPath):
            os.mkdir(newPath)
            print("新建文件夹ing")

        shutil.copy(oldPath, newPath)

    def saveAction(self):
        '''
        保存当前帧拥有的动作骨架
        '''
        if self.videoCapTure == None:
            QMessageBox.warning(self, "警告！", "请选择视频文件！")
            return None

        self.videoCapTure.set(cv.CAP_PROP_POS_MSEC, int(self.player.position()))    # 通过ms进行定位
        ret, frame = self.videoCapTure.read()   # 获取帧
        # Test 为啥可以正常显示但是frame确为0
        cv.imshow("resr", frame)
        print(ret, frame)
        cv.waitKey(0)
        cv.destroyAllWindows()
        

        # # 骨架信息预测
        # pred, img = net.detection(self.model, frame, False)
        # if self.isFirst:
        #     self.dist, skeleton = tools.normalization(pred['pred_coords'][0])
        #     self.isFirst = False
        #     # 移动视频文件
        #     self.moveVideo(self.videoPath)
        # else:
        #     dist, skeleton = tools.normalization(pred['pred_coords'][0], dis=self.dist)

        # # 信息写入文件
        # infoItem = {
        #     "timeid": int(self.player.duration()),
        #     "reactime": self.reacTime.text(),
        #     "score": (self.Score.currentIndex()+1) * 2,
        #     "posepoints": int(skeleton.asnumpy()) 
        # }
        # self.info.append(infoItem)
        # self.poseInfo["info"] = self.info
        # with open(os.path.join(self.SAVE_PATH, self.videoPath+".json"), "w") as f:
        #     f.write(json.dumps(self.poseInfo))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Dc = DcDesigner()
    Dc.show()
    sys.exit(app.exec_())
