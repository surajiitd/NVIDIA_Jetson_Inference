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

# Include any dependencies generated for this target.
include tests/libtest/CMakeFiles/lib1520.dir/depend.make

# Include the progress variables for this target.
include tests/libtest/CMakeFiles/lib1520.dir/progress.make

# Include the compile flags for this target's objects.
include tests/libtest/CMakeFiles/lib1520.dir/flags.make

tests/libtest/CMakeFiles/lib1520.dir/lib1520.c.o: tests/libtest/CMakeFiles/lib1520.dir/flags.make
tests/libtest/CMakeFiles/lib1520.dir/lib1520.c.o: ../tests/libtest/lib1520.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/vision/slam/curl-7.77.0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object tests/libtest/CMakeFiles/lib1520.dir/lib1520.c.o"
	cd /home/vision/slam/curl-7.77.0/build/tests/libtest && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/lib1520.dir/lib1520.c.o   -c /home/vision/slam/curl-7.77.0/tests/libtest/lib1520.c

tests/libtest/CMakeFiles/lib1520.dir/lib1520.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/lib1520.dir/lib1520.c.i"
	cd /home/vision/slam/curl-7.77.0/build/tests/libtest && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/vision/slam/curl-7.77.0/tests/libtest/lib1520.c > CMakeFiles/lib1520.dir/lib1520.c.i

tests/libtest/CMakeFiles/lib1520.dir/lib1520.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/lib1520.dir/lib1520.c.s"
	cd /home/vision/slam/curl-7.77.0/build/tests/libtest && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/vision/slam/curl-7.77.0/tests/libtest/lib1520.c -o CMakeFiles/lib1520.dir/lib1520.c.s

tests/libtest/CMakeFiles/lib1520.dir/first.c.o: tests/libtest/CMakeFiles/lib1520.dir/flags.make
tests/libtest/CMakeFiles/lib1520.dir/first.c.o: ../tests/libtest/first.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/vision/slam/curl-7.77.0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object tests/libtest/CMakeFiles/lib1520.dir/first.c.o"
	cd /home/vision/slam/curl-7.77.0/build/tests/libtest && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/lib1520.dir/first.c.o   -c /home/vision/slam/curl-7.77.0/tests/libtest/first.c

tests/libtest/CMakeFiles/lib1520.dir/first.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/lib1520.dir/first.c.i"
	cd /home/vision/slam/curl-7.77.0/build/tests/libtest && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/vision/slam/curl-7.77.0/tests/libtest/first.c > CMakeFiles/lib1520.dir/first.c.i

tests/libtest/CMakeFiles/lib1520.dir/first.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/lib1520.dir/first.c.s"
	cd /home/vision/slam/curl-7.77.0/build/tests/libtest && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/vision/slam/curl-7.77.0/tests/libtest/first.c -o CMakeFiles/lib1520.dir/first.c.s

# Object files for target lib1520
lib1520_OBJECTS = \
"CMakeFiles/lib1520.dir/lib1520.c.o" \
"CMakeFiles/lib1520.dir/first.c.o"

# External object files for target lib1520
lib1520_EXTERNAL_OBJECTS =

tests/libtest/lib1520: tests/libtest/CMakeFiles/lib1520.dir/lib1520.c.o
tests/libtest/lib1520: tests/libtest/CMakeFiles/lib1520.dir/first.c.o
tests/libtest/lib1520: tests/libtest/CMakeFiles/lib1520.dir/build.make
tests/libtest/lib1520: lib/libcurl.so
tests/libtest/lib1520: /usr/lib/aarch64-linux-gnu/libssl.so
tests/libtest/lib1520: /usr/lib/aarch64-linux-gnu/libcrypto.so
tests/libtest/lib1520: /usr/lib/aarch64-linux-gnu/libz.so
tests/libtest/lib1520: tests/libtest/CMakeFiles/lib1520.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/vision/slam/curl-7.77.0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking C executable lib1520"
	cd /home/vision/slam/curl-7.77.0/build/tests/libtest && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/lib1520.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tests/libtest/CMakeFiles/lib1520.dir/build: tests/libtest/lib1520

.PHONY : tests/libtest/CMakeFiles/lib1520.dir/build

tests/libtest/CMakeFiles/lib1520.dir/clean:
	cd /home/vision/slam/curl-7.77.0/build/tests/libtest && $(CMAKE_COMMAND) -P CMakeFiles/lib1520.dir/cmake_clean.cmake
.PHONY : tests/libtest/CMakeFiles/lib1520.dir/clean

tests/libtest/CMakeFiles/lib1520.dir/depend:
	cd /home/vision/slam/curl-7.77.0/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/vision/slam/curl-7.77.0 /home/vision/slam/curl-7.77.0/tests/libtest /home/vision/slam/curl-7.77.0/build /home/vision/slam/curl-7.77.0/build/tests/libtest /home/vision/slam/curl-7.77.0/build/tests/libtest/CMakeFiles/lib1520.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tests/libtest/CMakeFiles/lib1520.dir/depend

