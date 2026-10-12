#!/usr/bin/env python3

import numpy as np
import depthai as dai
import rospy

device = dai.Device()
calib_data = device.readCalibration()
rgb_camsocket = dai.CameraBoardSocket.CAM_A

camera_matrix = np.array(
    calib_data.getCameraIntrinsics(rgb_camsocket,4056,3040)
    )

print("Camera Intrinsics:")
print(camera_matrix)

