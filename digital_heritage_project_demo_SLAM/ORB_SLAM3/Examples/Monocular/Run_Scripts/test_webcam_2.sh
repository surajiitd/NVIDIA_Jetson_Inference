#!/bin/bash

echo "ORB_SLAM3" | figlet

# Function to read YAML file
read_yaml() {
    local yaml_file="$1"
    local key="$2"
    grep "$key:" "$yaml_file" | awk -F ': ' '{print $2}'
}

# change these variable(s) accordingly
settingsFileName='test_webcam_2.yaml'
settingsDirectory="../Setup_Files/"$settingsFileName

localizationMode=$(read_yaml "$settingsDirectory" localizationMode)
echo "Value of localizationMode is: $localizationMode"

load_file=$(read_yaml $settingsDirectory "System.LoadAtlasFromFile")
if [ ! -z "$load_file" ]; then
    echo 1
    load_file="${load_file//\"/}"
    trajectoryFileName=$load_file
else
    echo 3
    save_file="${save_file//\"/}"
    save_file=$(read_yaml $settingsDirectory "System.SaveAtlasToFile")
    if [ ! -z "$save_file" ]; then
        trajectoryFileName=$save_file
    fi
fi

if [ "$localizationMode" -eq 0 ]; then
    timeStampFileName='timestamps'
    DatasetFolderName='custom_data'

    ../test_webcam_2 ../../../Vocabulary/ORBvoc.txt "$settingsDirectory" ../../Datasets/"$DatasetFolderName" ../Datasets_TimeStamps/Lab_TimeStamps/"$timeStampFileName" "$trajectoryFileName"
elif [ "$localizationMode" -eq 1 ]; then
    ../test_webcam_2 ../../../Vocabulary/ORBvoc.txt "$settingsDirectory" "$trajectoryFileName"
else
    echo "Invalid localization mode"
    exit 1
fi

#------------------------------------
# Monocular Examples
echo "Launching ORB_SLAM3 with Monocular sensor"