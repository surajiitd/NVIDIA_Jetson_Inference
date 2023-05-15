import onnx
import onnxruntime as rt
import time
import numpy as np
import torch
from PIL import Image
from torchvision.transforms import transforms
import matplotlib.pyplot as plt

def preprocess_image(img_path):
    image = np.asarray(Image.open(img_path), dtype=np.float32) / 255.0
    image = torch.from_numpy(image.transpose((2, 0, 1)))
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    image = normalize(image)
    return image.unsqueeze(0)

print(rt.get_device())

# ONNX_path = '/home/vision/Gaurav/TensorRT_main/convertedFiles_onnx_IR/DN-Def-DETR/model_f1.onnx'
onnx_path = '/home/vision/suraj/jetson-documentation/model_compression/onnx_models/from_vision04/nyu_model-64000-best_abs_rel_0.09021.onnx'
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
pred_depth = onnx_result.squeeze()
print('Time for one image:', onnx_end_time - onnx_start_time)

#depth = onnx_result.transpose
plt.imsave("pred_depth_onnx.png",pred_depth,cmap="magma",vmin=0,vmax=3)
