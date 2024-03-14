#!/bin/bash

echo "ORB_SLAM3" | figlet

filename="../../../checkpointLog.txt"  # Specify your filename here

# Check if the file exists
if [ -f "$filename" ]; then
    checkpoint=$(head -n 1 "$filename")
    echo "First line of $filename: $checkpoint"
else
    echo "File $filename does not exist."
fi

checkpoint="${checkpoint%%,*}"

echo "checkpoint = $checkpoint"

# change these variable(s) accordingly
# timeStampFileName='timestamps.txt'
# DatasetFolderName='custom_data'
timeStampFileName='timestamps_'$checkpoint'.txt'
DatasetFolderName='custom_data_'$checkpoint

#------------------------------------
# Monocular Examples
echo "Launching ORB_SLAM3 with Pre-recorded custom dataset"
../test_recorded ../../../Vocabulary/ORBvoc.txt ../Setup_Files/test_recorded_example.yaml ../../Datasets/"$DatasetFolderName" ../Datasets_TimeStamps/Lab_TimeStamps/"$timeStampFileName"  dataset-Recorded_mono 

# chmod +x plot_pose_data.py
# python plot_pose_data.py

# evo_traj tum ../CameraTrajectory/EuRoC_f_dataset-Recorded_mono.txt --plot
