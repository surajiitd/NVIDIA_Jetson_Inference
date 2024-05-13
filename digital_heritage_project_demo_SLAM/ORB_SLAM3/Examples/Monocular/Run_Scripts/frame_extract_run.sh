#!/bin/bash

# change these variable(s) accordingly
videoFileName='IITD_campus_failed.mp4'
timeStampFileName='timestamps_IITD_campus_failed.txt'
DatasetFolderName='custom_data_IITD_campus_failed'
#------------------------------------
# Monocular Examples
echo "frame_extract" | figlet
echo "Launching frame_extract.cc"
../frame_extract ../../Datasets/"$videoFileName" ../../Datasets/"$DatasetFolderName"/ ../Datasets_TimeStamps/Lab_TimeStamps/"$timeStampFileName"