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

if [ "$localizationMode" -eq 0 ]; then
    trajectoryFileName='dataset-Hostel_Map'
    timeStampFileName='timestamps'
    DatasetFolderName='custom_data'

    ../test_webcam_2 ../../../Vocabulary/ORBvoc.txt "$settingsDirectory" ../../Datasets/"$DatasetFolderName" ../Datasets_TimeStamps/Lab_TimeStamps/"$timeStampFileName" "$trajectoryFileName"
elif [ "$localizationMode" -eq 1 ]; then
    ../test_webcam_2 ../../../Vocabulary/ORBvoc.txt "$settingsDirectory"
else
    echo "Invalid localization mode"
    exit 1
fi

#------------------------------------
# Monocular Examples
echo "Launching ORB_SLAM3 with Monocular sensor"