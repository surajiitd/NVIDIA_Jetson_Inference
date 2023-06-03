import torch
import cv2
import numpy as np
import depthai
import threading
import os
import sys
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

# Global variables
selected_points = []
completed = False
# Global variables
frame = None
is_frame_available = False
stop_capture = threading.Event()  # Event object to signal stop

engine_precision='FP16'
#img_size = [3, 480, 640] # for NYUv2
img_size = [3, 352, 1216] # for kitti
#img_size = [3, 192, 640] # for kitti from lenovo frame of size (480,640)
batch_size=1
dataset = "kitti" #"kitti" or "nyu" 
min_depth_eval = 1e-3
max_depth_eval = 80 if dataset == 'kitti' else 10
TRT_LOGGER = trt.Logger()

def live_preprocess_image(image):
    #image = np.asarray(Image.open(img_path), dtype=np.float32) / 255.0
    image = image / 255.0
    image = torch.from_numpy(image.transpose((2, 0, 1)))
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    image = normalize(image)
    return image



def colorize(depth,cmap, vmin=None,vmax=None):
    vmin = depth.min() if vmin is None else vmin
    vmax = depth.max() if vmax is None else vmax

    depth = np.clip(depth,vmin,vmax)
    #depth = 1/depth
    colormap = cm.get_cmap(cmap)
    colored_depth = colormap((depth-vmin)/(vmax-vmin)) #first convert from 0-1 then from 0-255 in below line.
    #colored_depth = colormap(depth)
    colored_depth_rgb = (colored_depth[:,:,:3]*255).astype(np.uint8)
    return colored_depth_rgb


# Function to continuously capture frames
def capture_frames():
    global frame, is_frame_available

    # Create the pipeline and camera node
    pipeline = depthai.Pipeline()
    cam = pipeline.createColorCamera()
    #Unsupported resolution set for detected camera IMX378/214, needs THE_1080_P / THE_4_K / THE_12_MP. 
    cam.setResolution(depthai.ColorCameraProperties.SensorResolution.THE_1080_P)
    #cam.initialControl.setManualFocus(150) # 0..255 (larger for near objects) 
    # Focus: 
    # value 150 == 22cm 
    # value 140 == 36cm
    
    xoutRgb = pipeline.createXLinkOut()
    xoutRgb.setStreamName("rgb")
    cam.video.link(xoutRgb.input)

    # Start the pipeline
    with depthai.Device(pipeline) as device:
        # Output queue for the frames
        q_rgb = device.getOutputQueue(name="rgb", maxSize=1, blocking=False)
        print('Connected cameras:', device.getConnectedCameraFeatures())
        print('Usb speed:', device.getUsbSpeed().name)
        if device.getBootloaderVersion() is not None:
            print('Bootloader version:', device.getBootloaderVersion())
        # Device name
        print('Device name:', device.getDeviceName())
        while not stop_capture.is_set():
            # Get the RGB frame
            in_rgb = q_rgb.tryGet()
            #focus_value = q_rgb.getCtrlValue(depthai.CameraControl.CamCtrl.FOCUS)
            #print("Focus = ",focus_value)
            if in_rgb is not None:
                # Convert the NV12 format to BGR
                frame = in_rgb.getCvFrame()

                # Set the flag to indicate that a new frame is available
                is_frame_available = True

def sort_coordinates(selected_points):

    # Sort the points by x-coordinate
    sorted_points = sorted(selected_points, key=lambda p: p[0])

    # Determine the top-left and top-right points
    if sorted_points[0][1] < sorted_points[1][1]:
        top_left, bottom_left = sorted_points[0], sorted_points[1]
    else:
        top_left, bottom_left = sorted_points[1], sorted_points[0]

    # Determine the bottom-right and bottom-left points
    if sorted_points[2][1] < sorted_points[3][1]:
        top_right, bottom_right = sorted_points[2], sorted_points[3]
    else:
        top_right, bottom_right = sorted_points[3], sorted_points[2]

    final_sorted_points = [top_left, top_right, bottom_right, bottom_left]
    return final_sorted_points

# Mouse callback function for selecting points
def store_points(event, x, y, flags, param):
    global selected_points, completed

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(selected_points) < 4:
            selected_points.append((x, y))
            for (x,y) in selected_points:
                cv2.circle(frame, (x, y), 9, (0, 255, 0), -1)
            cv2.imshow('Select Points', frame)
            print((x,y))
            if len(selected_points) == 4:
                completed = True

def get_scale_shift(prediction, target,  min_depth, max_depth):
    """Returns the median scaling factor from gt_depth and pred_depth,
        Tells by what scale factor you should scale up(multipy) your pred_depth.
    """
    mask = np.logical_and(target>min_depth , target<max_depth)
    scale = np.median(target[mask]) / np.median(prediction[mask])
    return scale

def select_points():
    screen_width, screen_height = 1920, 1080  # Replace with your screen resolution
    # Calculate the dimensions for the right half of the screen
    right_half_x = screen_width // 2
    right_half_y = screen_height
    right_half_width = screen_width // 2
    right_half_height = screen_height
    window_name = 'Select Points'
    # Create a resizable window for the camera feed
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, right_half_x, 0)
    cv2.resizeWindow(window_name, right_half_width, right_half_height)
    # Create a window and set the mouse callback
    # cv2.namedWindow('Select Points', cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty('Select Points', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(window_name, store_points)
    global selected_points
    # Instructions
    print("Please select 4 corner points of the rectangular screen.")
    while True:
        
        while not is_frame_available:
            pass
        #img = frame.copy()

        # Draw a circle to mark the selected point
        for (x,y) in selected_points:
            cv2.circle(frame, (x, y), 9, (0, 255, 0), -1)
        # Display the image
        cv2.imshow(window_name, frame)
        
        # Wait for the user to select points
        if completed:
            break

        # Check for key press
        key = cv2.waitKey(1)
        if key == ord('q'):
            sys.exit(0)
            break
    cv2.destroyAllWindows()


def tensorrt_inference(tensorrt_engine_path):
    a = time.time()
    trt.init_libnvinfer_plugins(None, "")
    with open(tensorrt_engine_path, "rb") as f, trt.Runtime(TRT_LOGGER) as runtime: 
        print("engine initialized")
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

    # Define the destination points (a rectangle)
    width, height = 1216, 352 #kitti 
    dst_points = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

    global selected_points, frame, is_frame_available
    selected_points = sort_coordinates(selected_points)
    print("Selected points are:",selected_points)
    # Convert the selected points to numpy array
    src_points = np.array(selected_points, dtype=np.float32)


    start_time = time.time()
    idx=0
    while True:
        global_idx = idx+1
        # Read a frame from the webcam
        #ret, image = cap.read()
        
        while not is_frame_available:
            pass
        #"""
        image = frame.copy()
        # Perform the homography transformation
        M, _ = cv2.findHomography(src_points, dst_points)

        # Warp the image
        image = cv2.warpPerspective(image, M, (width, height))
        #print("image size after warping:",image)
        
        data = live_preprocess_image(image)
        
        host_input = np.array(data, dtype=np.float32, order='C')
        cuda.memcpy_htod_async(device_input, host_input, stream)

        context.execute_async(bindings=[int(device_input), int(device_output)], stream_handle=stream.handle)
        cuda.memcpy_dtoh_async(host_output, device_output, stream)
        stream.synchronize()

        output_data = torch.Tensor(host_output).reshape(engine.max_batch_size, img_size[1], img_size[2])
        pred_depth = output_data.cpu().numpy().squeeze()

        cmap='inferno' #'magma', 'inferno'
        #gt_depth = colorize(gt_depth, cmap=cmap, vmin=0, vmax=vmax)
        #print(f"min = {np.min(pred_depth), np.max(pred_depth)}")
        #old
        #pred_depth = colorize(pred_depth, cmap=cmap,vmin = 0,vmax=6)
        #new
        print(np.median(pred_depth),np.max(pred_depth),np.mean(pred_depth))
        a = plt.imsave('temp.png', (3-np.log(pred_depth))/10, cmap='plasma')
        print(a)
        pred_depth = cv2.imread('temp.png')
        
        #sys.exit(0)
        thickness=2
        
        cv2.rectangle(image,(0,0), (190,35), (0,0,0),-1)
        cv2.rectangle(pred_depth,(0,0), (270,35), (0,0,0),-1)
        cv2.putText(image,"RGB Image",(5,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness, cv2.LINE_AA)
        #cv2.putText(gt_depth,"Groundtruth depth",(10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness, cv2.LINE_AA)
        cv2.putText(pred_depth,"Predicted depth",(5,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness, cv2.LINE_AA)
        #print(image.shape, pred_depth.shape)
        combined = np.vstack((image,pred_depth))

        window_name = "Pixelformer Depth Prediction"    
        screen_width, screen_height = 1920, 1080  # Replace with your screen resolution
        # Calculate the dimensions for the right half of the screen
        right_half_x = screen_width // 2
        right_half_y = screen_height
        right_half_width = screen_width // 2
        right_half_height = screen_height
        # Create a resizable window for the camera feed
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(window_name, right_half_x, 0)
        cv2.resizeWindow(window_name, right_half_width, right_half_height)
        # cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        #cv2.resizeWindow(window_name, 1800,1000)

        #cv2.imwrite(f"sample_output_images/kitti/{idx:03d}.png",combined)
        # left_pad = np.zeros((704,1216,3))
        # combined = np.hstack(left_pad, combined)
        cv2.imshow(window_name, combined)
        idx+=1
        #"""
        #key = cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_capture.set()  # Set the stop signal
            break
        

    cv2.destroyAllWindows()
    #cap.release()
    end_time = time.time()
    print(f"Took {end_time-start_time:.2f} seconds for {global_idx} images!!")
    #print(f"{len(rgb_path_list)/(end_time-start_time)} FPS")
    print(f"{global_idx/(end_time-start_time)} FPS")
    print(f"Took {end_time-a:.2f} seconds from start!!")
    
    #plt.imsave("pred_depth_tensorrt.png",pred_depth,cmap="magma",vmin=0,vmax=3)



# Start the frame capture thread
capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()

#select 4 points of the screen
select_points()

#perform homography 
tensorrt_engine_path = "/home/vision/suraj/jetson-documentation/model_compression/tensorRT_engines/kitti_model-55000-best_abs_rel_0.05135.trt"
tensorrt_engine_path = "/home/vision/suraj/jetson-documentation/model_compression/tensorRT_engines/kitti_model-55000-best_abs_rel_0.05135.trt"
tensorrt_inference(tensorrt_engine_path)

# Wait for the frame capture thread to finish
capture_thread.join()

# Release resources
cv2.destroyAllWindows()




# if __name__ == '__main__':

#     # Start the frame capture thread
#     capture_thread = threading.Thread(target=capture_frames)
#     capture_thread.start()

#     perform_homography()

#     # Wait for the frame capture thread to finish
#     capture_thread.join()

#     # Release resources
#     cv2.destroyAllWindows()
