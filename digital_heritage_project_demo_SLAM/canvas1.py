import tkinter as tk
import math
import numpy as np

canvas_width = 800
canvas_height = 800
root = tk.Tk()
root.title("LOCALIZATION MAP")
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()


filepath = "ORB_SLAM3/Examples/Monocular/Run_Scripts/pose_data.txt"

def loadData(filePath):
        # Read data from the file
    data = np.loadtxt(filePath)
    n = 55000
    n2 = 56000

    # Extract x, y, z, roll, pitch, and yaw (in degrees) from the data
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    roll = data[:, 3]
    pitch = data[:, 4]
    yaw_deg = data[:, 5]

    # Convert yaw from degrees to radians
    yaw_rad = np.radians(yaw_deg)

    return x, z, yaw_rad

userPoses = loadData(filepath)

print([(x, y) for x, y in zip(userPoses[0], userPoses[1])])

# Smooth trajectory points - straight line # user movement
start_point = (50, 50)
end_point = (0.1, 0.9)

# Landmarks
landmarks = [(0.100551, 0.314267), (0.407168, 0.580599), (0.332515, 0.824273)]

# Generate user trajectory
l=200
# trajectory_points = [(start_point[0] + (end_point[0] - start_point[0]) * i / l,
#                       start_point[1] + (end_point[1] - start_point[1]) * i / l) for i in range(l + 1)]

# user_headings = [2 * (i/len(trajectory_points)) * math.pi for i in range(len(trajectory_points)+1)]
# user_headings = [math.atan2((end_point[1] - start_point[1]), (end_point[0] - start_point[0]) )for i in range(len(trajectory_points)+1)]
s = 10
user_headings = [yaw for yaw in userPoses[2]]
trajectory_points = [(s*x, s*y) for x, y in zip(userPoses[0], userPoses[1])]

default_user_position = (canvas_width//2, canvas_height//2) # at the center of canvas

def Rz(theta):
    R = np.array([[math.cos(theta), math.sin(theta)], [-1*math.sin(theta), math.cos(theta)]]) # Rz(theta)
    return R

origLength = len(trajectory_points)

# Function to update the canvas
def update_canvas():
    global user_location, user_headings, trajectory_points

    # Update user heading and location based on trajectory points
    if trajectory_points:
        canvas.delete("all")
        canvas.create_oval(default_user_position[0]-5, default_user_position[1]-5,
                        default_user_position[0]+5, default_user_position[1]+5, fill="red")
        
        # user's location
        user_location = trajectory_points.pop(0)
        user_heading = user_headings.pop(0)
        # Direction Arrow
        line_length = 20

        # Rotate inverse to user's heading
        theta = user_heading
        
        # Draw landmarks
        for landmark in landmarks:
            # Transform to user coordinate
            landmark_wrt_user = np.array(landmark) - np.array(user_location)

            # print(landmark_wrt_user)

            # Rotate w.r.t user
            landmark_rotated_wrt_user = Rz(theta) @ (s*landmark_wrt_user.T)

            # Transform to original coordinates # This is not required since we want to plot wrt to the user itself on the canvas.
            landmark_rotated = landmark_rotated_wrt_user #+ np.array(user_location).T

            # Transform to canvas
            landmark_rotated_canvas = landmark_rotated + np.array([canvas_width//2, canvas_height//2]).T
            new_x = landmark_rotated_canvas[0]
            new_y = landmark_rotated_canvas[1]
        
            # Draw landmark
            canvas.create_oval(new_x-3, new_y-3, new_x+3, new_y+3, fill="blue")

        # Draw Heading
        line_end = np.rint(Rz(theta) @ np.array([line_length, 0]).T)
        canvas.create_line(default_user_position[0], default_user_position[1], new_x, new_y, fill="yellow", width=2)#default_user_position[1]+line_end[1]
        legend_text = f"User Coordinates: ({user_location[0]},\n \t\t{user_location[1]} \n \t\t{user_heading})"
        canvas.create_text(10, 10, anchor="nw", text=legend_text, fill="black")
        canvas.create_text(10, 60, anchor="nw", text="Frame Count: " +str(origLength-len(trajectory_points)), fill="black")

        trajectory_points

        # Goal point in green
        canvas.create_oval(new_x-3, new_y-3, new_x+3, new_y+3, fill="green")
    
    # x is +ve to right and y is +ve to bottom
    # fixed = (100, 200)
    # canvas.create_oval(fixed[0]-3, fixed[1]-3, fixed[0]+3, fixed[1]+3, fill="yellow")
    # canvas.create_text(10, 30, anchor="nw", text=f"Fixed Coordinate: {fixed}", fill="black")
    
    
    canvas.after(10, update_canvas)

# Start the update process
update_canvas()

# Run the tkinter main loop
root.mainloop()
