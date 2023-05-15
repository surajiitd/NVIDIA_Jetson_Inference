"""
Step 1: Install Dependencies

Install the required dependencies, including CUDA, cuDNN, and TensorRT, according to your system specifications and NVIDIA GPU compatibility.
"""

import torch
import torchvision
import torch.backends.cudnn as cudnn

import os, sys
import argparse
import numpy as np
from tqdm import tqdm
import time
import cv2
from PIL import Image
from torchvision import transforms
#sys.path.append('../Pixelformer_jetson')
# from ...Pixelformer_jetson.newcrfs.utils import post_process_depth, flip_lr, compute_errors
# from ...Pixelformer_jetson.newcrfs.networks.NewCRFDepth import NewCRFDepth
from newcrfs.utils import post_process_depth, flip_lr, compute_errors
from newcrfs.networks.NewCRFDepth import NewCRFDepth

encoder = "large07"
max_depth = 10.0
checkpoint_path = "../Pixelformer_jetson/trained_models_best/nyu/model-90000-best_abs_rel_0.09009"

def load_custom_model():
    model = NewCRFDepth(version=encoder, inv_depth=False, max_depth=max_depth, pretrained=None) 
    model = torch.nn.DataParallel(model)
    print("== Model Initialized")

    if checkpoint_path != '':
        if os.path.isfile(checkpoint_path):
            print("== Loading checkpoint '{}'".format(checkpoint_path))
            checkpoint = torch.load(checkpoint_path, map_location='cpu')
            model.load_state_dict(checkpoint['model'])
            print("== Loaded checkpoint '{}'".format(checkpoint_path))
            del checkpoint
        else:
            print("== No checkpoint found at '{}'".format(checkpoint_path))

    # cudnn.benchmark = True
    return model


def preprocess_image(img_path):
    image = np.asarray(Image.open(img_path), dtype=np.float32) / 255.0
    image = torch.from_numpy(image.transpose((2, 0, 1)))
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    image = normalize(image)
    return image.unsqueeze(0).cuda()

# Load the trained model
#model = torchvision.models.your_depth_estimation_model()
model = load_custom_model().eval().cuda()

# Convert the model to ONNX
#dummy_input = torch.randn(1, 3, 480, 640).cuda()  # Example input shape = torch.Size([1, 3, 480, 640])
sample_img_path = "/home/vision/suraj/Pixelformer_jetson/datasets/nyu_depth_v2_small/test/bathroom/rgb_00045.jpg"
input = preprocess_image(sample_img_path)
# import ipdb;ipdb.set_trace()
onnx_path = os.path.basename(checkpoint_path)+'.onnx'

#import ipdb; ipdb.set_trace()
#torch.onnx.export(model, dummy_input, onnx_path, opset_version=11) #error: ValueError: torch.nn.DataParallel is not supported by ONNX exporter
#torch.onnx.export(model.module, dummy_input, onnx_path, opset_version=12, export_params=True, verbose=True)
# I ran below command in vision04's eval.py file
torch.onnx.export(model.module, input, onnx_path,verbose=True, opset_version=14, input_names=['input'], output_names=['output']) 