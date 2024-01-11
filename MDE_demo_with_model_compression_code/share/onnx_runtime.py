# import os
# import cv2
# import onnxruntime
# # import pandas as pd

# import numpy as np
# # import cv2
# from shapely.geometry import Polygon
# import pyclipper
# import torch
# import time
# from PIL import Image
# from torchvision.transforms import transforms
# import json
# # import paddle
# from PIL import Image
# from typing import Tuple
# from torchvision import transforms as T
# from torchvision.ops import nms
# import time
# import json
# import onnxruntime as ort


# import torch
# import cv2
# #import onnx
# import os
# import time
# from torchvision import transforms
# from PIL import Image
# # from albumentations import Resize, Compose
# # from albumentations.pytorch.transforms import  ToTensor
# # from albumentations.augmentations.transforms import Normalize
# import pycuda.driver as cuda
# import pycuda.autoinit
# import numpy as np
# import tensorrt as trt

# def to_numpy(tensor):
#     return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


# def resize_image(img):
#     height, width, _ = img.shape
#     resized_img = cv2.resize(img, (224,224))
#     return resized_img


# def load_image(image_path):
#     img = cv2.imread(image_path, cv2.IMREAD_COLOR).astype('float32')
#     img = resize_image(img)
#     img = torch.from_numpy(img).permute(2, 0, 1).float().unsqueeze(0)
#     img_mean = [123.675, 116.28, 103.53]
#     img_std = [58.395, 57.12, 57.375]
#     transform_norm = transforms.Compose([
#         transforms.Normalize(img_mean, img_std)
#     ])
#     img_normalized = transform_norm(img)
#     img=img_normalized.numpy()
#     print(img.shape)
#     print('BLOB SHAPE:',img.shape)
#     return img#########################
# def to_tensor2(pic):

#     if isinstance(pic, np.ndarray):
#         img = torch.from_numpy(pic.transpose((2, 0, 1)))
#         return img


# def preprocess_image(img_path):
#     image = np.asarray(Image.open(img_path), dtype=np.float32) / 255.0
#     image = to_tensor2(image)
#     normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
#     image = normalize(image)
#     return image

# # img = load_image('/home/vision/Gaurav/TensorRT/dataset/DINO_test_images/000000000285.jpg')
# # data=json.dumps({'inputs':img.tolist()})
# # data=np.array(json.loads(data)['inputs']).astype('float32')



# sample_img_path = "/home/vision/suraj/Pixelformer_jetson/datasets/nyu_depth_v2_small/test/bathroom/rgb_00045.jpg"
# img = preprocess_image(sample_img_path).numpy()
# data=json.dumps({'inputs':img.tolist()})
# data=np.array(json.loads(data)['inputs']).astype('float32')

# onnx_path = '/home/vision/suraj/jetson-documentation/pytorch_to_tensorRT_conversion/model-90000-best_abs_rel_0.09009.onnx'
# session=ort.InferenceSession(onnx_path,   providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
# input_name=session.get_inputs()[0].name
# output_1=session.get_outputs()[0].name
# #output_2=session.get_outputs()[1].name

# #results_onnx=session.run([output_1,output_2],{input_name:data})
# x = time.time()
# results_onnx=session.run([output_1],{input_name:data})
# print(f"took {time.time()-x:.3f} seconds")

# onnx_path = '/home/vision/suraj/jetson-documentation/pytorch_to_tensorRT_conversion/model-90000-best_abs_rel_0.09009.onnx'
# model = onnxruntime.InferenceSession(onnx_path, providers=['CUDAExecutionProvider'])

# sample_img_path = "/home/vision/suraj/Pixelformer_jetson/datasets/nyu_depth_v2_small/test/bathroom/rgb_00045.jpg"
# img = preprocess_image(sample_img_path).numpy()

# x = time.time()
# output = model.run(None, {'input':img})
# # print(f"took {time.time()-x:.3f} seconds")
#
###########################################
import onnx
import onnxruntime as rt
import time
import numpy as np
import torch
from PIL import Image
from torchvision.transforms import transforms

def preprocess_image(img_path):
    image = np.asarray(Image.open(img_path), dtype=np.float32) / 255.0
    image = torch.from_numpy(image.transpose((2, 0, 1)))
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    image = normalize(image)
    return image.unsqueeze(0)

print(rt.get_device())

# ONNX_path = '/home/vision/Gaurav/TensorRT_main/convertedFiles_onnx_IR/DN-Def-DETR/model_f1.onnx'
onnx_path = '/home/vision/suraj/jetson-documentation/pytorch_to_tensorRT_conversion/model-90000-best_abs_rel_0.09009.onnx'
onnx_model = onnx.load(onnx_path)


sess = rt.InferenceSession(onnx_path,  providers=[ 'CUDAExecutionProvider'])

onnx.checker.check_model(onnx_model)

sample_img_path = "/home/vision/suraj/Pixelformer_jetson/datasets/nyu_depth_v2_small/test/bathroom/rgb_00045.jpg"
image = preprocess_image(sample_img_path).numpy()

input_all = [node.name for node in onnx_model.graph.input]
input_initializer = [
    node.name for node in onnx_model.graph.initializer
]
net_feed_input = list(set(input_all) - set(input_initializer))
assert len(net_feed_input) == 1

sess_input = sess.get_inputs()[0].name
sess_output = sess.get_outputs()[0].name

onnx_start_time = time.time()
#import ipdb;ipdb.set_trace()
onnx_result = sess.run([sess_output], {sess_input: image})[0]
onnx_end_time = time.time()

print('--onnx--')
print(onnx_result.shape)
print(onnx_result[0][:10])
print('Time:', onnx_end_time - onnx_start_time)
import matplotlib.pyplot as plt
import ipdb;ipdb.set_trace()
#depth = onnx_result.transpo
plt.imshow(onnx_result, cmap="magma")
