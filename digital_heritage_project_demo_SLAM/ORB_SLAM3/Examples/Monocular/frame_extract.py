import cv2
import os
import sys

def extract_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Create the output folder if it doesn't exist
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

        # Increment frame counter
        frame_count += 1

        # Save the frame as an image
        frame_name = f"{output_folder}/{frame_count}.png"
        cv2.imwrite(frame_name, frame)

    # Release the video capture object
    cap.release()

    print(f"Frames extracted and saved to {output_folder}")

    return frame_count

def generate_number_file(b, output_file):
    with open(output_file, 'w') as file:
        for number in range(1, b+1):
            file.write(str(number) + '\n')

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python frame_extract.py <video_path> <output_folder>")
        sys.exit(1)

    # Extract video path and output folder from command-line arguments
    video_path = sys.argv[1]
    output_file = "timestamps.txt"
    output_folder = sys.argv[2]

    # Call the extract_frames function with the provided video path and output folder
    frame_count = extract_frames(video_path, output_folder)
    
    # Generate timestamps file
    generate_number_file(frame_count, output_file)