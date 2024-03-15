import tkinter as tk
import math
import numpy as np
import sys

sys.path.insert(0, 'Digital Heritage app') 

from getRequest import send_get_request

canvas_width = 400
canvas_height = 400
root = tk.Tk()
root.title("LOCALIZATION MAP")
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

url = "http://127.0.0.1:8080/locations"

data = send_get_request(url, False)
print(data)

# Landmarks
landmarks = []
landmarks_heading = []
for item in data:
    buf = ()
    if 'location_name' in item:
        landmarks_heading.append(item['yaw'])
        landmarks.append((item['x'], item['y']))
    
default_user_position = (canvas_width//2, canvas_height//2) # at the center of canvas

def Rz(theta):
    R = np.array([[math.cos(theta), math.sin(theta)], [-1*math.sin(theta), math.cos(theta)]]) # Rz(theta)
    return R

# Function to update the canvas
def update_canvas():
    data = send_get_request(url, False)

    # print(data[0]) # --> dict to user loc data
    # print(data[1]) # --> dict to location 1 data
    # print(data[2]) # --> dict to location 2 data

    # Update user heading and location based on trajectory points
    canvas.delete("all")
    canvas.create_oval(default_user_position[0]-5, default_user_position[1]-5, default_user_position[0]+5, default_user_position[1]+5, fill="green")
    
    # user's location
    user_location = (data[0]['x'], data[0]['y'])
    user_heading = data[0]['yaw']

    # Direction Arrow
    line_length = 20

    if user_heading < 0:
        user_heading = 360 - abs(user_heading)

    user_heading = math.radians(user_heading)

    # Rotate inverse to user's heading
    theta = user_heading
       
    # Draw landmarks
    for l in landmarks:
        # Transform to user coordinate
        landmark_wrt_user = np.array(l) - np.array(user_location)

        # Rotate w.r.t user
        landmark_rotated_wrt_user = Rz(theta) @ landmark_wrt_user.T

        # Transform to original coordinates # This is not required since we want to plot wrt to the user itself on the canvas.
        landmark_rotated = landmark_rotated_wrt_user + np.array(user_location).T

        # Transform to canvas
        landmark_rotated_canvas = landmark_rotated + np.array([canvas_width//2, canvas_height//2]).T
        new_x = landmark_rotated_canvas[0]
        new_y = landmark_rotated_canvas[1]
    
        # Draw landmark
        canvas.create_oval(new_x-3, new_y-3, new_x+3, new_y+3, fill="red")

        # Draw Heading
        line_end = np.rint(Rz(theta) @ np.array([line_length, 0]).T)
        canvas.create_line(default_user_position[0], default_user_position[1], new_x, new_y, fill="yellow", width=2)#default_user_position[1]+line_end[1]
        legend_text4 = f"User Coordinates: ({user_location[0]}, {user_location[1]})"
        canvas.create_text(10, 10, anchor="nw", text=legend_text4, fill="black")

        # Goal point in green
        canvas.create_oval(new_x-3, new_y-3, new_x+3, new_y+3, fill="green")
    
    # x is +ve to right and y is +ve to bottom
    # fixed = (100, 200)
    # canvas.create_oval(fixed[0]-3, fixed[1]-3, fixed[0]+3, fixed[1]+3, fill="yellow")
    # canvas.create_text(10, 20, anchor="nw", text=f"Fixed Coordinate: {fixed}", fill="black")
    
    legend_text1 = f"User coordinates (from ORB_SLAM3): (x = {data[0]['x']}, y = {data[0]['y']}, yaw = {data[0]['yaw']})"
    canvas.create_text(10, 20, anchor="nw", text=legend_text1, fill="black")

    legend_text2 = f"location 1 coordinates (from ORB_SLAM3): (x = {data[1]['x']}, y = {data[1]['y']}, yaw = {data[1]['yaw']})"
    canvas.create_text(10, 30, anchor="nw", text=legend_text2, fill="black")

    legend_text3 = f"location2 (from ORB_SLAM3): (x = {data[2]['x']}, y = {data[2]['y']}, yaw = {data[2]['yaw']})"
    canvas.create_text(10, 40, anchor="nw", text=legend_text3, fill="black")

    
    canvas.after(50, update_canvas)

# Start the update process
update_canvas()

# Run the tkinter main loop
root.mainloop()
