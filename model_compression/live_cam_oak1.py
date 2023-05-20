""" 
script to read OAK-1 frames
"""
import sys

from tqdm import tqdm
import numpy as np
import cv2
import os
import glob 
import time
import depthai as dai



# def show_image(image):
#     cv2.imshow('image', image / 255.0)
#     cv2.waitKey(1)

# def image_stream(device, stride):
#     """ image generator """

#     # fx, fy, cx, cy = 3.09563892e+03, 3.09563892e+03, 1.95490430e+03, 1.09161853e+03

#     # K = np.eye(3)
#     # K[0,0] = fx
#     # K[0,2] = cx
#     # K[1,1] = fy
#     # K[1,2] = cy

#     qRgb = device.getOutputQueue(name="rgb", maxSize=5)

#     while True:
#         inRgb = qRgb.tryGet()

#         if inRgb is not None:
#             image = inRgb.getCvFrame()
#         else:
#             continue

#         # h0, w0, _ = image.shape
#         # h1 = int(h0 * np.sqrt((288 * 512) / (h0 * w0)))
#         # w1 = int(w0 * np.sqrt((288 * 512) / (h0 * w0)))

#         # image = cv2.resize(image, (w1, h1))
#         # image = image[:h1-h1%8, :w1-w1%8]
#         # print(image.shape)


#         # yield t, image[None] # , #intrinsics
        
#         # t = t + 1


if __name__ == '__main__':

    pipeline = dai.Pipeline()

    camRgb = pipeline.createColorCamera()
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
    # camRgb.setPreviewSize(1280,720)
    camRgb.setPreviewSize(300,300)
    camRgb.initialControl.setManualFocus(1)
    #camRgb.setAutoWhiteBalanceMode( AutoWhiteBalanceMode.OFF)

    xoutRgb = pipeline.createXLinkOut()
    xoutRgb.setStreamName("rgb")
    controlIn = pipeline.create(dai.node.XLinkIn)
    controlIn.setStreamName('control')
    
    camRgb.video.link(xoutRgb.input)
    
    device = dai.Device(pipeline)

    ctrl = dai.CameraControl()
    ctrl.setAutoWhiteBalanceMode(dai.CameraControl.AutoWhiteBalanceMode.OFF)
    controlQueue = device.getInputQueue('control')
    controlQueue.send(ctrl)

    tstamps = []
    # for (t, image) in tqdm(image_stream(device, 1)):

    qRgb = device.getOutputQueue(name="rgb", maxSize=1,blocking=False)

    while True:
        inRgb = qRgb.tryGet()

        if inRgb is not None:
            image = inRgb.getCvFrame()
        else:
            continue
        print(image.shape)
        window_name = "image"
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, image / 255.0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

