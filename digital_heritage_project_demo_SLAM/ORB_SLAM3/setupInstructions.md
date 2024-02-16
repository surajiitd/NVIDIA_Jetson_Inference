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
		
