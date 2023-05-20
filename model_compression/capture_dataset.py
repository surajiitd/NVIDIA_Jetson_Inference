import cv2
import numpy as np
import depthai
import threading
import sys
import os
# Global variables
selected_points = []
completed = False
# Global variables
dataset = "kitti"
img_size = [3, 352, 1216] # for kitti
frame = None
is_frame_available = False
stop_capture = threading.Event()  # Event object to signal stop

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
    global selected_points, completed, frame, is_frame_available
    while not is_frame_available:
            pass
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(selected_points) < 4:
            selected_points.append((x, y))
            for (x,y) in selected_points:
                cv2.circle(frame, (x, y), 9, (0, 255, 0), -1)
            cv2.imshow(window_name, frame)
            # cv2.waitKey(0)
            print((x,y))
            if len(selected_points) == 4:
                completed = True



def select_points():
    # Create a window and set the mouse callback
    screen_width, screen_height = 1920, 1080 #1920, 1080  # Replace with your screen resolution
    # Calculate the dimensions for the left half of the screen
    left_half_x = -10
    left_half_y = 0
    left_half_width = screen_width // 2
    left_half_height = screen_height

    window_name = 'Sample Image'
    # Create a resizable window for the webcam feed
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, left_half_x, left_half_y)
    cv2.resizeWindow(window_name, left_half_width, left_half_height)
    
    sample_image_path = "/home/vision/suraj/kitti_dataset/KITTI/2011_09_26/2011_09_26_drive_0001_sync/image_02/data/0000000000.png"
    image = cv2.imread(sample_image_path,-1)
    if dataset == "kitti": # do kb_crop
        height = img_size[1]
        width = img_size[2]
        top_margin = int(height - 352)
        left_margin = int((width - 1216) / 2)
        image = image[top_margin:top_margin + 352, left_margin:left_margin + 1216]
    top_padding = np.zeros((508,1216,3),dtype=np.uint8)
    bottom_padding = np.zeros((508,1216,3),dtype=np.uint8)
    # print(top_padding.shape)
    # print(bottom_padding.shape)

    image = np.vstack((top_padding,image,bottom_padding))
    cv2.imshow(window_name, image)
    # cv2.waitKey(1)
    global selected_points, frame, is_frame_available

    window_name = 'Select 4 Corners of your screen'
    screen_width, screen_height = 1920, 1080  # Replace with your screen resolution
    # Calculate the dimensions for the right half of the screen
    right_half_x = screen_width // 2 
    right_half_y = screen_height 
    right_half_width = screen_width // 2 
    right_half_height = screen_height 
    # window_name = 'Select Points'
    # Create a resizable window for the camera feed
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, right_half_x, 0)
    cv2.resizeWindow(window_name, right_half_width, right_half_height)
    cv2.setMouseCallback(window_name, store_points)
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

def display_frame(kitti_read_path,kitti_write_path,data_splits_file):
    # Path to the data splits file
    # Define the destination points (a rectangle)
    width, height = 1242, 375 #kitti 
    dst_points = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

    global selected_points, frame, is_frame_available
    selected_points = sort_coordinates(selected_points)
    print("Selected points are:",selected_points)
    # Convert the selected points to numpy array
    src_points = np.array(selected_points, dtype=np.float32)
    # Perform the homography transformation
    M, _ = cv2.findHomography(src_points, dst_points)

    # Read the data splits file
    with open(data_splits_file, 'r') as file:
        lines = file.readlines()

    # Process each image path
    for idx,line in enumerate(lines):
        image_path = line.strip().split(" ")[0]
        read_path = os.path.join(kitti_read_path,image_path)
        write_path = os.path.join(kitti_write_path,image_path)
        save_dir = os.path.dirname(write_path)
        os.makedirs(save_dir,exist_ok=True)
        # Load the RGB image

        rgb_image = cv2.imread(read_path,-1)
        rgb_image = cv2.resize(rgb_image,(width, height))
        if rgb_image is not None:
            # # Create a delay of 0.5 seconds
            # time.sleep(0.5)

            # Capture a photo through webcam and save it in the same directory structure
            screen_width, screen_height = 1920, 1080  # Replace with your screen resolution
            # Calculate the dimensions for the left half of the screen
            left_half_x = -10
            left_half_y = 0
            left_half_width = screen_width // 2
            left_half_height = screen_height

            window_name = 'Image to be captured'
            # Create a resizable window for the webcam feed
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.moveWindow(window_name, left_half_x, left_half_y)
            cv2.resizeWindow(window_name, left_half_width, left_half_height)
            cv2.putText(rgb_image,f"{idx}",(35,55), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

            # sample_image_path = "/home/vision/suraj/kitti_dataset/KITTI/2011_09_26/2011_09_26_drive_0001_sync/image_02/data/0000000000.png"
            # sample_image = cv2.imread(sample_image_path,-1)
            
            cv2.imshow(window_name,rgb_image)
            cv2.waitKey(1500)

            global frame, is_frame_available
            while not is_frame_available:
                pass 
            captured_frame = frame.copy()

            # Warp the image
            modified_frame = cv2.warpPerspective(captured_frame, M, (width, height))
            print("warped image's shape = ",modified_frame.shape)
            # Display the frame
            
            screen_width, screen_height = 1920, 1080  # Replace with your screen resolution
            # Calculate the dimensions for the right half of the screen
            right_half_x = screen_width // 2
            right_half_y = screen_height
            right_half_width = screen_width // 2
            right_half_height = screen_height
            window_name = 'Verify Captured Image'
            # Create a resizable window for the camera feed
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.moveWindow(window_name, right_half_x, 0)
            cv2.resizeWindow(window_name, right_half_width, right_half_height)
            cv2.imshow(window_name, modified_frame)
            # Check for the 'q' key to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_capture.set() 
                break

            #save image in write_path


# Start the frame capture thread
capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()

#select 4 points of the screen
select_points()

kitti_read_path = "/home/vision/suraj/kitti_dataset/KITTI"
kitti_write_path = "/home/vision/suraj/kitti_dataset/KITTI_captured_from_oak1"
data_splits_file = '/home/vision/suraj/Pixelformer_jetson/data_splits/kitti_all_data_for_data_capture_from_camera.txt'  # Replace with the actual path to your data splits file
display_frame(kitti_read_path,kitti_write_path,data_splits_file)


#perform homography 
#perform_homography()

# Wait for the frame capture thread to finish
capture_thread.join()

# Release resources
cv2.destroyAllWindows()


