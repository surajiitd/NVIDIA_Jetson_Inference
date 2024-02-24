#!/bin/bash

# change these variable(s) accordingly
timeStampFileName='timestamps.txt'
DatasetFolderName='lab_data'
#------------------------------------
# Monocular Examples
echo "ORB_SLAM3" | figlet
echo "Launching ORB_SLAM3 with Pre-recorded custom dataset"
../test_recorded ../../../Vocabulary/ORBvoc.txt ../Setup_Files/test_recorded_example.yaml ../../Datasets/"$DatasetFolderName" ../Datasets_TimeStamps/Lab_TimeStamps/"$timeStampFileName"  dataset-Recorded_mono

# chmod +x plot_pose_data.py
# python plot_pose_data.py

# evo_traj tum ../CameraTrajectory/EuRoC_f_dataset-Recorded_mono.txt --plot