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
CMAKE_SOURCE_DIR = /home/vision/slam/curl-7.77.0

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/vision/slam/curl-7.77.0/build

# Utility rule file for test-event.

# Include the progress variables for this target.
include tests/CMakeFiles/test-event.dir/progress.make

tests/CMakeFiles/test-event:
	cd /home/vision/slam/curl-7.77.0/build/tests && /usr/bin/perl /home/vision/slam/curl-7.77.0/tests/runtests.pl -a -e "\$$TFLAGS"

test-event: tests/CMakeFiles/test-event
test-event: tests/CMakeFiles/test-event.dir/build.make

.PHONY : test-event

# Rule to build all files generated by this target.
tests/CMakeFiles/test-event.dir/build: test-event

.PHONY : tests/CMakeFiles/test-event.dir/build

tests/CMakeFiles/test-event.dir/clean:
	cd /home/vision/slam/curl-7.77.0/build/tests && $(CMAKE_COMMAND) -P CMakeFiles/test-event.dir/cmake_clean.cmake
.PHONY : tests/CMakeFiles/test-event.dir/clean

tests/CMakeFiles/test-event.dir/depend:
	cd /home/vision/slam/curl-7.77.0/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/vision/slam/curl-7.77.0 /home/vision/slam/curl-7.77.0/tests /home/vision/slam/curl-7.77.0/build /home/vision/slam/curl-7.77.0/build/tests /home/vision/slam/curl-7.77.0/build/tests/CMakeFiles/test-event.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tests/CMakeFiles/test-event.dir/depend

