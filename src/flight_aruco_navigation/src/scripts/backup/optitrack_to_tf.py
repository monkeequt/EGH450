#!/usr/bin/env python3

import rospy
import tf2_ros

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TransformStamped


class OptiTrackTF:

    def __init__(self):

        rospy.init_node("optitrack_to_tf")

        # TF broadcaster
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()

        # Subscribe to OptiTrack UAV pose
        self.pose_subscriber = rospy.Subscriber(
            "/uavasr/pose",
            PoseStamped,
            self.pose_callback
        )

        rospy.loginfo("OptiTrack TF broadcaster started")

    def pose_callback(self, msg):

        transform = TransformStamped()

        # Use the timestamp from OptiTrack
        transform.header.stamp = msg.header.stamp

        # Parent frame
        transform.header.frame_id = "optitrack_world"

        # Child frame
        transform.child_frame_id = "uav"

        # UAV position
        transform.transform.translation.x = msg.pose.position.x
        transform.transform.translation.y = msg.pose.position.y
        transform.transform.translation.z = msg.pose.position.z

        # UAV orientation
        transform.transform.rotation = msg.pose.orientation

        # Publish TF
        self.tf_broadcaster.sendTransform(transform)


if __name__ == "__main__":

    try:
        OptiTrackTF()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
