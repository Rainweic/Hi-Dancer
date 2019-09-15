# 该类继承DcDesigner_UI.py
# UI 设置均在父类中
# 本类实现界面的逻辑功能
# https://blog.csdn.net/aaa_a_b_c/article/details/80367147

import sys
sys.path.append("../")
import cv2 as cv
import PyQt5 as Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from DcDesigner_UI import Ui_MainWindow
# from model.net import load_model, detection
# from score.tools import tools

class DcDesigner(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(DcDesigner, self).__init__()
        self.play = False
        self.videoPath = None
        self.fps = 0
        # 初始化UI
        self.setupUi(self)
        self.showCenter()
        self.load_model()
        # 槽绑定
        self.chooseVideo.triggered.connect(self.chooseVideoFile)
        self.playOrStop.clicked.connect(self.playAndStop)

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
        # self.net = load_model(use_gpu=False)
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
        self.videoPath, filetype = QFileDialog.getOpenFileName(self, "选择视频文件")
        # 读取视频
        self.videoCap = cv.VideoCapture(self.videoPath)
        self.size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) 

    def playAndStop(self):
        if self.play:
            self.playOrStop.setText("暂停")
            self.play = True
            # 播放函数
        else:
            self.playOrStop.setText("播放")
            self.play = False
            # 暂停函数
        pass

    def playVideo(self):
        # 播放地址为空 提示警报
        if not self.videoPath:
            warningMessage = QMessageBox.warning(self, "警告！", "请先选择视频文件！")
            if warningMessage == QMessageBox.Close:
                return None
        while self.play:
            pass

    def saveAction(self):
        '''
        保存当前帧拥有的动作骨架
        '''
        pass    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Dc = DcDesigner()
    Dc.show()
    sys.exit(app.exec_())