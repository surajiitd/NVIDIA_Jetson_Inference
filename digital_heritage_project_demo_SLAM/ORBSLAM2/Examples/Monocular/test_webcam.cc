/**
 * This file is part of ORB-SLAM2.
 *
 * Copyright (C) 2014-2016 Raúl Mur-Artal <raulmur at unizar dot es> (University of Zaragoza)
 * For more information see <https://github.com/raulmur/ORB_SLAM2>
 *
 * ORB-SLAM2 is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * ORB-SLAM2 is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with ORB-SLAM2. If not, see <http://www.gnu.org/licenses/>.
 */

#include <iostream>
#include <algorithm>
#include <fstream>
#include <chrono>

#include <opencv2/core/core.hpp>

#include <System.h>

#ifdef _WIN32
// Windows-specific headers
#include <conio.h> // For _kbhit and _getch
#elif defined(__unix__)
// Unix-based system specific headers
#include <unistd.h> // For read
#endif

using namespace std;

// Function to handle keyboard input
void keyboardInputHandler(bool &stopFlag)
{
    while (!stopFlag)
    {
// Check if a key is pressed
#ifdef _WIN32
        // Windows
        if (_kbhit())
        {
            char key = _getch();
            if (key == 'q')
            { // Press 'q' to set the stop flag
                stopFlag = true;
            }
        }
#elif defined(__unix__)
        // Unix-based systems
        char key;
        if (read(STDIN_FILENO, &key, 1) != -1)
        {
            if (key == 'q')
            { // Press 'q' to set the stop flag
                stopFlag = true;
            }
        }
#endif

        // Add a small delay to reduce CPU usage
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

#define _WEBCAM_BUILD_

int main(int argc, char **argv)
{
#ifdef _WEBCAM_BUILD_
    if (argc != 3)
    {
        cerr << endl
             << "argc:" << argc << "!= 3" << endl;
    }

    bool stopFlag = false;

    // Create a thread for keyboard input handling
    std::thread inputThread(keyboardInputHandler, std::ref(stopFlag));

    cv::VideoCapture cap(0);

    if (!cap.isOpened())
    {
        cerr << endl
             << "Could not open camera feed." << endl;
        return -1;
    }

    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);

    ORB_SLAM2::System SLAM(argv[1], argv[2], ORB_SLAM2::System::MONOCULAR, true);
    cout << endl
         << "-------" << endl;
    cout << "Start processing sequence ..." << endl;

#ifdef COMPILEDWITHC11
    std::chrono::steady_clock::time_point initT = std::chrono::steady_clock::now();
#else
    std::chrono::steady_clock::time_point initT = std::chrono::steady_clock::now();
#endif

    // Main loop
    while (!stopFlag)
    {
        // Create a new Mat
        cv::Mat frame;

        // Send the captured frame to the new Mat
        cap >> frame;

        if (frame.empty())
            break;

#ifdef COMPILEDWITHC11
        std::chrono::steady_clock::time_point nowT = std::chrono::steady_clock::now();
#else
        std::chrono::steady_clock::time_point nowT = std::chrono::steady_clock::now();
#endif

        // Pass the image to the SLAM system
        SLAM.TrackMonocular(frame, std::chrono::duration_cast<std::chrono::duration<double>>(nowT - initT).count());
    }

    // Join the input thread
    inputThread.join();

    // Stop all threads
    SLAM.Shutdown();

    // slam->SaveSeperateKeyFrameTrajectoryTUM("KeyFrameTrajectory-1.txt", "KeyFrameTrajectory-2.txt", "KeyFrameTrajectory-3.txt");
    SLAM.SaveMapPoints("MapPointsSave.txt");
    SLAM.SaveKeyFrameTrajectoryTUM("KeyFrameTrajectory.txt");
#endif
    return 0;
}