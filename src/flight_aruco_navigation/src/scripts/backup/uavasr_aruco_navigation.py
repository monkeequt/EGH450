#!/usr/bin/env python3

import rospy
import tf2_ros
import tf2_geometry_msgs

from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped


class ArucoNavigation:

    def __init__(self):

        rospy.init_node("uavasr_aruco_navigation")

        # TF2 buffer
        self.tf_buffer = tf2_ros.Buffer()

        # TF2 listener
        self.tf_listener = tf2_ros.TransformListener(
            self.tf_buffer
        )

        # Subscribe to ArUco marker pose
        self.aruco_subscriber = rospy.Subscriber(
            "/aruco_detection/pose",
            Marker,
            self.aruco_callback
        )

        # Publish ArUco position in global frame
        self.world_publisher = rospy.Publisher(
            "/aruco_detection/world_pose",
            PoseStamped,
            queue_size=10
        )

        rospy.loginfo("ArUco navigation node started")

    def aruco_callback(self, msg):

        # Create PoseStamped from the Marker message
        pose_camera = PoseStamped()

        pose_camera.header = msg.header
        pose_camera.pose = msg.pose

        # The ArUco position is relative to the camera
        pose_camera.header.frame_id = "camera"

        try:

            # Transform from camera frame to OptiTrack world frame
            pose_world = self.tf_buffer.transform(
                pose_camera,
                "optitrack_world",
                rospy.Duration(0.5)
            )

            # Publish result
            self.world_publisher.publish(pose_world)

            rospy.loginfo_throttle(
                1.0,
                "ArUco world position: "
                "x=%.3f, y=%.3f, z=%.3f",
                pose_world.pose.position.x,
                pose_world.pose.position.y,
                pose_world.pose.position.z
            )

        except (
            tf2_ros.LookupException,
            tf2_ros.ConnectivityException,
            tf2_ros.ExtrapolationException
        ) as error:

            rospy.logwarn_throttle(
                2.0,
                "Could not transform ArUco pose: %s",
                str(error)
            )


if __name__ == "__main__":

    try:
        ArucoNavigation()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass