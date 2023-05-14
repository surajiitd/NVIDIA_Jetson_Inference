import torch
import cv2
import onnx
import os
import time
# from albumentations import Resize, Compose
# from albumentations.pytorch.transforms import  ToTensor
# from albumentations.augmentations.transforms import Normalize
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
import tensorrt as trt

onnx_model_path='/home/vision/Gaurav/TensorRT_main/convertedFiles_onnx_IR/DINO/DINO_3Dec.onnx'
tensorrt_engine_path='./DINO_tensorrt.engine'
engine_precision='FP16'
img_size=[3, 224, 224]
batch_size=1

onnx_model = onnx.load(onnx_model_path)
onnx.checker.check_model(onnx_model)

TRT_LOGGER = trt.Logger()
 
def build_engine(onnx_model_path, tensorrt_engine_path, engine_precision, img_size, batch_size):
    
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
    transforms = Compose([
        Resize(224, 224, interpolation=cv2.INTER_NEAREST),
        Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensor(),
    ])
     
    input_img = cv2.imread(img_path)
    input_img = np.asarray( input_img)
    input_data = transforms(image=input_img)["image"]
    batch_data = torch.unsqueeze(input_data, 0)
    return batch_data
 


def main():
    #build_engine(onnx_model_path, tensorrt_engine_path, engine_precision, img_size, batch_size)
    trt.init_libnvinfer_plugins(None, "")
    with open('/home/vision/Gaurav/TensorRT/engines/DINO_new.engine', "rb") as f, trt.Runtime(TRT_LOGGER) as runtime: 
        engine = runtime.deserialize_cuda_engine(f.read()) 
          
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
    data = preprocess_image("/home/vision/Gaurav/TensorRT_main/coco_100_images/100_images_for_inference_time_calc/test_images/000000000139.jpg").numpy()
    x = time.time()
    host_input = np.array(data, dtype=np.float32, order='C')
    cuda.memcpy_htod_async(device_input, host_input, stream)

    
    context.execute_async(bindings=[int(device_input), int(device_output)], stream_handle=stream.handle)
    cuda.memcpy_dtoh_async(host_output, device_output, stream)
    stream.synchronize()
    

    output_data = torch.Tensor(host_output).reshape(engine.max_batch_size, 900, -1)
    
    y = time.time()
    print(y-x)
    
    print(output_data.shape)
    print(output_data[0])
    

if __name__ == '__main__':
    main()