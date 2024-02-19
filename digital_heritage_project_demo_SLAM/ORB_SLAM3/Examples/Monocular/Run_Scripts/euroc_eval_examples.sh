#!/bin/bash
pathDatasetEuroc='./Datasets/EuRoC' #Example, it is necesary to change it by the dataset path


# Single Session Example (Pure visual - monocular)
sequence1='MH01'
echo "Launching $sequence1 with Monocular sensor"
./Monocular/mono_euroc ../Vocabulary/ORBvoc.txt ./Monocular/EuRoC.yaml "$pathDatasetEuroc"/"$sequence1" ./Monocular/EuRoC_TimeStamps/"$sequence1".txt dataset-"$sequence1"_monocular
echo "------------------------------------"
echo "Evaluation of $sequence1 trajectory with left camera only - monocular"
python3 ../evaluation/evaluate_ate_scale.py ../evaluation/Ground_truth/EuRoC_left_cam/"$sequence1"_GT.txt f_dataset-"$sequence1"_monocular.txt --plot "$sequence1"_monocular.pdf --verbose --verbose2


# # Single Session Example (Pure visual stereo)
# sequence='MH05' # Sequence on which to run the evaluation.
# echo "Launching MH05 with Stereo sensor"
# ./Stereo/stereo_euroc ../Vocabulary/ORBvoc.txt ./Stereo/EuRoC.yaml "$pathDatasetEuroc"/"$sequence" ./Stereo/EuRoC_TimeStamps/"$sequence".txt dataset-"$sequence"_stereo
# echo "------------------------------------"
# echo "Evaluation of MH05 trajectory with Stereo sensor"
# python3 ../evaluation/evaluate_ate_scale.py ../evaluation/Ground_truth/EuRoC_left_cam/"$sequence"_GT.txt f_dataset-"$sequence"_stereo.txt --plot "$sequence"_stereo.pdf 



#MultiSession Example (Pure visual)
# echo "Launching Machine Hall with Stereo sensor"
# ./Stereo/stereo_euroc ../Vocabulary/ORBvoc.txt ./Stereo/EuRoC.yaml "$pathDatasetEuroc"/MH01 ./Stereo/EuRoC_TimeStamps/MH01.txt "$pathDatasetEuroc"/MH02 ./Stereo/EuRoC_TimeStamps/MH02.txt "$pathDatasetEuroc"/MH03 ./Stereo/EuRoC_TimeStamps/MH03.txt "$pathDatasetEuroc"/MH04 ./Stereo/EuRoC_TimeStamps/MH04.txt "$pathDatasetEuroc"/MH05 ./Stereo/EuRoC_TimeStamps/MH05.txt dataset-MH01_to_MH05_stereo
# echo "------------------------------------"
# echo "Evaluation of MAchine Hall trajectory with Stereo sensor"
# python ../evaluation/evaluate_ate_scale.py ../evaluation/Ground_truth/EuRoC_left_cam/MH_GT.txt f_dataset-MH01_to_MH05_stereo.txt --plot MH01_to_MH05_stereo.pdf


#Single Session Example (Visual-Inertial)
# echo "Launching V102 with Monocular-Inertial sensor"
# ./Monocular-Inertial/mono_inertial_euroc ../Vocabulary/ORBvoc.txt ./Monocular-Inertial/EuRoC.yaml "$pathDatasetEuroc"/V102 ./Monocular-Inertial/EuRoC_TimeStamps/V102.txt dataset-V102_monoi
# echo "------------------------------------"
# echo "Evaluation of V102 trajectory with Monocular-Inertial sensor"
# python ../evaluation/evaluate_ate_scale.py "$pathDatasetEuroc"/V102/mav0/state_groundtruth_estimate0/data.csv f_dataset-V102_monoi.txt --plot V102_monoi.pdf


#MultiSession Monocular Examples

# echo "Launching Vicon Room 2 with Monocular-Inertial sensor"
# ./Monocular-Inertial/mono_inertial_euroc ../Vocabulary/ORBvoc.txt ./Monocular-Inertial/EuRoC.yaml "$pathDatasetEuroc"/V201 ./Monocular-Inertial/EuRoC_TimeStamps/V201.txt "$pathDatasetEuroc"/V202 ./Monocular-Inertial/EuRoC_TimeStamps/V202.txt "$pathDatasetEuroc"/V203 ./Monocular-Inertial/EuRoC_TimeStamps/V203.txt dataset-V201_to_V203_monoi
# echo "------------------------------------"
# echo "Evaluation of Vicon Room 2 trajectory with Stereo sensor"
# python ../evaluation/evaluate_ate_scale.py ../evaluation/Ground_truth/EuRoC_imu/V2_GT.txt f_dataset-V201_to_V203_monoi.txt --plot V201_to_V203_monoi.pdf

