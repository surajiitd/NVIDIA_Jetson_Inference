import cv2

def extract_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Create the output folder if it doesn't exist
    import os
    os.makedirs(output_folder, exist_ok=True)

    # Initialize frame counter
    frame_count = 0

    # Loop through each frame in the video
    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Break the loop if the video has ended
        if not ret:
            break

        # Save the frame as an image
        frame_name = f"{output_folder}/{frame_count}.png"
        cv2.imwrite(frame_name, frame)

        # Increment frame counter
        frame_count += 1

    # Release the video capture object
    cap.release()

    print(f"Frames extracted and saved to {output_folder}")

# Example usage
video_path = "sample_video_lenovo.webm"
output_folder = "lab_data/"
extract_frames(video_path, output_folder)

def generate_number_file(b, output_file):
    with open(output_file, 'w') as file:
        for number in range(b):
            file.write(str(number) + '\n')

# Example usage
b = 652
output_file = 'timestamps.txt'

generate_number_file(b, output_file)
