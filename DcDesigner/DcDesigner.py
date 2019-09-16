# 该类继承DcDesigner_UI.py
# UI 设置均在父类中
# 本类实现界面的逻辑功能

import sys
sys.path.append("..")
import cv2 as cv
import PyQt5 as Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import  *
from DcDesigner_UI import Ui_MainWindow
from model import net
from score import tools

class DcDesigner(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(DcDesigner, self).__init__()
        self.play = False
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
        hbox = QHBoxLayout()
        label = QLabel("模型加载中...", self)
        hbox.addWidget(label)
        dialog.setLayout(hbox)
        dialog.setWindowModality(Qt.ApplicationModal)
        self.model = net.load_model(use_gpu=False)
        dialog.close()

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
        self.videoPath = QFileDialog.getOpenFileUrl()[0]
        self.player.setMedia(QMediaContent(self.videoPath))
        self.videoCapTure = cv.VideoCapture(str(self.videoPath)[25:-2])
        
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

    def saveAction(self):
        '''
        保存当前帧拥有的动作骨架
        '''
        if self.videoCapTure == None:
            QMessageBox.warning(self, "警告！", "请选择视频文件！")
            return None
        self.videoCapTure.set(cv.CAP_PROP_POS_MSEC, int(self.player.position()))    # 通过ms进行定位
        ret, frame = self.videoCapTure.read()   # 获取帧
        # TODO: 骨架预测
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Dc = DcDesigner()
    Dc.show()
    sys.exit(app.exec_())