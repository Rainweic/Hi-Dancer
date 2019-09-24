import sys
from PyQt5.QtWidgets import  QApplication
from frame import Game_start, gundou, Ui_StartDance

if __name__ == '__main__':
    #实例化窗口和APP
    app = QApplication(sys.argv)
    gameStartFrame = Game_start.Ui_MainWindow()
    chooseFrame = gundou.Ui_MainWindow()
    startDanceFrame = Ui_StartDance.Ui_Dialog()

    #设置窗口标题
    gameStartFrame.setWindowTitle("开始游戏")
    chooseFrame.setWindowTitle("选择关卡")
    startDanceFrame.setWindowTitle('Hi-Dancer')
    gameStartFrame.show()

    #main里的菜单
    main_menubar = chooseFrame.main_menubar
    main_menubar.triggered.connect(lambda:gameStartFrame.show())
    main_menubar.triggered.connect(lambda:chooseFrame.close())
 
    #开始游戏按钮
    Button_start = gameStartFrame.pushButton_2
    Button_start.clicked.connect(lambda:chooseFrame.show())
    Button_start.clicked.connect(lambda:gameStartFrame.close())

    #关卡选择选择listview
    listview = chooseFrame.listView
    listview.clicked.connect(lambda:startDanceFrame.show())
    listview.clicked.connect(lambda:chooseFrame.close())

    #跳舞页面返回按钮
    backButton = startDanceFrame.pushButton_2
    backButton.clicked.connect(lambda:chooseFrame.show())
    backButton.clicked.connect(lambda:startDanceFrame.close())

    #保证app推出后，程序才关闭
    sys.exit(app.exec_())
