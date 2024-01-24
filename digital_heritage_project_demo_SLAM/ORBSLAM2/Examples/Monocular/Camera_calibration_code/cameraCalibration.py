import cv2
import numpy as np

pattern_size = (8, 6)

obj_points = []  
img_points = []  

objp = np.zeros((np.prod(pattern_size), 3), dtype=np.float32)
objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

calibration_images = []
calibration_images.append(cv2.imread('calibration_image0.png'))
calibration_images.append(cv2.imread('calibration_image1.png'))
calibration_images.append(cv2.imread('calibration_image2.png'))
calibration_images.append(cv2.imread('calibration_image3.png'))

for img in calibration_images:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

    if ret:
        obj_points.append(objp)
        img_points.append(corners)

        img = cv2.drawChessboardCorners(img, pattern_size, corners, ret)

        cv2.imshow('Calibration Image', img)
        cv2.waitKey(500)  
        cv2.destroyWindow('Calibration Image')

ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

print("Camera Matrix:")
print(camera_matrix)
print("\nDistortion Coefficients:")
print(dist_coeffs)
