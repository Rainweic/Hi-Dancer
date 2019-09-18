'''
该文件仅用于测试匹配算法 
涉及到的文件有的地方写的还不够完善
后期需要改进
'''

import os
import cv2 as cv
from score import tools
from model import net

os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = str(0)

#展示图片和玩家图片地址
showerUrl = "./image/test.jpeg"
playerUrl = "./image/test3.jpeg"
showerImage = cv.imread(showerUrl)
playerImage = cv.imread(playerUrl)

#加载模型并获得预测结果
use_gpu = False
model = net.load_model(use_gpu=use_gpu)
showerPre , showerImage = net.detection(model, showerImage, use_gpu)
playerPre , playerImage = net.detection(model, playerImage, use_gpu)

#归一化
showerDis ,showerSkeleton = tools.normalization(showerPre['pred_coords'][0])
playerDis ,playerSkeleton = tools.normalization(playerPre['pred_coords'][0]) 

#匹配计算分数并输出结果
score = tools.matching(playerSkeleton, showerSkeleton, use_gpu=use_gpu)
print("匹配得分{}".format(score))






