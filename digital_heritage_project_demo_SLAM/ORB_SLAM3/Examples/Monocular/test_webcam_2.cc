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

#include <limits>
#include <iomanip>

using namespace std;

bool b_continue_session;

std::time_t checkpoint;
bool performPost;
std::string url;

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
    cv::FileStorage fs(argv[2], cv::FileStorage::READ);
    if (!fs.isOpened())
    {
        std::cerr << "Failed to open YAML file." << std::endl;
        return 1;
    }

    bool localizationMode;
    fs["localizationMode"] >> localizationMode;

    if (!localizationMode && argc == 5)
    {
        cerr << endl
             << "Usage: path_to_examples/test_webcam path_to_vocabulary path_to_settings path_to_saving_sequence_folder_1 path_to_times_file_1 path_to_checkpoint_log_file (trajectory_file_name)" << endl;
        return 1;
    }

    else if (localizationMode && argc == 2)
    {
        cerr << endl
             << "Usage: ./test_webcam path_to_vocabulary path_to_settings" << endl;
        return 1;
    }

    std::string executableFileName(argv[0]);

    bool showGUI;
    fs["showGUI"] >> showGUI;
    std::cout << "**(" << executableFileName << ") "
              << "showGUI = " << showGUI << std::endl;

    fs["performPost"] >> performPost;
    std::cout << "**(" << executableFileName << ") "
              << "performPost = " << performPost << std::endl;

    if (performPost)
    {
        std::string hostip;
        std::string portNum;
        fs["hostip"] >> hostip;
        fs["portNum"] >> portNum;

        std::cout << "**(" << executableFileName << ") "
                  << "Host Address = " << hostip << ":" << portNum << endl;

        url = "http://" + hostip + ":" + portNum + "/updatecurrent/";

        std::cout << "**(" << executableFileName << ") "
                  << "Post API Endpoint = " << url << std::endl;
    }

    struct sigaction sigIntHandler;

    sigIntHandler.sa_handler = exit_loop_handler;
    sigemptyset(&sigIntHandler.sa_mask);
    sigIntHandler.sa_flags = 0;

    sigaction(SIGINT, &sigIntHandler, NULL);
    b_continue_session = true;

    cv::VideoCapture cap("http://192.168.29.81:8000/camera/mjpeg");
    // cv::VideoCapture cap("http://10.194.18.91:8000/camera/mjpeg");

    // int cameraCap;
    // fs["Camera.cap"] >> cameraCap;
    // std::cout << "Camera.cap = " << cameraCap << std::endl;
    // cv::VideoCapture cap(cameraCap);

    if (!cap.isOpened())
    {
        cerr << "Error: Unable to open webcam." << endl;
        return 1;
    }

    int fps;
    fs["Camera.fps"] >> fps;
    std::cout << "Camera.fps = " << fps << std::endl;

    int width, height;
    fs["Camera.width"] >> width;
    fs["Camera.height"] >> height;
    std::cout << "Camera.width = " << width << std::endl;
    std::cout << "Camera.height = " << height << std::endl;

    cap.set(cv::CAP_PROP_FRAME_WIDTH, width);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, height);
    cap.set(cv::CAP_PROP_FPS, fps);

    // Load SLAM system
    ORB_SLAM3::System SLAM(argv[1], argv[2], ORB_SLAM3::System::MONOCULAR, showGUI);
    float imageScale = SLAM.GetImageScale();

    if (localizationMode) {
        cv::Mat imCV;

        while (b_continue_session)
        {
            cap >> imCV; // Capture frame from webcam

            if (imCV.empty())
            {
                cerr << "Error: Unable to capture frame from webcam." << endl;
                break;
            }

            unsigned long timestamp_ms = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();

            if (imageScale != 1.f)
            {
                int width = imCV.cols * imageScale;
                int height = imCV.rows * imageScale;
                cv::resize(imCV, imCV, cv::Size(width, height));
            }

            SLAM.TrackMonocular(imCV, timestamp_ms);
        }
    }
    else if (!localizationMode)
    {
        bool bFileName = true;
        string file_name;

        if (bFileName)
        {
            file_name = string(argv[argc - 1]);
            cout << "file name: " << file_name << endl;
        }
        // Get the current system time point
        auto now = std::chrono::system_clock::now();

        // Convert the time point to a time_t object
        std::time_t now_time = std::chrono::system_clock::to_time_t(now);
        checkpoint = now_time;

        // Print the current date and time
        std::cout << "############# Checkpoint test_webcam_2.cc ###############" << std::endl;
        std::cout << "Now date and time: " << std::to_string(checkpoint) << std::endl;  // long to string
        std::cout << "Current date and time: " << std::ctime(&checkpoint) << std::endl; // long to time format

        std::string outputFolder = argv[3];
        outputFolder += "_" + std::to_string(checkpoint);
        std::string timestampsFile = argv[4];
        timestampsFile += "_" + std::to_string(checkpoint) + ".txt";

        // Creating outFolder directory
        createDirectory(outputFolder);

        // Initialize timestamps file
        std::ofstream timestampsStream(timestampsFile);

        cv::Mat imCV;

        while (b_continue_session)
        {
            cap >> imCV; // Capture frame from webcam

            if (imCV.empty())
            {
                cerr << "Error: Unable to capture frame from webcam." << endl;
                break;
            }

            unsigned long timestamp_ms = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();

            if (imageScale != 1.f)
            {
                int width = imCV.cols * imageScale;
                int height = imCV.rows * imageScale;
                cv::resize(imCV, imCV, cv::Size(width, height));
            }

            // Save the frame as an image
            std::string frameName = outputFolder + "/" + std::to_string(timestamp_ms) + ".png";
            cv::imwrite(frameName, imCV);

            // Write timestamp to the timestamps file
            // timestampsStream << timestamp_ms << std::endl;
            timestampsStream << std::fixed << std::setprecision(6) << timestamp_ms << std::endl;

            SLAM.TrackMonocular(imCV, timestamp_ms);
        }

        std::cout << "Frames extracted and saved to " << outputFolder << std::endl;
        std::cout << "Timestamps saved to " << timestampsFile << std::endl;

    }

    // Stop all threads
    cap.release();

    SLAM.Shutdown();

    return 0;
}