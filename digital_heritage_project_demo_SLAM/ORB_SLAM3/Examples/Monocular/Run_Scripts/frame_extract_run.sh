#!/bin/bash

# change these variable(s) accordingly
videoFileName='visionLab_v2.mp4'
timeStampFileName='timestamps.txt'
DatasetFolderName='custom_data'
#------------------------------------
# Monocular Examples
echo "frame_extract" | figlet
echo "Launching frame_extract.cc"
../frame_extract ../../Datasets/"$videoFileName" ../../Datasets/"$DatasetFolderName"/ ../Datasets_TimeStamps/Lab_TimeStamps/"$timeStampFileName"