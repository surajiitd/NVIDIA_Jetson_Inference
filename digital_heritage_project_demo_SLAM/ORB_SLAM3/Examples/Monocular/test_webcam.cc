#include <stdlib.h>
#include <iostream>
#include <algorithm>
#include <fstream>
#include <chrono>
#include <ctime>
#include <sstream>
#include <thread>

#include <opencv2/opencv.hpp>

#include <System.h>

using namespace std;

void keyboardInputHandler(bool& stopFlag) {
    while (!stopFlag) {
        // Check if a key is pressed
        #ifdef _WIN32
            // Windows
            if (_kbhit()) {
                char key = _getch();
                if (key == 'q') { // Press 'q' to set the stop flag
                    stopFlag = true;
                }
            }
        #elif defined(__unix__)
            // Unix-based systems
            char key;
            if (read(STDIN_FILENO, &key, 1) != -1) {
                if (key == 'q') { // Press 'q' to set the stop flag
                    stopFlag = true;
                }
            }
        #endif

        // Add a small delay to reduce CPU usage
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
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

    // Start the user input thread
    bool stopFlag = false;
    std::thread inputThread(keyboardInputHandler, std::ref(stopFlag));

    while (!stopFlag)
    {
        cap >> imCV; // Capture frame from webcam

        if (imCV.empty())
        {
            cerr << "Error: Unable to capture frame from webcam." << endl;
            break;
        }

        double timestamp_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::system_clock::now().time_since_epoch()).count();

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

    // Join the user input thread to avoid termination issues
    if (inputThread.joinable()) {
        inputThread.join();
    }

    return 0;
}