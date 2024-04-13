# ORB_SLAM2 Setup on NVIDIA Jetson AGX Xavier (For Monocular Cameras Only) (by Aryan Singh) 

### Important Notes before starting setup.
- for now, later we will update it for RGB-D cameras as well

- the below setup was initially written for ORBSLAM_2 but, this same can work for ORB_SLAM3 as well. You may also want to go through setup instructions written my Sarvesh Thakur as some of the dependency issues are covered there as well.

- Most of the changes mentioned below is already being done so the simplest way to setup this is install all the dependencies mentioned below and run build.sh, if you encounter setup issues then try to resolve by yourself or contact one of the contributors.

This guide outlines the steps to set up ORB-SLAM2 on NVIDIA Jetson AGX Xavier, integrating it with NVIDIA Jetson Inference and using Pangolin for visualization.

There are some extra files and code present in this ORBSLAM2 repo and not present in the original ORBSLAM2 repo, so please use our ORBSLAM2 files to test build given below.

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

**NOTE**: There may be other dependencies required for building ORBSLAM2 as well. This may vary depending on the existing system one is using, so debugging may be required as per the dependencies error generated.

Look into the original [ORBSLAM2](https://github.com/raulmur/ORB_SLAM2) repo for the same.

## 3. Download NVIDIA Jetson Inference Repo
In this example we are in `~/Desktop/` directory , all commands given below are written accordingly.
### 3.1 Setup Native CURL

```bash
git clone https://github.com/surajiitd/NVIDIA_Jetson_Inference.git
cd NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM
cd curl-7.77.0
./configure --without-ssl
make
sudo make install
```

#### Corrections made in CMakeLists.txt
Some of the libraries and code is omitted from the build as it is meant for RGB-D cameras and not Monocular Camera so, these can be omitted for now.

Omitted Target Libraries
```cmake
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
```cmake
# add_executable(test
# Examples/Monocular/test.cc)
# target_link_libraries(test /home/vision/slam/depthai-core/build/libdepthai-opencv.so -lcurl ${PROJECT_NAME})
```
test.cc is for RGB-D cameras (not required for now)

### 3.2 Build ORB-SLAM2

```bash
cd ORB_SLAM2
chmod +x build.sh
./build.sh
```

## 4. Adding custom test code
for example, take `my_custom_code.cc` which is present at `<some_directory>`

It is advised to work in `Examples/Monocular` directory.

So to compile this code using cmake build process, we need to edit `CMakeLists.txt`. Here we need to add the following lines:

```cmake
add_executable(my_custom_code
<some_directory>/my_custom_code.cc)
target_link_libraries(my_custom_code ${PROJECT_NAME})
```

**NOTE**: You will need to change the name and directory in the above lines of code according to the locations where the file is saved.

## 5. Testing the new build

Now, to test our new build with the new `my_custom_code` binary as a part of the executable, run the following command.

```bash
.<some_directory>/my_custom_code Vocabulary/ORBvoc.txt <some_other_directory>/<my_camera_properties>.yaml ~/Desktop/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORBSLAM2/<some_other_directory>/lab_data/
```

You will understand the exact commands to run by running the next features mentioned in this `README.md` file

**NOTE**: For running the following programs, you need to have opencv installed in your python environment.

# Performing camera calibration
#### Run the following commands:
```bash
cd Examples/Camera_calibration_code
```

change to the above directory for performing the following commands.

```bash
python getImages.py
```

This will be used to get images of the webcam and saved as `.png` file for further processing.
```bash
python cameraCalibration.py
```
This will be used to perform camera calibration to find the camera matrix and distortion matrix.

**NOTE**: For more details on how to perform camera calibration read up on the internet for the same.

Update the appropiate `.yaml` file to change the intrinsic properties of the camera as per your setup and usecase.

# Running ORBSLAM2 on recorded video

1. Record a video using any webcam software and save it at `Examples/Monocular/Recorded_Video_Setup/` directory.

2. Then run the below commands.

```bash
cd Examples/Monocular/Recorded_Video_Setup
python frame_extract.py <video_file> lab_data
```

In our repo we have provided a sample video `sample_video_lenovo.webm`, to use this run the following command.

```bash
cd Examples/Monocular/Recorded_Video_Setup
python frame_extract.py sample_video_lenovo.webm lab_data
```

Now, you could see that under `lab_data/` folder there are frames snapshots starting from `1.png`, `2.png`, . . . as per the length and frame rate at which the video was recorded. 

3. Update `visionLab.yaml` file using the camera and distortion matrix generated by camera calibration python code.

4. Now to run ORBSLAM2 with our own generated sequence folder, run the following command:

```bash
./Examples/Monocular/test_recorded Vocabulary/ORBvoc.txt Examples/Monocular/Recorded_Video_Setup/visionLab.yaml ~/Desktop/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORBSLAM2/Examples/Monocular/Recorded_Video_Setup/lab_data/
```

This uses `test_recorded.cc` to load the frames one by one and pass it on to ORBSLAM2 threads for further processing.

`test_recorded.cc` is authored by the contributors of this repo and is not the part of original documentation.

# Running ORBSLAM2 in Real Time using monocular webcam

1. Connect a monocular webcam to the compute unit.

2. Perform camera calibration as given above.

3. Goto to the following directory.

```bash
cd Examples/Monocular/Webcam_ORBSLAM_setup
```

4. Update `visionLab.yaml` file using the camera and distortion matrix generated by camera calibration python code.

5. Now run the following commands.

```bash
./Examples/Monocular/test_webcam Vocabulary/ORBvoc.txt Examples/Monocular/Webcam_ORBSLAM_setup/visionLab.yaml 
```

`test_webcam.cc` is used for taking capturing frames from webcam and is passed to ORBSLAM for further processing.

`test_webcam.cc` is authored by the contributors of this repo and is not the part of original documentation.

# Running ORBSLAM2 through Remote Access
This feature will be useful when we will make a portable setup using a monocular webcam and jetson agx orin compute device.

**NOTE**:
- Both devices needs to be connect to a common network for ssh to work.
- If you are using `IITD_WIFI`, then make sure both devices are connected using the same uid and password.

#### Setup for Jetson AGX Orin

1. Before starting with setup we need to know the **hostname** and **inet address** under `wlan0`, so run the following commands in your compute device:

```bash
ifconfig && whoami
```

```bash
wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.194.14.38  netmask 255.255.224.0  broadcast 10.194.31.255
        inet6 2001:df4:e000:3fc1:ae76:c4b:d8d5:98b2  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::3f7b:e7c0:3bef:a04  prefixlen 64  scopeid 0x20<link>
        inet6 2001:df4:e000:3fc1:d2e5:2507:10ab:fa66  prefixlen 64  scopeid 0x0<global>
        ether cc:47:40:6f:c5:8b  txqueuelen 1000  (Ethernet)
        RX packets 9807  bytes 175798861 (175.7 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 15857  bytes 3801126999 (3.8 GB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vision-agx-05
```

in our case its inet = `10.194.14.38` and hostname = `vision-agx-05`.

2. Check whether `X11Forwarding` is enabled in ssh config file.

```bash
sudo cat /etc/ssh/sshd_config | grep X11Forwarding
```

If the output you get is the following,
```bash
X11Forwarding yes
```
then its is enabled and you can go ahead.

If not then please edit the `sshd_config` file using the below command.
```bash
sudo nano /etc/ssh/sshd_config
```

#### Instruction for Linux Desktop Client:
1. We will ssh using OPENSSH, run the following commands:

```bash
ssh hostname@<inet address> -X 
```

in our case,
```bash
ssh vision-agx-05@10.194.14.38 -X
```

`-X` is for allowing X11 forwarding for GUI interface

#### Instruction for Windows Desktop Client:
1. Install [Putty](https://putty.org) and [VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/).

2. Go to the Windows Client device and Open Putty.

3. Check and fill the following fields.

![image](https://github.com/surajiitd/NVIDIA_Jetson_Inference/assets/63505435/5c43c36a-9446-47b1-97b7-67cd48f8755a) <br>
![image](https://github.com/surajiitd/NVIDIA_Jetson_Inference/assets/63505435/b4f1bc3a-84b0-4ae3-9f30-42dbc3e7bf14) <br>
![image](https://github.com/surajiitd/NVIDIA_Jetson_Inference/assets/63505435/9b6ac974-86be-45db-91b0-0b45f0d1bf30) <br>

4. Save this configuration for loading this later whenever we need it and click to open to start ssh.

5. Open Windows X server using XLaunch and configure as below.

![image](https://github.com/surajiitd/NVIDIA_Jetson_Inference/assets/63505435/14aa1a58-a7b7-4c89-aa46-5dd08cae2fae) <br>
![image](https://github.com/surajiitd/NVIDIA_Jetson_Inference/assets/63505435/aa4e8d15-000b-44ae-82b4-659e5bf4485e) <br>
![image](https://github.com/surajiitd/NVIDIA_Jetson_Inference/assets/63505435/e4933be5-4ed8-4ff4-9a58-1f7f85543ba5) <br>
![image](https://github.com/surajiitd/NVIDIA_Jetson_Inference/assets/63505435/76039b80-3ccc-4183-b9e4-2bf076eff0ca) <br>

Now X server has started in the background.

6. In the Putty SSH terminal we can run the commands for running ORBSLAM2 with Monocular webcam as given above. New Windows will be formed when command is executed. There will be some latency in the update of frame which is expected as it's a SSH connection.

**NOTE**: 

- It is advised to build ORBSLAM2 before running the above command as the already existing binaries may or may not work.

- Further steps regarding Python installation, Django setup, and running the server haven't been tested at the time of writing this readme.

For additional details and troubleshooting, please refer to the, code, original documentation or repositories for each component.

In case of query regarding this repo please contact the following contributors:
- [Aryan Singh](https://github.com/build-error)
- [Sarvesh Thakur](https://github.com/ThakurSarveshGit)
- [Suraj Patni](https://github.com/surajiitd)

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

OS: Ubuntu 20.04


1. Pangolin Installation:
	# Get Pangolin
	cd ~/your_fav_code_directory
	git clone --recursive https://github.com/stevenlovegrove/Pangolin.git
	cd Pangolin
	
	# Get CMAKE
	sudo apt-get install build-essential --yes
	sudo apt install cmake --yes
	
	# Catch2 Installation
	$ cd ..
	$ git clone https://github.com/catchorg/Catch2.git -b v2.13.4
	$ cd Catch2
	$ cmake -Bbuild -H. -DBUILD_TESTING=OFF
	$ sudo cmake --build build/ --target install 

	# Install dependencies (as described above, or your preferred method)
	
	# Run Dependency script provided in Pangolin Repository:
		./scripts/install_prerequisites.sh recommended
			This command gives false error of not finding catch2.
			catch2 is installed and its path is in the home directory.
			Hence build manually
			
			[This might give error about other packages not found like:
				1. Eigen3
				2. OpenGL
				3. GLEW
			This was supposed to be installed by install_prerequisties.sh but rather we will do it manually]
		
	# If you face errors in above step, then run:
		# Install Eigen3
		sudo apt install libeigen3-dev
		
		# Install OpenGL
		sudo apt install freeglut3-dev --yes
		
		# Install GLEW
		sudo apt install libglew-dev --yes
		
		# Install BOOST
		sudo apt install libboost-all-dev
		
		# Install OpenSSL
		sudo apt install build-essential checkinstall zlib1g-dev -y
		sudo apt-get install libssl-dev
		
		# Build
		mkdir build
		cd build
		cmake ..
		sudo make install
		

		# Configure and build
		cmake -B build
		cmake --build build

		# with Ninja for faster builds (sudo apt install ninja-build)
		cmake -B build -GNinja
		cmake --build build

		# This does not run, but since it is a python package, leaving it for now.
		cmake --build build -t pypangolin_pip_install

		# Run me some tests! (Requires Catch2 which must be manually installed on Ubuntu.)
		cmake -B build -G Ninja -D BUILD_TESTS=ON
		cmake --build build
		cd build
		ctest
		
	
2. Install OPENCV4
	sudo apt-get install build-essential cmake git pkg-config
	sudo apt-get install python3-dev python3-numpy
	sudo apt-get install libjpeg-dev libpng-dev
	sudo apt-get install libavcodec-dev libavformat-dev
	sudo apt-get install libswscale-dev libdc1394-22-dev
	sudo apt-get install libv4l-dev v4l-utils
	sudo apt-get install libgtk2.0-dev libcanberra-gtk* libgtk-3-dev


	cd ~
	git clone --depth=1 https://github.com/opencv/opencv.git
	cd opencv
	mkdir build
	cd build
	cmake ..
	make -j4

3. Install ORB-SLAM3
	chmod +x build.sh
	./build.sh
	
	3.1 If error is about "error: ‘m_slots’ was not declared in this scope":
		sed -i 's/++11/++14/g' CMakeLists.txt
		then try installation again.
	
4. Run ORBSLAM3 on EuRoC dataset
	Download sample datasets from here(https://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets) - one easy [MH01], one difficult [MH05]
	Put the extracted downloaded datasets in this format inside Examples directory:
		Datasets/EuRoC/...
	Modify euroc_examples.sh to comment out all other test data from running except the one you want to run. 
		For example, for running MH05 dataset, do the following changes:
			Line 2: pathDatasetEuroc='./Datasets/EuRoC' #Example, it is necesary to change it by the dataset path
			Line 19: ./Monocular/mono_euroc ../Vocabulary/ORBvoc.txt ./Monocular/EuRoC.yaml "$pathDatasetEuroc"/MH_05_difficult ./Monocular/EuRoC_TimeStamps/MH05.txt dataset-MH05_mono
	
	For running:
		cd Examples
		./euroc_examples.sh
	
	n case, Window GUI didn't show up during running:
		Change line 84 in mono_euroc.cc :     ORB_SLAM3::System SLAM(argv[1],argv[2],ORB_SLAM3::System::MONOCULAR, true);
			i.e. change false to true for the fourth param.
	Build again.
	Run again.

5. Benchmarking EuRoC Evaluation
	Run Evaluation Script
	
6. Running with ROS
	Update build_ros.sh if you have conda installed.
	Better create an environment named ROS and give it's path for Python executable.
	
	Update in build_ros.sh:
		echo "Building ROS nodes"

		cd Examples/ROS/ORB_SLAM3
		mkdir build
		cd build
		cmake .. -DROS_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/home/marsar/anaconda3/envs/ROS/bin/python
		make -j4
	If Sophus error:
		Install Sophus.
		Go to Thirdparty/Sophus/build
		cmake ..
		sudo make install
	A lot of sigslot and other errors:
		change CMakeLists.txt inside the Examples/ROS/ORB_SLAM3 directory
		change the C++ standard to 14 from 11
	If errors of Sophus conversion to CV::Mat
		Comment out project MonoAR from CMakeLists.txt in Examples/ROS/ORB_SLAM3 directory
		Currently not using this project, if needs to be used. Go here: https://github.com/UZ-SLAMLab/ORB_SLAM3/issues/479
	
	Run ROS nodes
		If segmentation fault errors:
		 Probably due to Opencv 3 vs 4 mismatch, part of ROS code in ORB-SLAM3 expects 3 vs what's installed on my system is 4.
		Fix:
		(https://github.com/ethz-asl/kalibr/issues/368)
		 Clone cv_bridge package inside catkin_ws/src:
		 	git clone https://github.com/fizyr-forks/vision_opencv/tree/opencv4
			cd vision_opencv
			git checkout opencv4
		 change CMakeLists.txt line 11:
			 from     find_package(Boost REQUIRED python3)
			 to     find_package(Boost REQUIRED python)
		cd to catkin_ws
		catkin_make -j4
		
