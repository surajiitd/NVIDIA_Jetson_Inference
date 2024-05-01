#!/bin/bash

echo "ORB_SLAM3" | figlet

settingFiles=$1
datasetFolder=$2

cd ../
./p-rgbd_kitti ../../Vocabulary/ORBvoc.txt Setup_Files/$settingFiles.yaml ../Datasets/RGB-D/$datasetFolder $datasetFolder