## Digital Heritage app.

# ORB-SLAM2 Setup on NVIDIA Jetson AGX Xavier (For Monocular Cameras Only)
**for now, later we will do it for RGB-D cameras as well

This guide outlines the steps to set up ORB-SLAM2 on NVIDIA Jetson AGX Xavier, integrating it with NVIDIA Jetson Inference and using Pangolin for visualization.

## 1. Install Pangolin
```
git clone --recursive https://github.com/stevenlovegrove/Pangolin.git
cd Pangolin
./scripts/install_prerequisites.sh recommended
git checkout v0.6
mkdir build && cd build
cmake ..
cmake --build .
sudo make install
```
Note: Building the Python wheel is currently known to have issues and is left unaddressed for now.

## 2. Install OpenCV

Follow the instructions provided in this [blog post](https://forums.developer.nvidia.com/t/best-way-to-install-opencv-with-cuda-on-jetpack-5-xavier-nx-opencv-for-tegra/222777) for installing OpenCV with CUDA support.

## 3. Download NVIDIA Jetson Inference Repo

### 3.1 Setup Native CURL

```
git clone https://github.com/surajiitd/NVIDIA_Jetson_Inference.git
cd digital_heritage_project_demo_SLAM
cd curl-7.77.0
./configure --without-ssl
make
sudo make install
```

#### IMPORTANT NOTE: Corrections made in CMakeLists.txt
Some of the libraries and code is omitted from the build as it is meant for RGB-D cameras and not Monocular Camera so, these can be omitted for now.

Omitted Target Libraries
```
target_link_libraries(${PROJECT_NAME}
   ${OpenCV_LIBS}
   ${EIGEN3_LIBS}
   ${Pangolin_LIBRARIES}
   ${PROJECT_SOURCE_DIR}/Thirdparty/DBoW2/lib/libDBoW2.so
   ${PROJECT_SOURCE_DIR}/Thirdparty/g2o/lib/libg2o.so
   # /usr/local/lib/libdepthai-opencv.so {for RGB-D OAK-D camera}
   # /usr/local/lib/libdepthai-core.so {for RGB-D Oak-D camera}
   -lcurl 
)
```
Omitted Source Code to be Build
```
# add_executable(test
# Examples/Monocular/test.cc)
# target_link_libraries(test /home/vision/slam/depthai-core/build/libdepthai-opencv.so -lcurl ${PROJECT_NAME})
```
test.cc is for RGB-D cameras (not required for now)

### 3.2 Build ORB-SLAM2

```
cd ORB_SLAM2
chmod +x build.sh
./build.sh
```

## 4. Performing camera calibration
```
cd Examples/Camera_calibration_code
```
change to the above directory for performing the following commands.
```
python getImages.py
```
This will be used to get images of the webcam and saved as `.png` file for further processing.
```
python cameraCalibration.py
```
This will be used to perform camera calibration to find the camera matrix and distortion matrix.

NOTE: For more details on how to perform camera calibration read up on the internet for the same.

Update the appropiate `.yaml` file to change the intrinsic properties of the camera as per your setup and usecase.

## 5. To Test the Build
```
./Examples/Monocular/test_recorded Vocabulary/ORBvoc.txt Examples/Monocular/recorded_video_tools/visionLab.yaml /home/vision-agx-05/Desktop/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORBSLAM2/Examples/Monocular/recorded_video_tools/lab_data/
```
Note: Further steps regarding Python installation, Django setup, and running the server haven't been tested at the time of writing this readme.

For additional details and troubleshooting, please refer to the original documentation or repositories for each component.

### Steps to run ORBSLAM2 with app.
1. first connect jetson with same mobile's hotspot in which you want to run the app.
2. Now find the ip asigned to jetson... go to "manage devices" in your mobile hotspot and see jetson's ip. let's say it's ip is "IP". (You can do this in IIT_WIFI also if you don't want to run the app in mobile and can run in the jetson's browser itself.in that case you can use ip everywhere as 127.0.0.1 also).
3. Now update the ip in line-no. 176 in  `ORB_SLAM2/src/Viewer.cc`, (they have made changes in this file only in ORBSLAM2, they are just sending the current x,y,z,yaw to django server always, they have just added curl lines (from line no. 171 to 178)).
4. then compile ORBSLAM2 again using `./build.sh` command. (ORB_SLAM2/build.sh is the file.)
5. now go to dheritage folder in the app code. update the ip in `dheritage/dheritage/settings.py` and `dheritage/geoloc/static/script.js`. I have made a variable ip there just update that, that variable is used 3 times. 
6. Now go to dheritage home directory and run the app using `python manage.py runserver IP:8080`. No open this link in your mobile or in jetson itself. `https://IP:8080`. you'll see the app running.
7. In `dheritage/db.sqlite3`, this is the database having all marked locations, you can access it using `https://IP:8080/admin` the username pwd is `admin` and `aks123`, this pwd is wrong. ask from aakash what was it(Arka don't know that).
8. In this database you can manually change the location coordinates, add, delete locations, etc.
---
**Problem 1:**
Bug to resolve in app: while entering a location's name and pressing "mark location" button, the location is not getting added, and the app is toggled to off mode. (actually the error was happening(printing) in the orbslam terminal).  
**Problem 2:**
- App with map code was deleted due to jetson got format. and map was not updated in github code. 
- and in the new app code also, they didn't get time to complete the map part of the app, just made the frontend(html) for map, but not the js code,etc. So later from frontend also they removed the map part. So that has to be done.




### DROID-SLAM in jetson:

#### Installation: 
- In setup.py just add the compiler flags for `_87`. (or whatever is the gencode of jetson, google that).
- And to increase fps, Arka said they changed the hyperparameters in demo.py (but he was not not sure, and in negroni when we checked no changes were made there).
