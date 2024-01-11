import cv2

# Create a VideoCapture object to read from the webcam (index 0)
cap = cv2.VideoCapture(0)

# Check if the webcam is successfully opened
if not cap.isOpened():
    print("Failed to open webcam")
    exit()

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    print(frame.shape)
    # Check if the frame was successfully read
    if not ret:
        print("Failed to read frame from webcam")
        break

    # Display the frame
    window_name = "RGB"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the VideoCapture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()

