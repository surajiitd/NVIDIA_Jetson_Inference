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
import matplotlib.cm as cm
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

engine_precision='FP16'
#img_size = [3, 480, 640] # for NYUv2
img_size = [3, 352, 1216] # for kitti
batch_size=1
dataset = "kitti"
TRT_LOGGER = trt.Logger()

def get_image_path_lists(rgb_path, gt_depth_path, data_splits_file_path):
    with open(data_splits_file_path,'r') as f:
        filenames = f.readlines()
    rgb_path_list = []
    gt_depth_path_list = []
    for line in filenames:
        rgb_file = line.split()[0]
        if dataset == "kitti":
            depth_file = os.path.join(line.split()[0].split('/')[0], line.split()[1])
        else:
            depth_file = line.split()[1]

        rgb_path_list.append(os.path.join(rgb_path,rgb_file))
        gt_depth_path_list.append(os.path.join(gt_depth_path,depth_file))
    return rgb_path_list, gt_depth_path_list

def preprocess_image(img_path):
    image = np.asarray(Image.open(img_path), dtype=np.float32) / 255.0
    image = torch.from_numpy(image.transpose((2, 0, 1)))
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    image = normalize(image)
    return image

def colorize(depth,cmap="inferno", vmin=0,vmax=10):
    depth = np.clip(depth,vmin,vmax)
    colormap = cm.get_cmap(cmap)
    colored_depth = colormap((depth-vmin)/(vmax-vmin))
    colored_depth_rgb = (colored_depth[:,:,:3]*255).astype(np.uint8)
    return colored_depth_rgb


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
    rgb_path = "/home/vision/suraj/Pixelformer_jetson/datasets/kitti_small/kitti_gt"
    gt_depth_path = "/home/vision/suraj/Pixelformer_jetson/datasets/kitti_small/kitti_gt"
    data_splits_file_path = "/home/vision/suraj/Pixelformer_jetson/data_splits/eigen_test_files_with_gt.txt"
    rgb_path_list, gt_depth_path_list = get_image_path_lists(rgb_path, gt_depth_path, data_splits_file_path)

    window_name = "Pixelformer Depth Prediction"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1200,400)
    start_time = time.time()
    for idx,(image_path,gt_depth_path) in enumerate(zip(rgb_path_list, gt_depth_path_list)):
        data = preprocess_image(image_path).numpy()
        host_input = np.array(data, dtype=np.float32, order='C')
        cuda.memcpy_htod_async(device_input, host_input, stream)

        context.execute_async(bindings=[int(device_input), int(device_output)], stream_handle=stream.handle)
        cuda.memcpy_dtoh_async(host_output, device_output, stream)
        stream.synchronize()

        output_data = torch.Tensor(host_output).reshape(engine.max_batch_size, img_size[1], img_size[2])
        pred_depth = output_data.cpu().numpy().squeeze()
        image = cv2.imread(image_path,-1)
        gt_depth = cv2.imread(gt_depth_path,-1)/1000.0
        pred_depth[gt_depth==0] = 0
        vmax = max(np.max(pred_depth),np.max(gt_depth))
        print("vmax = ",vmax)
        cmap='inferno'
        gt_depth = colorize(gt_depth, cmap=cmap, vmin=0, vmax=vmax)
        pred_depth = colorize(pred_depth, cmap=cmap, vmin=0, vmax=vmax)
        thickness=2
        cv2.rectangle(image,(0,5), (210,30), (0,0,0,1),-1)
        cv2.putText(image,"RGB Image",(10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness, cv2.LINE_AA)
        cv2.putText(gt_depth,"Groundtruth depth",(10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness, cv2.LINE_AA)
        cv2.putText(pred_depth,"Predicted depth",(10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness, cv2.LINE_AA)
        
        combined = np.vstack((image,gt_depth,pred_depth))
        cv2.imwrite(f"sample_output_images/kitti/{idx:03d}.png",combined)
        cv2.imshow(window_name, combined)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
    end_time = time.time()
    print(f"Took {end_time-start_time:.2f} seconds for {len(rgb_path_list)} image!!")
    print(f"Took {end_time-a:.2f} seconds from start!!")
    
    #plt.imsave("pred_depth_tensorrt.png",pred_depth,cmap="magma",vmin=0,vmax=3)


if __name__ == '__main__':
    onnx_model_path = "/home/vision/suraj/jetson-documentation/model_compression/onnx_models/from_vision04/nyu_model-64000-best_abs_rel_0.09021.onnx"
    tensorrt_engine_path = os.path.join("tensorRT_engines",os.path.basename(onnx_model_path)[:-5]+".trt")
    #convert onnx to tensorRT
    if not os.path.exists(tensorrt_engine_path):
        build_engine(onnx_model_path, tensorrt_engine_path, engine_precision, img_size, batch_size)

    #inference tensorrt
    tensorrt_inference(tensorrt_engine_path)



