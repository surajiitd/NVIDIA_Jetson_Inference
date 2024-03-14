import tkinter as tk
import math
import numpy as np
import sys

sys.path.insert(0, 'Digital Heritage app')

from getRequest import send_get_request

canvas_width = 800
canvas_height = 800
root = tk.Tk()
root.title("LOCALIZATION MAP")
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

url = "http://127.0.0.1:8080/locations"

# Smooth trajectory points - straight line # user movement
start_point = (50, 50)
end_point = (350, 350)

# Landmarks
landmarks = [(50, 50), (100, 150), (200, 100), (300, 200), (250, 50), (150, 300), (350, 350), (250, 250), (100, 350), end_point]

# Generate user trajectory
l=200
trajectory_points = [(start_point[0] + (end_point[0] - start_point[0]) * i / l, start_point[1] + (end_point[1] - start_point[1]) * i / l) for i in range(l + 1)]

user_headings = [2 * (i/len(trajectory_points)) * math.pi for i in range(len(trajectory_points)+1)]
# user_headings = [math.atan2((end_point[1] - start_point[1]), (end_point[0] - start_point[0]) )for i in range(len(trajectory_points)+1)]

default_user_position = (canvas_width//2, canvas_height//2) # at the center of canvas

def Rz(theta):
    R = np.array([[math.cos(theta), math.sin(theta)], [-1*math.sin(theta), math.cos(theta)]]) # Rz(theta)
    return R

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

            # Rotate w.r.t user
            landmark_rotated_wrt_user = Rz(theta) @ landmark_wrt_user.T

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
        legend_text4 = f"User Coordinates: ({user_location[0]}, {user_location[1]})"
        canvas.create_text(10, 10, anchor="nw", text=legend_text4, fill="black")

        # Goal point in green
        canvas.create_oval(new_x-3, new_y-3, new_x+3, new_y+3, fill="green")
    
    # x is +ve to right and y is +ve to bottom
    fixed = (100, 200)
    canvas.create_oval(fixed[0]-3, fixed[1]-3, fixed[0]+3, fixed[1]+3, fill="yellow")
    canvas.create_text(10, 20, anchor="nw", text=f"Fixed Coordinate: {fixed}", fill="black")
    
    data = send_get_request(url, False)

    print(data[0]) # ==> dict to user loc data
    print(data[1]) # ==> dict to location 1 data
    print(data[2]) # ==> dict to location 2 data

    legend_text1 = f"User coordinates (from ORB_SLAM3): (x = {data[0]['x']}, y = {data[0]['y']}, yaw = {data[0]['yaw']})"
    canvas.create_text(10, 30, anchor="nw", text=legend_text1, fill="black")

    legend_text2 = f"location 1 coordinates (from ORB_SLAM3): (x = {data[1]['x']}, y = {data[1]['y']}, yaw = {data[1]['yaw']})"
    canvas.create_text(10, 40, anchor="nw", text=legend_text2, fill="black")

    legend_text3 = f"location2 (from ORB_SLAM3): (x = {data[2]['x']}, y = {data[2]['y']}, yaw = {data[2]['yaw']})"
    canvas.create_text(10, 50, anchor="nw", text=legend_text3, fill="black")

    
    canvas.after(50, update_canvas)

# Start the update process
update_canvas()

# Run the tkinter main loop
root.mainloop()
