# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/build

# Include any dependencies generated for this target.
include CMakeFiles/rgbd_tum.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/rgbd_tum.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/rgbd_tum.dir/flags.make

CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.o: CMakeFiles/rgbd_tum.dir/flags.make
CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.o: ../Examples/RGB-D/rgbd_tum.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.o -c /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/Examples/RGB-D/rgbd_tum.cc

CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/Examples/RGB-D/rgbd_tum.cc > CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.i

CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/Examples/RGB-D/rgbd_tum.cc -o CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.s

# Object files for target rgbd_tum
rgbd_tum_OBJECTS = \
"CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.o"

# External object files for target rgbd_tum
rgbd_tum_EXTERNAL_OBJECTS =

../Examples/RGB-D/rgbd_tum: CMakeFiles/rgbd_tum.dir/Examples/RGB-D/rgbd_tum.cc.o
../Examples/RGB-D/rgbd_tum: CMakeFiles/rgbd_tum.dir/build.make
../Examples/RGB-D/rgbd_tum: ../lib/libORB_SLAM3.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_gapi.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_stitching.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_alphamat.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_aruco.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_bgsegm.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_bioinspired.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_ccalib.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudabgsegm.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudafeatures2d.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudaobjdetect.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudastereo.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_dnn_objdetect.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_dnn_superres.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_dpm.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_highgui.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_face.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_freetype.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_fuzzy.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_hdf.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_hfs.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_img_hash.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_intensity_transform.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_line_descriptor.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_quality.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_rapid.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_reg.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_rgbd.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_saliency.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_stereo.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_structured_light.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_phase_unwrapping.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_superres.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudacodec.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_surface_matching.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_tracking.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_datasets.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_plot.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_text.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_dnn.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_videostab.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_videoio.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudaoptflow.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudalegacy.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudawarping.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_optflow.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_xfeatures2d.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_ml.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_shape.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_ximgproc.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_video.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_xobjdetect.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_imgcodecs.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_objdetect.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_calib3d.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_features2d.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_flann.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_xphoto.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_photo.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudaimgproc.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudafilters.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_imgproc.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudaarithm.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_core.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libopencv_cudev.so.4.4.0
../Examples/RGB-D/rgbd_tum: /usr/lib/aarch64-linux-gnu/libtiff.so.5
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_glgeometry.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_geometry.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_plot.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_python.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_scene.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_tools.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_display.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_vars.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_video.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_packetstream.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_windowing.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_opengl.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_image.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libpango_core.so
../Examples/RGB-D/rgbd_tum: /usr/lib/aarch64-linux-gnu/libGLEW.so
../Examples/RGB-D/rgbd_tum: /usr/lib/aarch64-linux-gnu/libOpenGL.so
../Examples/RGB-D/rgbd_tum: /usr/lib/aarch64-linux-gnu/libGLX.so
../Examples/RGB-D/rgbd_tum: /usr/lib/aarch64-linux-gnu/libGLU.so
../Examples/RGB-D/rgbd_tum: /usr/local/lib/libtinyobj.so
../Examples/RGB-D/rgbd_tum: ../Thirdparty/DBoW2/lib/libDBoW2.so
../Examples/RGB-D/rgbd_tum: ../Thirdparty/g2o/lib/libg2o.so
../Examples/RGB-D/rgbd_tum: CMakeFiles/rgbd_tum.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../Examples/RGB-D/rgbd_tum"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rgbd_tum.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/rgbd_tum.dir/build: ../Examples/RGB-D/rgbd_tum

.PHONY : CMakeFiles/rgbd_tum.dir/build

CMakeFiles/rgbd_tum.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/rgbd_tum.dir/cmake_clean.cmake
.PHONY : CMakeFiles/rgbd_tum.dir/clean

CMakeFiles/rgbd_tum.dir/depend:
	cd /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3 /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3 /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/build /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/build /home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/build/CMakeFiles/rgbd_tum.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/rgbd_tum.dir/depend

