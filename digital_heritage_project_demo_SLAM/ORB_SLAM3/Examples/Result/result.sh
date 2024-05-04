# for direc in traj*;
# do
#     cd $direc;
#     echo $direc;
#     type=trans_part
#     plot_mode=xyz
#     evo_ape tum groundtruth.txt rgb.txt --pose_relation ${type}  --plot_mode ${plot_mode} --plot_x_dimension index --save_plot results_rpe/${type}/rgb_${plot_mode}  --save_results results_rpe/${type}/rgb.zip --align_origin --no_warnings;
#     # evo_rpe tum groundtruth.txt rgbd.txt --pose_relation ${type} --delta 1 --delta_unit f --plot_mode ${plot_mode} --plot_x_dimension index --save_plot results_rpe/${type}/rgbd_${plot_mode}  --save_results results_rpe/${type}/rgbd.zip --align_origin --no_warnings;
#     # evo_rpe tum groundtruth.txt p-rgbd.txt --pose_relation ${type} --delta 1 --delta_unit f --plot_mode ${plot_mode} --plot_x_dimension index --save_plot results_rpe/${type}/p-rgbd_${plot_mode}  --save_results results_rpe/${type}/p-rgbd.zip --align_origin --no_warnings;
#     # evo_rpe tum groundtruth.txt p-rgbd_scaled.txt --pose_relation ${type} --delta 1 --delta_unit f --plot_mode ${plot_mode} --plot_x_dimension index --save_plot results_rpe/${type}/p-rgbd_scaled_${plot_mode}  --save_results results_rpe/${type}/p-rgbd_scaled.zip --align_origin --no_warnings;
#     evo_res ./results_rpe/${type}/*.zip --plot_markers --use_rel_time --no_warnings --save_plot ./results_rpe/${type}/comparison;
#     cd ../

# done

groundtruthTraj=../../Datasets/RGB-D/kitti_data_odometry_poses/dataset/poses
slamTraj=../CameraTrajectory

evo_ape kitti $groundtruthTraj/$1 $slamTraj/$2 --pose_relation trans_part  --plot_mode xz --plot_x_dimension index --save_plot ../Result/results_rpe/trans_part/"$3"_p-rgbd_xz --save_results ../Result/results_rpe/trans_part/"$3"_p-rgbd.zip --align_origin --no_warnings;

# evo_ape kitti $groundtruthTraj/$1 $slamTraj/$2 --pose_relation trans_part  --plot_mode xz --plot_x_dimension index --save_plot ../Result/results_rpe/trans_part/"$3"_p-rgbd_xz --save_results ../Result/results_rpe/trans_part/"$3"_p-rgbd.zip --n_to_align 100 --align_origin --no_warnings;
