# !/bin/bash

cd /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/Examples/Monocular/Run_Scripts

# Check if the first argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <mode: {recorded, webcam2}>"
    exit 1
fi

# Perform actions based on the selected mode
if [ "$1" = "recorded" ]; then
    echo "MODE: recorded mode"
    bash test_recorded.sh
elif [ "$1" = "webcam2" ]; then
    echo "MODE: webcam2 mode"
    bash test_webcam_2.sh
else
    echo "Invalid mode: $1"
    exit 1
fi