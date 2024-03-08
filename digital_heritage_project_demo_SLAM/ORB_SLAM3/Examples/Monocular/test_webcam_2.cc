#include <stdlib.h>
#include <iostream>
#include <algorithm>
#include <fstream>
#include <chrono>
#include <ctime>
#include <sstream>
#include <thread>

#include <condition_variable>
#include <signal.h>
#include <sys/stat.h>

#include <opencv2/opencv.hpp>

#include <System.h>

using namespace std;

bool b_continue_session;

void createDirectory(const std::string &path)
{
    // Create the directory if it doesn't exist
    if (mkdir(path.c_str(), 0777) == -1)
    {
        std::cerr << "Error creating directory: " << path << std::endl;
    }
}

void exit_loop_handler(int s)
{
    cout << "Finishing session" << endl;
    b_continue_session = false;
}

int main(int argc, char **argv)
{
    if (argc < 6)
    {
        cerr << endl
             << "Usage: path_to_example_code/test_webcam path_to_vocabulary path_to_settings path_to_saving_sequence_folder_1 path_to_times_file_1 (trajectory_file_name)" << endl;
        return 1;
    }

    string file_name;
    bool bFileName = false;
    bool showGUI = true;

    if (bFileName)
    {
        file_name = string(argv[argc - 1]);
        cout << "file name: " << file_name << endl;
    }

    struct sigaction sigIntHandler;

    sigIntHandler.sa_handler = exit_loop_handler;
    sigemptyset(&sigIntHandler.sa_mask);
    sigIntHandler.sa_flags = 0;

    sigaction(SIGINT, &sigIntHandler, NULL);
    b_continue_session = true;

    // cv::VideoCapture cap(0); // Open the first webcam available
    cv::VideoCapture cap("http://192.168.29.81:8000/camera/mjpeg");

    if (!cap.isOpened())
    {
        cerr << "Error: Unable to open webcam." << endl;
        return 1;
    }

    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);

    std::string outputFolder = argv[2];
    std::string timestampsFile = argv[3];

    // Creating outFolder directory
    createDirectory(outputFolder);

    // Initialize timestamps file
    std::ofstream timestampsStream(timestampsFile);

    // Load SLAM system
    ORB_SLAM3::System SLAM(argv[1], argv[2], ORB_SLAM3::System::MONOCULAR, showGUI);
    float imageScale = SLAM.GetImageScale();

    cv::Mat imCV;

    while (b_continue_session)
    {
        cap >> imCV; // Capture frame from webcam

        if (imCV.empty())
        {
            cerr << "Error: Unable to capture frame from webcam." << endl;
            break;
        }

        double timestamp_ms = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();

        if (imageScale != 1.f)
        {
            int width = imCV.cols * imageScale;
            int height = imCV.rows * imageScale;
            cv::resize(imCV, imCV, cv::Size(width, height));
        }

        std::string frameName = outputFolder + "/" + std::to_string(timestamp_ms) + ".png";
        cv::imwrite(frameName, imCV);

        SLAM.TrackMonocular(imCV, timestamp_ms);
    }

    cap.release();

    std::cout << "Frames extracted and saved to " << outputFolder << std::endl;
    std::cout << "Timestamps saved to " << timestampsFile << std::endl;

    // Stop all threads
    SLAM.Shutdown();

    return 0;
}