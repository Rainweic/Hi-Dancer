from queue import Queue

"""
    此文件保存全局变量
    
    变量格式
    GL_VPath(str): ""             选择关卡的视频的path

    GL_VInfo(list):               选择关卡的关卡设定信息
        [
            {
                "timeid": 1232,
                "reactime": "0.5",
                "score":  10,
                "posepoints": []
            },
            {},
        ]
    GL_CurScore(int): 0          当前分数
    GL_TalScore(int): 0          总分
    GL_PerScore(float): 0.0      百分制得分
       
"""

GL_VPath = ''   # 选择关卡的视频的path
GL_VInfo = []   # 选择关卡的关卡设定信息
GL_CurScoreQueue = Queue(maxsize= 100) # 当前分数队列
GL_TalScore = 0 # 总分
GL_PerScore = 0.0 # 百分制得分
GL_Images = []    #截取摄像视频流视频的图片list
GL_Images_Length = 0 #截取图片的数量
GL_Model = None   #加载的模型