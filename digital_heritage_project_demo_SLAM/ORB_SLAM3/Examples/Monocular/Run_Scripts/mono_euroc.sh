#!/bin/bash
echo "EuRoC ORB_SLAM3" | figlet

cd ../

sequenceNumber=$1

settingsFileName='EuRoC.yaml'
settingsDirectory='Setup_Files/'$settingsFileName

DatasetFolderName=$sequenceNumber
DatasetDirectory='../Datasets/EuRoC/'$DatasetFolderName

timeStampFileName=$sequenceNumber'.txt'
timeStampDirectory='../Datasets/EuRoC/EuRoC_TimeStamps/'$timeStampFileName

trajectoryFileName=$sequenceNumber

echo "settings directory = $settingsDirectory"
echo "dataset directory = $DatasetDirectory"
echo "timestamp directory = $timeStampDirectory"

#------------------------------------
# Monocular Examples
echo "Launching $sequenceNumber with Monocular sensor"

./mono_euroc ../../Vocabulary/ORBvoc.txt $settingsDirectory $DatasetDirectory $timeStampDirectory $trajectoryFileName