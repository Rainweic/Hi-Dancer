import cv2
import time
from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
from gluoncv.data.transforms.pose import detector_to_simple_pose, heatmap_to_coord

def load_model(detector_name='yolo3_mobilenet1.0_coco', pose_net_name='simple_pose_resnet18_v1b', use_gpu=True):
    
    '''
    detector_name detector模型名
    pose_net_name pose_net模型名
    use_gpu 是否使用gpu
    return net 返回模型
    '''

    if use_gpu == False:
        ctx = mx.cpu()
    else :
        ctx = mx.gpu()
    
    print("正在加载detector模型...")
    detector = model_zoo.get_model(detector_name, pretrained=True)
    detector.collect_params().reset_ctx(ctx)
    detector.hybridize()
    detector.reset_class(["person"], reuse_weights=['person'])
    print("加载detector模型成功")
    
    print("正在加载pose_net模型...")
    pose_net = model_zoo.get_model(pose_net_name, pretrained=True)
    pose_net.collect_params().reset_ctx(ctx)
    pose_net.hybridize()
    print("加载pose_net模型成功")
    net = {'detector': detector, 'pose_net': pose_net}
    return net

def detection(net, image, use_gpu):
    '''
    net 模型
    image 图片
    use_gpu 是否使用gpu
    return pred, img 返回pred字典和图片
    '''
    if use_gpu == False:
        ctx = mx.cpu()
    else :
        ctx = mx.gpu()
        
    x, img = data.transforms.presets.ssd.load_test(image, short=512)
    x = x.as_in_context(ctx)
    class_IDs, scores, bounding_boxs = net['detector'](x)
    pose_input, upscale_bbox = detector_to_simple_pose(img, class_IDs, scores, bounding_boxs)
    
    pose_input = pose_input.as_in_context(ctx)
    predicted_heatmap = net['pose_net'](pose_input)
    pred_coords, confidence = heatmap_to_coord(predicted_heatmap, upscale_bbox)
    pred = {'class_IDs':class_IDs, 'scores':scores, 'bounding_boxs':bounding_boxs, 'pred_coords':pred_coords, 'confidence':confidence}
    return pred, img


