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

#include <opencv2/opencv.hpp>

#include <System.h>

using namespace std;

bool b_continue_session;

void exit_loop_handler(int s)
{
    cout << "Finishing session" << endl;
    b_continue_session = false;
}

int main(int argc, char **argv)
{
    if (argc < 3 || argc > 4)
    {
        cerr << endl
             << "Usage: ./test_webcam path_to_vocabulary path_to_settings (trajectory_file_name)" << endl;
        return 1;
    }

    string file_name;
    bool bFileName = false;

    if (argc == 4)
    {
        file_name = string(argv[argc - 1]);
        bFileName = true;
    }

    struct sigaction sigIntHandler;

    sigIntHandler.sa_handler = exit_loop_handler;
    sigemptyset(&sigIntHandler.sa_mask);
    sigIntHandler.sa_flags = 0;

    sigaction(SIGINT, &sigIntHandler, NULL);
    b_continue_session = true;

    cv::VideoCapture cap(0); // Open the first webcam available

    if (!cap.isOpened())
    {
        cerr << "Error: Unable to open webcam." << endl;
        return 1;
    }

    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);

    // Load SLAM system
    ORB_SLAM3::System SLAM(argv[1], argv[2], ORB_SLAM3::System::MONOCULAR, true);
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

        double timestamp_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                                  std::chrono::system_clock::now().time_since_epoch())
                                  .count();

        if (imageScale != 1.f)
        {
            int width = imCV.cols * imageScale;
            int height = imCV.rows * imageScale;
            cv::resize(imCV, imCV, cv::Size(width, height));
        }

        SLAM.TrackMonocular(imCV, timestamp_ms);
    }

    cap.release();

    // Stop all threads
    SLAM.Shutdown();

    return 0;
}