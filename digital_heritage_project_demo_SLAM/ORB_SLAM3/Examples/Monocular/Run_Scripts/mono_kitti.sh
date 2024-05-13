#!/bin/bash

echo "ORB_SLAM3" | figlet
echo "running monocular in kitti"

cd ../

sequenceNumber=$1

settingsFileName='KITTI'$sequenceNumber'.yaml'
settingsDirectory='Setup_Files/'$settingsFileName

DatasetFolderName='kitti_'$sequenceNumber
DatasetDirectory='../Datasets/Kitti/'$DatasetFolderName

trajectoryFileName=$DatasetFolderName

echo "settings directory = $settingsDirectory"
echo "dataset directory = $DatasetDirectory"

./mono_kitti ../../Vocabulary/ORBvoc.txt $settingsDirectory $DatasetDirectory $trajectoryFileName