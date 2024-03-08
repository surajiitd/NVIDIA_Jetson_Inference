import os
print(os.getcwd())
os.chdir('ORB_SLAM3')
os.system('./build.sh')
os.chdir('ORB_SLAM3/Examples/Monocular/Run_Scripts')
print(os.getcwd())
os.system('./test_recorded_example.sh')