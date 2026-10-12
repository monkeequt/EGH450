#!/usr/bin/env python3

'''
Run as:
# check model path line ~30is
rosrun depthai_publisher dai_publisher_yolov5_runner
'''

###############################
# Libraries
###############################

from pathlib import Path
import threading
import csv
import argparse
import time
import sys
import json

import cv2
import numpy as np
import depthai as dai
import rospy

from sensor_msgs.msg import CompressedImage, Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError


###############################
# Parameters
###############################

pipeline = None
cam_source = 'rgb'  # 'rgb', 'left', 'right'
cam = None

# sync outputs
syncNN = True

# model path
modelsPath = "/home/uavteam6/catkin_ws_G6/src/depthai_publisher/Models"

# modelName = 'exp31Yolov5_ov21.4_6sh'
modelName = 'best_epoch'

# confJson = 'exp31Yolov5.json'
confJson = 'best.json'
File_name = 'Best_Shave'

################################
# Yolo Config File
################################

configPath = Path(f'{modelsPath}/{File_name}/{confJson}')

if not configPath.exists():
    raise ValueError("Path {} does not exist!".format(configPath))

with configPath.open() as f:
    config = json.load(f)

nnConfig = config.get("nn_config", {})

# Extract metadata
metadata = nnConfig.get("NN_specific_metadata", {})

classes = metadata.get("classes", 0)
coordinates = metadata.get("coordinates", 4)
anchors = metadata.get("anchors", [])
anchorMasks = metadata.get("anchor_masks", {})
iouThreshold = metadata.get("iou_threshold", 0.5)
confidenceThreshold = metadata.get("confidence_threshold", 0.2)

# Parse labels
nnMappings = config.get("mappings", {})
labels = nnMappings.get("labels", [])


class DepthaiCamera():

    # Network input resolution
    fps = 20.0

    pub_topic = '/depthai_node/image/compressed'
    pub_topic_raw = '/depthai_node/image/raw'
    pub_topic_detect = '/depthai_node/detection/compressed'
    pub_topic_detect_raw = '/depthai_node/detection/raw'
    pub_topic_cam_inf = '/depthai_node/camera/camera_info'

    def __init__(self):

        self.pipeline = dai.Pipeline()

        # OAK-D stereo depth settings
        self.depth_enabled = False
        self.depth_width = None
        self.depth_height = None

        # Input image size
        if "input_size" in nnConfig:
            self.nn_shape_w, self.nn_shape_h = tuple(
                map(int, nnConfig.get("input_size").split('x'))
            )
        else:
            self.nn_shape_w = 416
            self.nn_shape_h = 416

        # Publish ROS image data
        self.pub_image = rospy.Publisher(
            self.pub_topic,
            CompressedImage,
            queue_size=10
        )

        self.pub_image_raw = rospy.Publisher(
            self.pub_topic_raw,
            Image,
            queue_size=10
        )

        self.pub_image_detect = rospy.Publisher(
            self.pub_topic_detect,
            CompressedImage,
            queue_size=10
        )

        self.pub_image_detect_raw = rospy.Publisher(
            self.pub_topic_detect_raw,
            Image,
            queue_size=10
        )

        # Create publisher for CameraInfo
        self.pub_cam_inf = rospy.Publisher(
            self.pub_topic_cam_inf,
            CameraInfo,
            queue_size=10
        )

        # Timer for camera info
        self.timer = rospy.Timer(
            rospy.Duration(1.0 / 10),
            self.publish_camera_info,
            oneshot=False
        )

        rospy.loginfo(
            "Publishing images to rostopic: {}".format(
                self.pub_topic
            )
        )

        self.br = CvBridge()

        rospy.on_shutdown(
            lambda: self.shutdown()
        )


    def publish_camera_info(self, timer=None):

        camera_info_msg = CameraInfo()

        camera_info_msg.header.frame_id = "camera_frame"

        camera_info_msg.height = self.nn_shape_h
        camera_info_msg.width = self.nn_shape_w

        # Camera intrinsic matrix
        camera_info_msg.K = [
            [3.25093799e+03,0.0,2.03031531e+03],
            [0.0,3.25093799e+03,1.54433728e+03],
            [0.0,0.0,1.0]
        ]

        # Distortion parameters
        camera_info_msg.D = np.zeros(5)

        # Rectification matrix
        camera_info_msg.R = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ]

        # Projection matrix
        camera_info_msg.P = [
        3.25093799e+03,0.0,2.03031531e+03,0.0,
        0.0,3.25093799e+03,1.54433728e+03,0.0,
        0.0,0.0,1.0,0.0
        ]

        camera_info_msg.distortion_model = "plumb_bob"

        camera_info_msg.header.stamp = rospy.Time.now()

        self.pub_cam_inf.publish(camera_info_msg)


    def rgb_camera(self):

        cam_rgb = self.pipeline.createColorCamera()

        cam_rgb.setPreviewSize(
            self.nn_shape_w,
            self.nn_shape_h
        )

        cam_rgb.setInterleaved(False)
        cam_rgb.setFps(self.fps)

        ctrl_in = self.pipeline.createXLinkIn()

        ctrl_in.setStreamName("cam_ctrl")

        ctrl_in.out.link(
            cam_rgb.inputControl
        )

        xout_rgb = self.pipeline.createXLinkOut()

        xout_rgb.setStreamName("video")

        cam_rgb.preview.link(
            xout_rgb.input
        )


    ###############################
    # YOLO decoder
    ###############################

    def sigmoid(self, x):

        # Prevent overflow
        x = np.clip(x, -50, 50)

        return 1.0 / (1.0 + np.exp(-x))


    def decode_yolo(self, nn_data, frame):
        """
        Decode a YOLOv5 output tensor with shape [1, 10647, 7].

        For a standard YOLOv5 ONNX/OpenVINO export, each row is already:

            [center_x, center_y, width, height,
             objectness, class0, class1]

        The coordinates have already been decoded by the YOLO Detect layer,
        so DO NOT apply anchors, grids, strides, or sigmoid again here.
        """

        output = np.asarray(
            nn_data.getFirstLayerFp16(),
            dtype=np.float32
        ).reshape(-1, 7)

        if output.shape[0] != 10647:
            rospy.logwarn_throttle(
                5.0,
                "Unexpected YOLO output shape: {}".format(output.shape)
            )
            return []

        # Split tensor
        boxes_xywh = output[:, 0:4]
        objectness = output[:, 4]
        class_scores = output[:, 5:7]

        # Standard YOLOv5 confidence = objectness * best class probability
        class_ids = np.argmax(class_scores, axis=1)
        best_class_scores = class_scores[
            np.arange(class_scores.shape[0]),
            class_ids
        ]
        confidences = objectness * best_class_scores

        # Filter before doing any per-box Python work
        keep = confidences >= confidenceThreshold

        if not np.any(keep):
            return []

        boxes_xywh = boxes_xywh[keep]
        confidences = confidences[keep]
        class_ids = class_ids[keep]

        # YOLOv5 exported coordinates are normally in model-input pixels.
        cx = boxes_xywh[:, 0]
        cy = boxes_xywh[:, 1]
        w = boxes_xywh[:, 2]
        h = boxes_xywh[:, 3]

        x1 = cx - w / 2.0
        y1 = cy - h / 2.0
        x2 = cx + w / 2.0
        y2 = cy + h / 2.0

        # Clip to NN input dimensions
        x1 = np.clip(x1, 0.0, float(self.nn_shape_w))
        y1 = np.clip(y1, 0.0, float(self.nn_shape_h))
        x2 = np.clip(x2, 0.0, float(self.nn_shape_w))
        y2 = np.clip(y2, 0.0, float(self.nn_shape_h))

        widths = x2 - x1
        heights = y2 - y1

        valid = (widths > 1.0) & (heights > 1.0)

        if not np.any(valid):
            return []

        x1 = x1[valid]
        y1 = y1[valid]
        widths = widths[valid]
        heights = heights[valid]
        confidences = confidences[valid]
        class_ids = class_ids[valid]

        boxes_for_nms = np.stack(
            [x1, y1, widths, heights],
            axis=1
        ).tolist()

        scores_for_nms = confidences.tolist()

        indices = cv2.dnn.NMSBoxes(
            boxes_for_nms,
            scores_for_nms,
            confidenceThreshold,
            iouThreshold
        )

        if indices is None or len(indices) == 0:
            return []

        indices = np.asarray(indices).reshape(-1)

        detections = []

        for idx in indices:
            idx = int(idx)

            xmin = x1[idx] / float(self.nn_shape_w)
            ymin = y1[idx] / float(self.nn_shape_h)
            xmax = (x1[idx] + widths[idx]) / float(self.nn_shape_w)
            ymax = (y1[idx] + heights[idx]) / float(self.nn_shape_h)

            detections.append({
                "label": int(class_ids[idx]),
                "confidence": float(confidences[idx]),
                "xmin": float(xmin),
                "ymin": float(ymin),
                "xmax": float(xmax),
                "ymax": float(ymax)
            })

        return detections


    ###############################
    # Depth measurement
    ###############################

    def get_distance_to_detection_center(self, depth_frame, detection):
        """
        Measure depth at the centre of a YOLO bounding box.

        The depth frame is aligned to the RGB camera and resized to the
        neural-network resolution, so the normalized YOLO coordinates can
        be used directly to address the depth image.

        Returns:
            z_mm: depth along the RGB camera optical axis, in millimetres.
            distance_mm: straight-line distance from the camera to the
                         measured 3-D point, in millimetres.
        """

        if depth_frame is None:
            return None, None

        depth_h, depth_w = depth_frame.shape[:2]

        # Centre of the detected bounding box in normalized coordinates.
        cx_norm = (detection["xmin"] + detection["xmax"]) / 2.0 #could multiply by 416
        cy_norm = (detection["ymin"] + detection["ymax"]) / 2.0

        px = int(np.clip(cx_norm * depth_w, 0, depth_w - 1))
        py = int(np.clip(cy_norm * depth_h, 0, depth_h - 1))

        # Use a small window around the centre rather than one pixel.
        # This makes the measurement considerably less sensitive to
        # invalid stereo pixels/noise.
        radius = 3
        x0 = max(0, px - radius)
        x1 = min(depth_w, px + radius + 1)
        y0 = max(0, py - radius)
        y1 = min(depth_h, py + radius + 1)

        roi = depth_frame[y0:y1, x0:x1]
        valid_depth = roi[roi > 0]

        if valid_depth.size == 0:
            return None, None

        # Median depth in millimetres.
        z_mm = float(np.median(valid_depth))

        # At this point z_mm is the camera-axis distance.  For a true
        # straight-line camera-to-point distance, deproject the centre
        # using the RGB camera intrinsics. 

        cx = 2.03031531e+03
        cy = 1.54433728e+03
        fx = 3.25093799e+03
        fy = 3.25093799e+03



        x_mm = (px - cx) * z_mm / fx
        y_mm = (py - cy) * z_mm / fy
        distance_mm = float(np.sqrt(x_mm * x_mm + y_mm * y_mm + z_mm * z_mm))

        return z_mm, distance_mm


    ###############################
    # Frame normalization
    ###############################

    def frameNorm(self, frame, bbox):

        normVals = np.full(
            len(bbox),
            frame.shape[0]
        )

        normVals[::2] = frame.shape[1]

        return (
            np.clip(
                np.array(bbox),
                0,
                1
            ) * normVals
        ).astype(int)


    ###############################
    # Draw YOLO detections
    ###############################

    def show_yolo(self, frame, detections):

        color = (255, 0, 0)

        overlay = frame.copy()

        for detection in detections:

            bbox = self.frameNorm(
                overlay,
                (
                    detection["xmin"],
                    detection["ymin"],
                    detection["xmax"],
                    detection["ymax"]
                )
            )

            label = detection["label"]

            confidence = detection[
                "confidence"
            ]

            if label < len(labels):
                label_text = labels[label]
            else:
                label_text = str(label)

            cv2.putText(
                overlay,
                label_text,
                (
                    bbox[0] + 10,
                    bbox[1] + 20
                ),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.5,
                255
            )

            cv2.putText(
                overlay,
                "{}%".format(
                    int(confidence * 100)
                ),
                (
                    bbox[0] + 10,
                    bbox[1] + 40
                ),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.5,
                255
            )

            # Display the distance measured at the bounding-box centre.
            distance_mm = detection.get("distance_mm")
            if distance_mm is not None:
                cv2.putText(
                    overlay,
                    "Dist: {:.2f} m".format(distance_mm / 1000.0),
                    (
                        bbox[0] + 10,
                        bbox[1] + 60
                    ),
                    cv2.FONT_HERSHEY_TRIPLEX,
                    0.5,
                    255
                )

            cv2.rectangle(
                overlay,
                (
                    bbox[0],
                    bbox[1]
                ),
                (
                    bbox[2],
                    bbox[3]
                ),
                color,
                2
            )

        return overlay


    ###############################
    # Main run function
    ###############################

    def run(self):

        ###############################
        # Model path
        ###############################

        modelPathName = (
            f'{modelsPath}/'
            f'{File_name}/'
            f'{modelName}.blob'
        )

        print("YOLO metadata:")
        print(metadata)

        nnPath = str(
            (
                Path(__file__).parent /
                Path(modelPathName)
            ).resolve().absolute()
        )

        print("Blob path:")
        print(nnPath)

        ###############################
        # Create pipeline
        ###############################

        pipeline = self.createPipeline(
            nnPath
        )

        ###############################
        # Connect to device
        ###############################

        with dai.Device() as device:

            cams = device.getConnectedCameras()

            depth_enabled = (
                dai.CameraBoardSocket.LEFT in cams
                and
                dai.CameraBoardSocket.RIGHT in cams
            )

            if (
                cam_source != "rgb"
                and
                not depth_enabled
            ):

                raise RuntimeError(
                    "Unable to run the experiment on {} "
                    "camera! Available cameras: {}".format(
                        cam_source,
                        cams
                    )
                )

            device.startPipeline(
                pipeline
            )

            ###############################
            # Output queues
            ###############################

            q_nn_input = device.getOutputQueue(
                name="nn_input",
                maxSize=2,
                blocking=False
            )

            q_nn = device.getOutputQueue(
                name="nn",
                maxSize=2,
                blocking=False
            )

            q_depth = device.getOutputQueue(
                name="depth",
                maxSize=2,
                blocking=False
            )

            frame = None
            depth_frame = None

            detections = []

            start_time = time.time()

            counter = 0

            fps = 0

            ###############################
            # Main loop
            ###############################

            while True:

                found_classes = []

                # Blocking reads are intentional here.
                # The NN passthrough stream contains the frame associated
                # with the corresponding neural-network inference.
                inRgb = q_nn_input.get()
                inDet = q_nn.get()

                # Get the latest aligned stereo-depth frame.
                # Depth is aligned to the RGB/NN image by the pipeline.
                inDepth = q_depth.tryGet()
                if inDepth is not None:
                    depth_frame = inDepth.getFrame()

                ###############################
                # Get image
                ###############################

                frame = inRgb.getCvFrame()

                ###############################
                # Get NN output
                ###############################

                # Decode raw [1,10647,7] output
                detections = self.decode_yolo(
                    inDet,
                    frame
                )

                for detection in detections:

                    found_classes.append(
                        detection["label"]
                    )

                if len(found_classes) > 0:

                    found_classes = np.unique(
                        found_classes
                    )

                else:

                    found_classes = []

                # Calculate distance to the centre of every detection.
                # The values are stored in the detection dictionary so the
                # drawing function can display them.
                for detection in detections:
                    z_mm, distance_mm = self.get_distance_to_detection_center(
                        depth_frame,
                        detection
                    )
                    detection["depth_mm"] = z_mm
                    detection["distance_mm"] = distance_mm

                overlay = self.show_yolo(
                    frame,
                    detections
                )

                ###############################
                # Display information
                ###############################

                if frame is not None:

                    cv2.putText(
                        overlay,
                        "NN fps: {:.2f}".format(fps),
                        (
                            2,
                            overlay.shape[0] - 4
                        ),
                        cv2.FONT_HERSHEY_TRIPLEX,
                        0.4,
                        (255, 0, 0)
                    )

                    cv2.putText(
                        overlay,
                        "Found classes {}".format(
                            found_classes
                        ),
                        (
                            2,
                            10
                        ),
                        cv2.FONT_HERSHEY_TRIPLEX,
                        0.4,
                        (255, 0, 0)
                    )

                    ###############################
                    # Publish ROS
                    ###############################

                    self.publish_to_ros(
                        frame
                    )

                    self.publish_detect_to_ros(
                        overlay
                    )

                    self.publish_camera_info()

                ###############################
                # FPS
                ###############################

                counter += 1

                if (
                    time.time() -
                    start_time
                ) > 1:

                    fps = (
                        counter /
                        (
                            time.time() -
                            start_time
                        )
                    )

                    counter = 0

                    start_time = time.time()


    ###############################
    # ROS image publisher
    ###############################

    def publish_to_ros(self, frame):

        msg_out = CompressedImage()

        msg_out.header.stamp = rospy.Time.now()

        msg_out.format = "jpeg"

        msg_out.header.frame_id = "home"

        msg_out.data = np.array(
            cv2.imencode(
                '.jpg',
                frame
            )[1]
        ).tostring()

        self.pub_image.publish(
            msg_out
        )

        # Publish raw image
        msg_img_raw = self.br.cv2_to_imgmsg(
            frame,
            encoding="bgr8"
        )

        self.pub_image_raw.publish(
            msg_img_raw
        )


    ###############################
    # Detection image publisher
    ###############################

    def publish_detect_to_ros(self, frame):

        msg_out = CompressedImage()

        msg_out.header.stamp = rospy.Time.now()

        msg_out.format = "jpeg"

        msg_out.header.frame_id = "home"

        msg_out.data = np.array(
            cv2.imencode(
                '.jpg',
                frame
            )[1]
        ).tostring()

        self.pub_image_detect.publish(
            msg_out
        )

        # Publish raw detection image for tools such as rqt_image_view
        msg_img_raw = self.br.cv2_to_imgmsg(
            frame,
            encoding="bgr8"
        )

        msg_img_raw.header.stamp = msg_out.header.stamp
        msg_img_raw.header.frame_id = msg_out.header.frame_id

        self.pub_image_detect_raw.publish(
            msg_img_raw
        )


    ###############################
    # Create DepthAI pipeline
    ###############################

    def createPipeline(self, nnPath):

        pipeline = dai.Pipeline()

        ###############################
        # Stereo depth
        ###############################

        # OAK-D Pro: use the left/right mono cameras to calculate depth
        # and align that depth map to the RGB camera.
        mono_left = pipeline.create(dai.node.MonoCamera)
        mono_right = pipeline.create(dai.node.MonoCamera)

        mono_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
        mono_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

        mono_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        mono_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

        mono_left.setFps(self.fps)
        mono_right.setFps(self.fps)

        stereo = pipeline.create(dai.node.StereoDepth)
        stereo.setDefaultProfilePreset(
            dai.node.StereoDepth.PresetMode.HIGH_ACCURACY
        )
        stereo.setLeftRightCheck(True)
        stereo.setSubpixel(True)
        stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)

        # Produce an aligned depth image at the same resolution as the NN.
        stereo.setOutputSize(self.nn_shape_w, self.nn_shape_h)

        mono_left.out.link(stereo.left)
        mono_right.out.link(stereo.right)

        ###############################
        # Neural network
        ###############################

        # IMPORTANT:
        #
        # Use a generic NeuralNetwork instead
        # of YoloDetectionNetwork.
        #
        # The blob exposes:
        #
        # [1, 10647, 7]
        #
        # rather than separate 52/26/13
        # YOLO output layers.

        detection_nn = pipeline.create(
            dai.node.NeuralNetwork
        )

        detection_nn.setBlobPath(
            nnPath
        )

        detection_nn.setNumPoolFrames(
            4
        )

        detection_nn.input.setBlocking(
            False
        )

        detection_nn.setNumInferenceThreads(
            2
        )

        ###############################
        # RGB camera
        ###############################

        if cam_source == 'rgb':

            cam = pipeline.create(
                dai.node.ColorCamera
            )

            cam.setPreviewSize(
                self.nn_shape_w,
                self.nn_shape_h
            )

            cam.setInterleaved(
                False
            )

            cam.preview.link(
                detection_nn.input
            )

            cam.setColorOrder(
                dai.ColorCameraProperties.ColorOrder.RGB
            )

            cam.setFps(
                self.fps
            )

            print(
                "Using RGB camera..."
            )

        ###############################
        # Mono cameras
        ###############################

        elif cam_source == 'left':

            cam = pipeline.create(
                dai.node.MonoCamera
            )

            cam.setBoardSocket(
                dai.CameraBoardSocket.LEFT
            )

            print(
                "Using BW Left cam"
            )

        elif cam_source == 'right':

            cam = pipeline.create(
                dai.node.MonoCamera
            )

            cam.setBoardSocket(
                dai.CameraBoardSocket.RIGHT
            )

            print(
                "Using BW Right cam"
            )

        ###############################
        # Resize mono image
        ###############################

        if cam_source != 'rgb':

            manip = pipeline.create(
                dai.node.ImageManip
            )

            manip.setResize(
                self.nn_shape_w,
                self.nn_shape_h
            )

            manip.setKeepAspectRatio(
                True
            )

            manip.setFrameType(
                dai.RawImgFrame.Type.RGB888p
            )

            cam.out.link(
                manip.inputImage
            )

            manip.out.link(
                detection_nn.input
            )

        ###############################
        # NN input output
        ###############################

        xout_rgb = pipeline.create(
            dai.node.XLinkOut
        )

        xout_rgb.setStreamName(
            "nn_input"
        )

        xout_rgb.input.setBlocking(
            False
        )

        # Send the exact image associated with each NN inference.
        # Using the NN passthrough keeps the frame and inference paired.
        detection_nn.passthrough.link(
            xout_rgb.input
        )

        ###############################
        # NN output
        ###############################

        xinDet = pipeline.create(
            dai.node.XLinkOut
        )

        xinDet.setStreamName(
            "nn"
        )

        xinDet.input.setBlocking(
            False
        )

        detection_nn.out.link(
            xinDet.input
        )

        ###############################
        # Aligned depth output
        ###############################

        xout_depth = pipeline.create(
            dai.node.XLinkOut
        )
        xout_depth.setStreamName("depth")
        xout_depth.input.setBlocking(False)

        stereo.depth.link(
            xout_depth.input
        )

        return pipeline


    ###############################
    # Shutdown
    ###############################

    def shutdown(self):

        cv2.destroyAllWindows()


###############################
# Main
###############################

def main():

    rospy.init_node(
        'depthai_node'
    )

    dai_cam = DepthaiCamera()

    while not rospy.is_shutdown():

        dai_cam.run()

    dai_cam.shutdown()


if __name__ == '__main__':

    main()