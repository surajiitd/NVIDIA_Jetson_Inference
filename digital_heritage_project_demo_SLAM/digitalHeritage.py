# Import the Tkinter library
import tkinter as tk
import os

def run_test_recorded_sh():
    original_directory = os.getcwd()
    os.chdir('ORB_SLAM3/Examples/Monocular/Run_Scripts')
    script_file = "./test_recorded_example.sh"
    print(f"Executing {script_file} ...")
    os.system(f"bash {script_file}")
    os.chdir(original_directory)

def run_build_sh():
    original_directory = os.getcwd()
    os.chdir('ORB_SLAM3')
    script_file = "./build.sh"
    print(f"Executing {script_file} ...")
    os.system(f"bash {script_file}")
    os.chdir(original_directory)

def run_test_webcam_2_sh():
    original_directory = os.getcwd()
    os.chdir('ORB_SLAM3/Examples/Monocular/Run_Scripts')
    script_file = "./test_webcam_2_example.sh"
    print(f"Executing {script_file} ...")
    os.system(f"bash {script_file}")
    os.chdir(original_directory)

# Create a main application window
root = tk.Tk()
root.title("Digital Heritage App")

# Create a button to run the shell script
button1 = tk.Button(root, text="test_recorded.sh", command=run_test_recorded_sh)
button1.pack(pady=20)
button2 = tk.Button(root, text="build.sh", command=run_build_sh)
button2.pack(pady=20)
button3 = tk.Button(root, text="test_webcam_2_example.sh", command=run_test_webcam_2_sh)
button3.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()