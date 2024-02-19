#!/bin/bash

# change these variable(s) accordingly
timeStampFileName='timestamps.txt'
DatasetFolderName='lab_data'
#------------------------------------
# Monocular Examples
echo "ORB_SLAM3" | figlet
echo "Launching ORB_SLAM3 with Pre-recorded custom dataset"
../test_recorded ../../../Vocabulary/ORBvoc.txt ../Setup_Files/test_recorded_example.yaml ../../Datasets/"$DatasetFolderName" ../TimeStamps/Lab_TimeStamps/"$timeStampFileName"  dataset-Recorded_mono