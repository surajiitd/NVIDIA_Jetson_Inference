import cv2
import numpy as np
import depthai
import threading
import sys

# Global variables
selected_points = []
completed = False
# Global variables
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



def select_points():
    # Create a window and set the mouse callback
    # cv2.namedWindow('Select Points', cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty('Select Points', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    screen_width, screen_height = 1920, 1080  # Replace with your screen resolution
    # Calculate the dimensions for the right half of the screen
    right_half_x = screen_width // 2
    right_half_y = screen_height
    right_half_width = screen_width // 2
    right_half_height = screen_height

    # Create a resizable window for the camera feed
    cv2.namedWindow('Select Points', cv2.WINDOW_NORMAL)
    cv2.moveWindow('Select Points', right_half_x, 0)
    cv2.resizeWindow('Select Points', right_half_width, right_half_height)
    cv2.setMouseCallback('Select Points', store_points)
    global selected_points
    # Instructions
    print("Please select 4 corner points of the rectangular screen.")
    while True:
        
        while not is_frame_available:
            pass
        #img = frame.copy()

        # Draw a circle to mark the selected point
        for (x,y) in selected_points:
            cv2.circle(frame, (x, y), 9, (0, 230, 0), -1)
        # Display the image
        cv2.imshow('Select Points', frame)
        
        # Wait for the user to select points
        if completed:
            break

        # Check for key press
        key = cv2.waitKey(1)
        if key == ord('q'):
            sys.exit(0)
            break
    cv2.destroyAllWindows()



def perform_homography():
    # Define the destination points (a rectangle)
    width, height = 1216, 352 #kitti 
    dst_points = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

    global selected_points, frame, is_frame_available
    selected_points = sort_coordinates(selected_points)
    print("Selected points are:",selected_points)
    # Convert the selected points to numpy array
    src_points = np.array(selected_points, dtype=np.float32)

    while True:

        # Wait for a new frame to be available
        while not is_frame_available:
            pass 
        modified_frame = frame.copy()
        # Perform the homography transformation
        M, _ = cv2.findHomography(src_points, dst_points)

        # Warp the image
        modified_frame = cv2.warpPerspective(modified_frame, M, (width, height))

        # Display the frame
        window_name = "Frames after Homography"
        # cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
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
        cv2.imshow(window_name, modified_frame)
        # Check for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_capture.set() 
            break





# Start the frame capture thread
capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()

#select 4 points of the screen
select_points()

#perform homography 
perform_homography()

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
