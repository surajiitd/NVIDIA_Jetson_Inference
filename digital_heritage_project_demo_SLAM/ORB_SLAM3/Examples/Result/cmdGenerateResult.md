# plot multiple 2D trajectory (with groundtruth as ref)
 ```bash 
 evo_traj kitti --ref <pathToGroundTruth> <pathToTrajectory1> <pathToTrajectory2> ... --plot_mode xz --plot --align_origin --correct_scale
 ```

# plot and calculate APE
## for Monocular Trajectories (with scale correction)
```bash 
evo_ape kitti <pathToGroundTruth> <pathToTrajectory> --align_origin --plot --plot_mode xz --correct_scale
```
## for RGBD/p-RGBD trajectories
```bash
evo_ape kitti <pathToGroundTruth> <pathToTrajectory> --align_origin --plot --plot_mode xz
```
```bash
evo_ape kitti ../Datasets/RGB-D/Kitti/kitti_data_odometry_poses/dataset/poses/00.txt ../RGB-D/CameraTrajectory/f_kitti_00_p-rgbd.kitti --align_origin --plot --plot_mode xz
```