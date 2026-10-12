#!/usr/bin/env python3

import rospy
import tf2_ros

from geometry_msgs.msg import TransformStamped


def main():

    rospy.init_node("camera_to_uav")

    # Static TF broadcaster
    broadcaster = tf2_ros.StaticTransformBroadcaster()

    transform = TransformStamped()

    # Parent frame
    transform.header.frame_id = "uav"

    # Child frame
    transform.child_frame_id = "camera"

    # Camera position relative to UAV
    transform.transform.translation.x = -0.125
    transform.transform.translation.y = 0.0
    transform.transform.translation.z = 0.1

    # No rotation
    transform.transform.rotation.x = 0.0
    transform.transform.rotation.y = 0.0
    transform.transform.rotation.z = 0.0
    transform.transform.rotation.w = 1

    # Publish static transform
    broadcaster.sendTransform(transform)

    rospy.loginfo(
        "Published camera -> UAV offset: "
        "x=-0.125 m, y=0 m, z=0.1 m"
    )

    rospy.spin()


if __name__ == "__main__":
    main()