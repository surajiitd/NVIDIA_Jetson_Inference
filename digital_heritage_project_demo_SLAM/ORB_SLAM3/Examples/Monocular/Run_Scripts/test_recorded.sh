#!/bin/bash

echo "ORB_SLAM3" | figlet

cd ../

# Function to read YAML file
read_yaml() {
    local yaml_file="$1"
    local key="$2"
    grep "$key:" "$yaml_file" | awk -F ': ' '{print $2}'
}

settingsFileName='test_recorded.yaml'
settingsDirectory="Setup_Files/"$settingsFileName

checkpoint=$(read_yaml "$settingsDirectory" checkpoint)
echo "Value of checkpoint is: $checkpoint"

load_file=$(read_yaml $settingsDirectory "System.LoadAtlasFromFile")
if [ ! -z "$load_file" ]; then
    echo 1
    load_file="${load_file//\"/}"
    trajectoryFileName=$load_file"_load"
else
    save_file="${save_file//\"/}"
    save_file=$(read_yaml $settingsDirectory "System.SaveAtlasToFile")
    if [ ! -z "$save_file" ]; then
        trajectoryFileName=$save_file"_save"
    fi
fi

DatasetFolderName='custom_data_'$checkpoint
DatasetDirectory='../Datasets/Custom/'$DatasetFolderName

timeStampFileName='timestamps_'$checkpoint'.txt'
timeStampDirectory='../Datasets/Custom/Custom_TimeStamps/'$timeStampFileName

#------------------------------------
# Monocular Examples
echo "Launching ORB_SLAM3 with Pre-recorded custom dataset"

./test_recorded ../../Vocabulary/ORBvoc.txt $settingsDirectory $DatasetDirectory $timeStampDirectory $checkpoint $trajectoryFileName