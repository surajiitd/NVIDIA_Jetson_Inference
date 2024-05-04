#!/bin/bash

echo "ORB_SLAM3" | figlet

cd ../

sequenceNumber=$1

settingsFileName='KITTI'$sequenceNumber'.yaml'
settingsDirectory='Setup_Files/'$settingsFileName

DatasetFolderName='kitti_'$sequenceNumber
DatasetDirectory='../Datasets/RGB-D/Kitti/'$DatasetFolderName

trajectoryFileName=$DatasetFolderName

echo "settings directory = $settingsDirectory"
echo "dataset directory = $DatasetDirectory"

./p-rgbd_kitti ../../Vocabulary/ORBvoc.txt $settingsDirectory $DatasetDirectory $trajectoryFileName