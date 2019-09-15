# 该类继承DcDesigner_UI.py
# UI 设置均在父类中
# 本类实现界面的逻辑功能

import sys
sys.path.append("../")
import PyQt5 as Qt
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, \
    QDialog, QLabel, QHBoxLayout, QFileDialog
from PyQt5.QtCore import *
from DcDesigner_UI import Ui_MainWindow
# from model.net import load_model, detection
# from score.tools import tools

class DcDesigner(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(DcDesigner, self).__init__()
        # 初始化UI
        self.setupUi(self)
        # 槽绑定
        self.chooseVideo.clicked.connect(self.chooseVideoFile())
        self.showCenter()
        self.load_model()

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
        self.videoPath = QFileDialog.getOpenFileName(self, "选择视频文件")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Dc = DcDesigner()
    Dc.show()
    sys.exit(app.exec_())