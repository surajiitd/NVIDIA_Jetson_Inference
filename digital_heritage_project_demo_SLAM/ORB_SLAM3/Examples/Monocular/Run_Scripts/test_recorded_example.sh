#!/bin/bash

echo "ORB_SLAM3" | figlet

# filename="../../../checkpointLog.txt"  # Specify your filename here

# # Check if the file exists
# if [ -f "$filename" ]; then
#     checkpoint=$(head -n 1 "$filename")
#     echo "First line of $filename: $checkpoint"
# else
#     echo "File $filename does not exist."
# fi

# checkpoint="${checkpoint%%,*}"

# echo "checkpoint = $checkpoint"

# Function to read YAML file
read_yaml() {
    local yaml_file="$1"
    local key="$2"
    grep "$key:" "$yaml_file" | awk -F ': ' '{print $2}'
}

# Example usage
yaml_file="../Setup_Files/test_recorded_example.yaml"
key="checkpoint"
checkpoint=$(read_yaml "$yaml_file" "$key")
echo "Value of $key is: $checkpoint"

# change these variable(s) accordingly
# timeStampFileName='timestamps.txt'
# DatasetFolderName='custom_data'

# timeStampFileName='timestamps_IITD_campus_failed.txt'
# DatasetFolderName='custom_data_IITD_campus_failed'

timeStampFileName='timestamps_'$checkpoint'.txt'
DatasetFolderName='custom_data_'$checkpoint

#------------------------------------
# Monocular Examples
echo "Launching ORB_SLAM3 with Pre-recorded custom dataset"
../test_recorded ../../../Vocabulary/ORBvoc.txt ../Setup_Files/test_recorded_example.yaml ../../Datasets/"$DatasetFolderName" ../Datasets_TimeStamps/Lab_TimeStamps/"$timeStampFileName"  dataset-Hostel_Map "$checkpoint" 

# chmod +x plot_pose_data.py
# python plot_pose_data.py

# evo_traj tum ../CameraTrajectory/EuRoC_f_dataset-Recorded_mono.txt --plot
