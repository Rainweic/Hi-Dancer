import mxnet as mx
from mxnet import nd
from gluoncv import model_zoo, data
from gluoncv.data.transforms.pose import detector_to_simple_pose, heatmap_to_coord
from gluoncv.data.transforms.presets.ssd import transform_test


def load_model(detector_name='yolo3_mobilenet1.0_coco',
               pose_net_name='simple_pose_resnet18_v1b',
               use_gpu=True):
    '''
    加载模型

    input:
        detector_name(Str):     detector模型名
        pose_net_name(Str):     pose_net模型名
        use_gpu(bool):          是否使用gpu
    return 
        net(dict):             模型
    '''

    if use_gpu == False:
        ctx = mx.cpu()
    else:
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
    return net, True


def detection(net, image, use_gpu):
    '''
    进行预测：

    input:
        net(dict):     模型
        image(str):     图片(numpy)
        use_gpu(bool):  是否使用gpu
    return:
        pred(dict):     包含各种信息的字典
        img(numpy):     图片
    '''
    if use_gpu:
        ctx = mx.gpu()
    else:
        ctx = mx.cpu()
    img_adarry = nd.array(image)
    x, img = transform_test(img_adarry,
                            short=512,
                            max_size=1024,
                            mean=(0.485, 0.456, 0.406),
                            std=(0.229, 0.224, 0.225))
    x = x.as_in_context(ctx)
    class_IDs, scores, bounding_boxs = net['detector'](x)
    pose_input, upscale_bbox = detector_to_simple_pose(img, class_IDs, scores,
                                                       bounding_boxs)

    pose_input = pose_input.as_in_context(ctx)
    predicted_heatmap = net['pose_net'](pose_input)
    pred_coords, confidence = heatmap_to_coord(predicted_heatmap, upscale_bbox)

    if use_gpu:
        # pred_coords转移至GPU
        pred_coords = pred_coords.as_in_context(mx.gpu())

    pred = {
        'class_IDs': class_IDs,
        'scores': scores,
        'bounding_boxs': bounding_boxs,
        'pred_coords': pred_coords,
        'confidence': confidence
    }
    return pred, img