#!/bin/bash


# TODO: Update the commands to run for the run in new file structure

#------------------------------------
# Monocular Examples
echo "ORB_SLAM3" | figlet
echo "Launching ORBSLAM3 with Monocular sensor"
./Monocular/test_webcam_2 ../Vocabulary/ORBvoc.txt ./Monocular/test_webcam_2_example.yaml