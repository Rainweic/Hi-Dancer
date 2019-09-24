import sys
import json
import os
import cv2
sys.path.append("..")
import myGlobal as gl

def findAllJsonPath(path):
    '''
        找到某目录下的所有json文件
        input:
            path(str):          目录地址

        return:
            pathes(list(str)):  找到的json文件的地址列表
    '''
    pathes = []
    fileNameList = os.listdir(path)
    for fileName in fileNameList:
        newDir = os.path.join(path,fileName)
        if os.path.isfile(newDir):
            if os.path.splitext(newDir)[1] == '.json':
                pathes.append(newDir)
                #print(newDir)
    return pathes


def resolveJson(path):
    '''
        解析json文件为Python数据
        input：
            path(str):                      json文件地址

        return：
            {
                'videoPath':(str)           视频地址
                'info':[
                    {
                        "timeid": (int),    视频放时间（ms）
                        "reactime": (float),反应时间
                        "score":  (int),    分数
                        "posepoints": []    骨架关键点
                    },
                    {}
                ]
            }
    '''
    file = open(path,'rb')
    fileJson = json.load(file)
    videoPath = fileJson["videopath"]
    info = fileJson['info']

    return {'videopath':videoPath, 'info':info}


def getVideosInfo(path):
    '''
        获取所有json文件的所有信息
        input:
            path(str):          目录地址
        
        return：
            allInfo:
            [
                {
                    'videoPath':(str)           视频地址
                    'info':[
                        {
                            "timeid": (int),    视频放时间（ms）
                            "reactime": (float),反应时间
                            "score":  (int),    分数
                            "posepoints": []    骨架关键点
                        },
                        {}
                    ]
                },
                {}
            ]
            demoImages:[
                (image),
                (image)                         演示图片
            ]

            
    '''
    pathes = findAllJsonPath(path)
    allInfo = []
    demoImages = []

    for onePath in pathes:
        info = resolveJson(onePath)
        allInfo.append(info)
        cap = cv2.VideoCapture(info['videopath'])
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame = int(info['info'][0]['timeid'] * fps /10000) - 1
        cap.set(cv2.CAP_PROP_POS_FRAMES,frame)
        success,img = cap.read()
        demoImages.append(img)

    return allInfo,demoImages


def saveJson2Global(videoPath,info):
    '''
        将videoPath,info保存在全局变量中
        input:
            videopath:(str)             视频地址
            info:[
                {
                    "timeid": (int),    视频放时间（ms）
                    "reactime": (float),反应时间
                    "score":  (int),    分数
                    "posepoints": []    骨架关键点
                },
                {}
            ]
    '''
    gl.GL_VPath = videoPath
    gl.GL_VInfo = info


    


