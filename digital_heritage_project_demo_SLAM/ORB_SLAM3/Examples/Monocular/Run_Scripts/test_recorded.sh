#!/bin/bash

echo "ORB_SLAM3" | figlet

# Function to read YAML file
read_yaml() {
    local yaml_file="$1"
    local key="$2"
    grep "$key:" "$yaml_file" | awk -F ': ' '{print $2}'
}

settingsFileName='test_recorded.yaml'
trajectoryFileName='dataset-Hostel_Map'

# change these variable(s) accordingly
# timeStampFileName='timestamps.txt'
# DatasetFolderName='custom_data'

# timeStampFileName='timestamps_IITD_campus_failed.txt'
# DatasetFolderName='custom_data_IITD_campus_failed'

settingsDirectory="../Setup_Files/"$settingsFileName
checkpoint=$(read_yaml "$settingsDirectory" checkpoint)
echo "Value of $key is: $checkpoint"

timeStampFileName='timestamps_'$checkpoint'.txt'
DatasetFolderName='custom_data_'$checkpoint

#------------------------------------
# Monocular Examples
echo "Launching ORB_SLAM3 with Pre-recorded custom dataset"

../test_recorded ../../../Vocabulary/ORBvoc.txt $settingsDirectory ../../Datasets/"$DatasetFolderName" ../Datasets_TimeStamps/Lab_TimeStamps/"$timeStampFileName" "$checkpoint" "$trajectoryFileName"

# chmod +x plot_pose_data.py
# python plot_pose_data.py

# evo_traj tum ../CameraTrajectory/EuRoC_f_$trajectoryFileName.txt --plot
