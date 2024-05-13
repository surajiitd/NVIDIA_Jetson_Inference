import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import LinearSegmentedColormap

def plot_pose_TUM(file_path, num_samples=1800, start_color='green', end_color='red'):
    return

def plot_pose_data(file_path, num_samples=1800, TUMFormat=False, start_color='green', end_color='red'):
    if TUMFormat:
        plot_pose_TUM(file_path, num_samples, start_color, end_color)
        return
    # Read data from the file
    data = np.loadtxt(file_path)

    # Extract x, y, z, roll, pitch, and yaw (in degrees) from the data
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    roll = data[:, 3]
    pitch = data[:, 4]
    yaw_deg = data[:, 5]

    # Convert yaw from degrees to radians
    yaw_rad = np.radians(yaw_deg)

    # Sample uniformly from the data
    indices = np.linspace(0, len(x) - 1, num_samples, dtype=int)
    x_sampled = x[indices]
    y_sampled = y[indices]
    z_sampled = z[indices]
    roll_sampled = roll[indices]
    pitch_sampled = pitch[indices]
    yaw_sampled = yaw_rad[indices]

    # Define colormap
    cmap = LinearSegmentedColormap.from_list('trajectory_color', [start_color, end_color])

    # Plot the data
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot camera pyramids and trajectory points
    for i in range(num_samples):
        # Camera pyramid vertices
        pyramid_vertices = np.array([[0, 0, 0], [0.05, 0.02, 0.02], [0.05, -0.02, 0.02], [0.05, -0.02, -0.02], [0.05, 0.02, -0.02]])
        # Rotate pyramid according to roll, pitch, and yaw
        R_roll = np.array([[1, 0, 0], [0, np.cos(roll_sampled[i]), -np.sin(roll_sampled[i])], [0, np.sin(roll_sampled[i]), np.cos(roll_sampled[i])]])
        R_pitch = np.array([[np.cos(pitch_sampled[i]), 0, np.sin(pitch_sampled[i])], [0, 1, 0], [-np.sin(pitch_sampled[i]), 0, np.cos(pitch_sampled[i])]])
        R_yaw = np.array([[np.cos(yaw_sampled[i]), -np.sin(yaw_sampled[i]), 0], [np.sin(yaw_sampled[i]), np.cos(yaw_sampled[i]), 0], [0, 0, 1]])
        R_total = R_yaw @ R_pitch @ R_roll
        rotated_vertices = np.dot(pyramid_vertices, R_total.T)
        # Translate vertices to current position
        translated_vertices = rotated_vertices + np.array([x_sampled[i], y_sampled[i], z_sampled[i]])
        # Plot the pyramid
        # ax.add_collection3d(Poly3DCollection([translated_vertices[[0, 1, 2]], 
        #                                         translated_vertices[[0, 2, 3]], 
        #                                         translated_vertices[[0, 3, 4]], 
        #                                         translated_vertices[[0, 4, 1]]], color=cmap(i/num_samples)))

        # Plot trajectory point
        ax.scatter(x_sampled[i], y_sampled[i], z_sampled[i], color=cmap(i/num_samples), s=1)

    ax.set_title('Odometry Trajectory with Camera Orientation')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Z Position')
    ax.set_xlim([np.min(x), np.max(x)])
    ax.set_ylim([np.min(y), np.max(y)])
    ax.set_zlim([np.min(z), np.max(z)])
    
    # Add color bar legend
    sm = plt.cm.ScalarMappable(cmap=cmap)
    sm.set_array([])
    plt.colorbar(sm, label='Trajectory Point Index')

    ax.grid(True)
    plt.show()

if __name__ == "__main__":
    file_path = "/home/vision/NVIDIA_Jetson_Inference/digital_heritage_project_demo_SLAM/ORB_SLAM3/Examples/Monocular/CameraTrajectory/EuRoC_f_dataset-Recorded_mono.txt"
    num_samples = 500
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    if len(sys.argv) > 2:
        num_samples = int(sys.argv[2])
    plot_pose_data(file_path, num_samples, TUMFormat=False)