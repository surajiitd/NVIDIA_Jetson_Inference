#!/bin/bash

#------------------------------------
# Monocular Examples
echo "Launching ORBSLAM3 with Pre-recorded custom dataset"
./Monocular/test_recorded ../Vocabulary/ORBvoc.txt ./Monocular/test_recorded_example.yaml ./Datasets/lab_data ./Monocular/Lab_TimeStamps/timestamps.txt 