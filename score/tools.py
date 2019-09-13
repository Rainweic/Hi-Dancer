from mxnet import nd

def normalization(x):
    '''
    将人物骨架归一化：
        以头部胸部点为坐标原点，各坐标点减去胸部点坐标，同时测出头部与脚部的距离，各坐标点除以该距离
    
    input:
        x(ndarray):  二维的人体骨架关键点数组
    return:
        dis(float):  头脚距离最大值
        y(ndarray):  处理后二维人体骨架关键点数组
    '''
    
    # 鼻子部位坐标点
    arm_point = (x[5] + x[6]) / 2
    # 头脚距离（以最大值为准）
    dis = nd.max(x, (0, 1)) - nd.min(x, (0, 1))

    # 各坐标点减去鼻子点坐标
    x = x - arm_point
    # 各坐标点除以头脚距离
    y = x / dis
    return dis, y

def matching(sample_pose, player_pose):
    '''
    比较样本动作与玩家动作是否匹配，并返回匹配得分（0-17）

    input:
        sample_pose(ndarray):   样本动作骨架
        player_pose(ndarray):   玩家动作骨架
    return:
        score(int):             匹配得分
    '''

    r = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 
         0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]

    x_square = nd.square(sample_pose[:, 0] - player_pose[:, 0])
    y_square = nd.square(sample_pose[:, 1] - player_pose[:, 1])
    r_square = nd.square(nd.array(r))

    distant = x_square + y_square - r_square
    score = len(distant <= 0)

    return score
