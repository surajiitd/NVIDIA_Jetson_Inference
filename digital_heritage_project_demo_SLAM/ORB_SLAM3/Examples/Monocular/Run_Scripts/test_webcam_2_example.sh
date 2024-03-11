#!/bin/bash

# change these variable(s) accordingly
timeStampFileName='timestamps'
checkpointLogFileName='checkpointLog.txt'
DatasetFolderName='custom_data'

#------------------------------------
# Monocular Examples
echo "ORB_SLAM3" | figlet
echo "Launching ORBSLAM3 with Monocular sensor"
../test_webcam_2 ../../../Vocabulary/ORBvoc.txt ../Setup_Files/test_webcam_2_example.yaml ../../Datasets/"$DatasetFolderName" ../Datasets_TimeStamps/Lab_TimeStamps/"$timeStampFileName"  ../../../"$checkpointLogFileName" dataset-webcam_mono