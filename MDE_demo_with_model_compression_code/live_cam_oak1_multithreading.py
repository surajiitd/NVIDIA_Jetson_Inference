import cv2
import depthai
import threading

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
    cam.setResolution(depthai.ColorCameraProperties.SensorResolution.THE_4_K) 
    #cam.initialControl.setManualFocus(140) # 0..255 (larger for near objects) 
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
            
            if in_rgb is not None:
                # Convert the NV12 format to BGR
                frame = in_rgb.getCvFrame()

                # Set the flag to indicate that a new frame is available
                is_frame_available = True

# Function to continuously display frames
def display_frames():
    global frame, is_frame_available
    flag = True
    

    while True:
        # Wait for a new frame to be available
        while not is_frame_available:
            pass

        # Display the frame
        window_name = "RGB"
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, frame)
        if flag:
            print(frame.shape)
            flag = False
        

        # Reset the flag
        is_frame_available = False

        # Check for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("input_image.jpg",frame)
            stop_capture.set()  # Set the stop signal
            break

# Start the frame capture thread
capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()

# Start the frame display thread
display_frames()

# Wait for the frame capture thread to finish
capture_thread.join()

# Close the OpenCV windows
cv2.destroyAllWindows()
