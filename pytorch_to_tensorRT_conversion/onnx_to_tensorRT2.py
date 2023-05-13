import torch
import cv2
#import onnx
import os
import time
from torchvision import transforms
from PIL import Image
# from albumentations import Resize, Compose
# from albumentations.pytorch.transforms import  ToTensor
# from albumentations.augmentations.transforms import Normalize
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
import tensorrt as trt




#onnx_model_path='model-90000-best_abs_rel_0.09009.onnx'
#tensorrt_engine_path='./model-90000-best_abs_rel_0.09009_tensorrt.engine'
tensorrt_engine_path='./model-90000-best_abs_rel_0.09009.trt'
engine_precision='FP16'
img_size=[3, 480, 640]
batch_size=1

#onnx_model = onnx.load(onnx_model_path)
#onnx.checker.check_model(onnx_model)

TRT_LOGGER = trt.Logger()
 
# def build_engine(onnx_model_path, tensorrt_engine_path, engine_precision, img_size, batch_size):
    
#     logger = trt.Logger(trt.Logger.ERROR)
#     builder = trt.Builder(logger)
#     network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
#     profile = builder.create_optimization_profile()
#     config = builder.create_builder_config()
    
#     if engine_precision == 'FP16':
#         config.set_flag(trt.BuilderFlag.FP16)
    
#     parser = trt.OnnxParser(network, logger)

#     if not os.path.exists(onnx_model_path):
#         print("Failed finding ONNX file!")
#         exit()
#     print("Succeeded finding ONNX file!")

#     with open(onnx_model_path, "rb") as model:
#         if not parser.parse(model.read()):
#             print("Failed parsing .onnx file!")
#             for error in range(parser.num_errors):
#             	print(parser.get_error(error))
#             exit()
#         print("Succeeded parsing .onnx file!")
    
    
#     inputTensor = network.get_input(0) 
#     print('inputTensor.name:', inputTensor.name)
    
#     profile.set_shape(inputTensor.name, (batch_size, img_size[0], img_size[1], img_size[2]), \
#         (batch_size, img_size[0], img_size[1], img_size[2]), \
#         (batch_size, img_size[0], img_size[1], img_size[2]))

#     config.add_optimization_profile(profile)
    
    
#     engineString = builder.build_serialized_network(network, config)
#     if engineString == None:
#         print("Failed building engine!")
#         exit()
#     print("Succeeded building engine!")
#     with open(tensorrt_engine_path, "wb") as f:
#         f.write(engineString)


# def preprocess_image(img_path):
#     transforms = Compose([
#         Resize(224, 224, interpolation=cv2.INTER_NEAREST),
#         Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#         ToTensor(),
#     ])
     
#     input_img = cv2.imread(img_path)
#     input_img = np.asarray( input_img)
#     input_data = transforms(image=input_img)["image"]
#     batch_data = torch.unsqueeze(input_data, 0)
#     return batch_data
 
def _is_pil_image(img):
    return isinstance(img, Image.Image)

def _is_numpy_image(img):
    return isinstance(img, np.ndarray) and (img.ndim in {2, 3})

def to_tensor(pic):
    if not (_is_pil_image(pic) or _is_numpy_image(pic)):
        raise TypeError(
            'pic should be PIL Image or ndarray. Got {}'.format(type(pic)))
    
    if isinstance(pic, np.ndarray):
        img = torch.from_numpy(pic.transpose((2, 0, 1)))
        return img
    
    # handle PIL Image
    if pic.mode == 'I':
        img = torch.from_numpy(np.array(pic, np.int32, copy=False))
    elif pic.mode == 'I;16':
        img = torch.from_numpy(np.array(pic, np.int16, copy=False))
    else:
        img = torch.ByteTensor(torch.ByteStorage.from_buffer(pic.tobytes()))
    # PIL image mode: 1, L, P, I, F, RGB, YCbCr, RGBA, CMYK
    if pic.mode == 'YCbCr':
        nchannel = 3
    elif pic.mode == 'I;16':
        nchannel = 1
    else:
        nchannel = len(pic.mode)
    img = img.view(pic.size[1], pic.size[0], nchannel)
    
    img = img.transpose(0, 1).transpose(0, 2).contiguous()
    if isinstance(img, torch.ByteTensor):
        return img.float()
    else:
        return img

def to_tensor2(pic):

    if isinstance(pic, np.ndarray):
        img = torch.from_numpy(pic.transpose((2, 0, 1)))
        return img


def preprocess_image(img_path):
    image = np.asarray(Image.open(img_path), dtype=np.float32) / 255.0
    image = to_tensor2(image)
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    image = normalize(image)
    return image

def main():
    #build_engine(onnx_model_path, tensorrt_engine_path, engine_precision, img_size, batch_size)
    a = time.time()
    trt.init_libnvinfer_plugins(None, "")
    with open('model-90000-best_abs_rel_0.09009.trt', "rb") as f, trt.Runtime(TRT_LOGGER) as runtime: 
        engine = runtime.deserialize_cuda_engine(f.read()) 
    b = time.time()
    print(f"Took {(b-a):.2f} seconds for loading model!!")
    context = engine.create_execution_context()

    for binding in engine:
        if engine.binding_is_input(binding):  
            input_shape = engine.get_binding_shape(binding)
            input_size = trt.volume(input_shape) * engine.max_batch_size * np.dtype(np.float32).itemsize  
            device_input = cuda.mem_alloc(4*input_size)
        else:  
            output_shape = engine.get_binding_shape(binding)
            host_output = cuda.pagelocked_empty(trt.volume(output_shape) * engine.max_batch_size, dtype=np.float32)
            device_output = cuda.mem_alloc(4*host_output.nbytes)

    stream = cuda.Stream()
    sample_img_path = "/home/vision/suraj/Pixelformer_jetson/datasets/nyu_depth_v2_small/test/bathroom/rgb_00045.jpg"
    data = preprocess_image(sample_img_path).numpy()
    x = time.time()
    host_input = np.array(data, dtype=np.float32, order='C')
    cuda.memcpy_htod_async(device_input, host_input, stream)

    context.execute_async(bindings=[int(device_input), int(device_output)], stream_handle=stream.handle)
    cuda.memcpy_dtoh_async(host_output, device_output, stream)
    stream.synchronize()
    

    output_data = torch.Tensor(host_output).reshape(engine.max_batch_size, 480, 640)
    #output_data = host_output.reshape(engine.max_batch_size, 900, -1)
    
    y = time.time()
    print(f"Took {y-x:.2f} seconds for one image!!")
    print(f"Took {y-a:.2f} seconds from start!!")
    print(output_data.shape)
    #print(output_data[0])
    - try what happens when using FP16 while converting to onnx

if __name__ == '__main__':
    main()


