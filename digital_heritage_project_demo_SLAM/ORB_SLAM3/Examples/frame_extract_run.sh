#!/bin/bash

# change these variable(s) accordingly
videoName='WIN_20240218_16_50_41_Pro.mp4'
#------------------------------------
# Monocular Examples
echo "Launching frame_extract.cc"
./Monocular/frame_extract ./Datasets/"$videoName" ./Datasets/lab_data ./Monocular/Lab_TimeStamps/timestamps.txt 