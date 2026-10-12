#!/usr/bin/env python3

import cv2
import depthai as dai
import rospy
from visualization_msgs.msg import Marker
from sensor_msgs.msg import CompressedImage # poosibly delete
from cv_bridge import CvBridge, CvBridgeError


import numpy as np


class ArucoDetector():
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
    aruco_params = cv2.aruco.DetectorParameters()

    frame_sub_topic = '/depthai_node/image/compressed'

    def __init__(self):
    
        self.camera_name = rospy.get_param("~camera_name", "camera")
    
        # Processed image
        self.aruco_image_pub = rospy.Publisher('/processed_aruco/image/compressed', CompressedImage, queue_size=10)
        # Marker ID and SolvePNP position
        self.aruco_pose_pub = rospy.Publisher(
            '/aruco_detection/pose',
            Marker,
            queue_size=5
        )
         

        self.br = CvBridge()

        if not rospy.is_shutdown():
            self.frame_sub = rospy.Subscriber(
                self.frame_sub_topic, CompressedImage, self.img_callback, queue_size=10, buff_size=2**24, tcp_nodelay=True )

    def img_callback(self, msg_in):
        try:
            frame = self.br.compressed_imgmsg_to_cv2(msg_in)
        except CvBridgeError as e:
            rospy.logerr(e)

        aruco = self.find_aruco(frame)
        self.publish_to_ros(aruco)

        # cv2.imshow('aruco', aruco)
        # cv2.waitKey(1)

    def find_aruco(self, frame):
        (corners, ids, _) = cv2.aruco.detectMarkers(
            frame, self.aruco_dict, parameters=self.aruco_params)

        if len(corners) > 0:
            ids = ids.flatten()

            for (marker_corner, marker_ID) in zip(corners, ids):
                corners = marker_corner.reshape((4, 2))
                (top_left, top_right, bottom_right, bottom_left) = corners

                top_right = (int(top_right[0]), int(top_right[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
                top_left = (int(top_left[0]), int(top_left[1]))

                line1 = [bottom_left, top_right]
                line2 = [top_left, bottom_right]

                xdiff = ((line1[0][0] - line1[1][0]), (line2[0][0] - line2[1][0]))
                ydiff =  ((line1[0][1] - line1[1][1]), (line2[0][1] - line2[1][1]))
                def det(a,b):
                    return a[0]*b[1] - a[1]*b[0]   

                div = (det(xdiff,ydiff))
                d = (det(*line1),det(*line2))
                x = int(det(d,xdiff)/div)
                y = int(det(d,ydiff)/div)
                center = ((x),(y))

                cv2.circle(frame,(x, y),1,(0,128,255),5)
                
                cv2.line(frame, top_left, top_right, (0, 255, 0), 2)
                cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
                cv2.line(frame, bottom_right, bottom_left, (0, 255, 0), 2)
                cv2.line(frame, bottom_left, top_left, (0, 255, 0), 2)
                
                object_points = np.array([
                    [-0.01,0.01,0.0], # Top-Left
                    [0.01,0.01,0.0], # Top-Right
                    [-0.01,-0.01,0.0], # Bottom-left
                    [0.01,-0.01,0.0], # Bottom-Right
                    [0.0,0.0,0.0] #center

                ], dtype=float)

                image_points = np.array([
                    [top_left],
                    [top_right],
                    [bottom_left],
                    [bottom_right],                 
                    [center]
                ],dtype = float)

                camera_matrix = np.array([
                    [3.25093799e+03,0.0,2.03031531e+03],
                    [0.0,3.25093799e+03,1.54433728e+03],
                    [0.0,0.0,1.0]
                ])

                distortion_coefficients = np.zeros(5)

                # Solve for pose using SOLVEPNP_ITERATIVE
                success, rotation_vector, translation_vector = cv2.solvePnP(
                    object_points, image_points, camera_matrix, distortion_coefficients, flags=cv2.SOLVEPNP_ITERATIVE
                )
                
                # added by ANS if you have questions 
                # Publish detected ArUco ID and camrea-relative XYZ
                if success:
                    marker_msg = Marker()
                    
                    marker_msg.header.stamp = rospy.Time.now()
                    marker_msg.header.frame_id = self.camera_name
                    
                    marker_msg.id = int(marker_ID)
                    
                    marker_msg.pose.position.x = -float(translation_vector[0][0])
                    marker_msg.pose.position.y = -float(translation_vector[1][0])
                    marker_msg.pose.position.z = -float(translation_vector[2][0])
                    
                    marker_msg.pose.orientation.x = 0.0
                    marker_msg.pose.orientation.y = 0.0
                    marker_msg.pose.orientation.z = 0.0
                    marker_msg.pose.orientation.w = 1.0
                    
                    self.aruco_pose_pub.publish(marker_msg)

                #distance_from_camera = std::sqrt(translation_vector[0]*translation_vector[0]+translation_vector[1]*translation_vector[1]+translation_vector[2]*translation_vector[2]) 
                distance_from_camera = ((translation_vector[0]**2)+(translation_vector[1]**2)+(translation_vector[2]**2)) ** 0.5

                rospy.loginfo("Aruco detected, ID: {}".format(marker_ID))
                rospy.loginfo("Distance to marker: {}".format(distance_from_camera))

                cv2.putText(frame, str(
                    marker_ID), (top_left[0], top_right[1] - 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(frame, str(
                    center), (top_left[0], top_right[1] - 40), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(frame, str(
                    distance_from_camera), (top_left[0], top_right[1] - 60), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)

        return frame

    def publish_to_ros(self, frame):
        msg_out = CompressedImage()
        msg_out.header.stamp = rospy.Time.now()
        msg_out.format = "jpeg"
        msg_out.data = np.array(cv2.imencode('.jpg', frame)[1]).tostring()
        
        self.aruco_image_pub.publish(msg_out)


def main():
    rospy.init_node('EGB349_vision', anonymous=True)
    rospy.loginfo("Processing images...")

    aruco_detect = ArucoDetector()

    rospy.spin()
