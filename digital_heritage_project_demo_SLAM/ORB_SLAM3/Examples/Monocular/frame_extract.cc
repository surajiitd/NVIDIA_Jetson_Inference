#include <iostream>
#include <opencv2/opencv.hpp>
#include <fstream>
#include <sys/stat.h>

void createDirectory(const std::string& path) {
    // Create the directory if it doesn't exist
    if (mkdir(path.c_str(), 0777) == -1) {
        std::cerr << "Error creating directory: " << path << std::endl;
    }
}

void extractFrames(const std::string& videoPath, const std::string& outputFolder, const std::string& timestampsFile) {
    // Open the video file
    cv::VideoCapture cap(videoPath);

    // Check if the video opened successfully
    if (!cap.isOpened()) {
        std::cerr << "Error opening video file" << std::endl;
        return;
    }

    // Create the output folder if it doesn't exist
    createDirectory(outputFolder);

    // Initialize frame counter
    int frameCount = 0;

    // Initialize timestamps file
    std::ofstream timestampsStream(timestampsFile);

    // Loop through each frame in the video
    while (true) {
        // Read a frame from the video
        cv::Mat frame;
        cap >> frame;

        // Break the loop if the video has ended
        if (frame.empty()) {
            break;
        }

        // Increment frame counter
        frameCount++;

        // Save the frame as an image
        std::string frameName = outputFolder + "/" + std::to_string(frameCount) + ".png";
        cv::imwrite(frameName, frame);

        // Write timestamp to the timestamps file
        timestampsStream << frameCount << std::endl;
    }

    // Release the video capture object
    cap.release();

    std::cout << "Frames extracted and saved to " << outputFolder << std::endl;
    std::cout << "Timestamps saved to " << timestampsFile << std::endl;
}

int main(int argc, char* argv[]) {
    // Check if the correct number of command-line arguments is provided
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <video_path> <output_folder> <timestamps_file>" << std::endl;
        return 1;
    }

    // Extract video path, output folder, and timestamps file from command-line arguments
    std::string videoPath = argv[1];
    std::string outputFolder = argv[2];
    std::string timestampsFile = argv[3];

    // Call the extractFrames function with the provided video path and output folder
    extractFrames(videoPath, outputFolder, timestampsFile);

    return 0;
}