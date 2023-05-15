import torch
import cv2
#import onnx
import os
import time
from torchvision import transforms
from PIL import Image
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
import tensorrt as trt
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)


engine_precision='FP16'
img_size=[3, 480, 640]
batch_size=1

TRT_LOGGER = trt.Logger()
 
def build_engine(onnx_model_path, tensorrt_engine_path, engine_precision, img_size, batch_size):
    print(f"TensorRT model will be saved in {tensorrt_engine_path}")
    onnx_model = onnx.load(onnx_model_path)
    onnx_model.checker.check_model(onnx_model)

    logger = trt.Logger(trt.Logger.ERROR)
    builder = trt.Builder(logger)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    profile = builder.create_optimization_profile()
    config = builder.create_builder_config()
    
    if engine_precision == 'FP16':
        config.set_flag(trt.BuilderFlag.FP16)
    
    parser = trt.OnnxParser(network, logger)

    if not os.path.exists(onnx_model_path):
        print("Failed finding ONNX file!")
        exit()
    print("Succeeded finding ONNX file!")

    with open(onnx_model_path, "rb") as model:
        if not parser.parse(model.read()):
            print("Failed parsing .onnx file!")
            for error in range(parser.num_errors):
            	print(parser.get_error(error))
            exit()
        print("Succeeded parsing .onnx file!")
    
    
    inputTensor = network.get_input(0) 
    print('inputTensor.name:', inputTensor.name)
    
    profile.set_shape(inputTensor.name, (batch_size, img_size[0], img_size[1], img_size[2]), \
        (batch_size, img_size[0], img_size[1], img_size[2]), \
        (batch_size, img_size[0], img_size[1], img_size[2]))

    config.add_optimization_profile(profile)
    
    
    engineString = builder.build_serialized_network(network, config)
    if engineString == None:
        print("Failed building engine!")
        exit()
    print("Succeeded building engine!")
    with open(tensorrt_engine_path, "wb") as f:
        f.write(engineString)


def preprocess_image(img_path):
    image = np.asarray(Image.open(img_path), dtype=np.float32) / 255.0
    image = torch.from_numpy(image.transpose((2, 0, 1)))
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    image = normalize(image)
    return image

def tensorrt_inference(tensorrt_engine_path):
    
    a = time.time()
    trt.init_libnvinfer_plugins(None, "")
    with open(tensorrt_engine_path, "rb") as f, trt.Runtime(TRT_LOGGER) as runtime: 
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
    pred_depth = output_data.cpu().numpy().squeeze()
    plt.imsave("pred_depth_tensorrt.png",pred_depth,cmap="magma",vmin=0,vmax=3)


if __name__ == '__main__':
    onnx_model_path = "/home/vision/suraj/jetson-documentation/model_compression/onnx_models/from_vision04/nyu_model-64000-best_abs_rel_0.09021.onnx"
    tensorrt_engine_path = os.path.join("tensorRT_engines",os.path.basename(onnx_model_path)[:-5]+".trt")
    #convert onnx to tensorRT
    if not os.path.exists(tensorrt_engine_path):
        build_engine(onnx_model_path, tensorrt_engine_path, engine_precision, img_size, batch_size)

    #inference tensorrt
    tensorrt_inference(tensorrt_engine_path)



