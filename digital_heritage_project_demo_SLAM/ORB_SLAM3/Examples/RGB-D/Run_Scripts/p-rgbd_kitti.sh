#!/bin/bash

echo "ORB_SLAM3" | figlet
echo "running pseudo rgbd in kitti"

cd ../

sequenceNumber=$1

settingsFileName='KITTI'$sequenceNumber'.yaml'
settingsDirectory='Setup_Files/'$settingsFileName

DatasetFolderName='kitti_'$sequenceNumber
DatasetDirectory='../Datasets/Kitti/'$DatasetFolderName

trajectoryFileName=$DatasetFolderName

echo "settings directory = $settingsDirectory"
echo "dataset directory = $DatasetDirectory"

./p-rgbd_kitti ../../Vocabulary/ORBvoc.txt $settingsDirectory $DatasetDirectory $trajectoryFileName