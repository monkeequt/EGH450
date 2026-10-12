#!/usr/bin/env python3

import copy

import rospy
import tf2_ros
import tf2_geometry_msgs

from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Int32MultiArray, String


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
            queue_size=5
        )

        # Publish the latest transformed detection while preserving its ID.
        self.world_marker_publisher = rospy.Publisher(
            "/aruco_detection/world_marker",
            Marker,
            queue_size=5
        )

        # Latched topics immediately give new RViz/subscriber instances the
        # complete set of markers found so far.
        self.marker_array_publisher = rospy.Publisher(
            "/aruco_detection/world_markers",
            MarkerArray,
            queue_size=1,
            latch=True
        )
        self.unique_ids_publisher = rospy.Publisher(
            "/aruco_detection/unique_ids",
            Int32MultiArray,
            queue_size=1,
            latch=True
        )

        # Publish a text message for speech/vocalisation when an ArUco is detected
        self.chatter_publisher = rospy.Publisher(
            "/chatter",
            String,
            queue_size=5
        )

        # marker_id -> most recently transformed world pose
        self.unique_markers = {}

        self.marker_scale = rospy.get_param("~marker_scale", 0.15)
        self.update_existing = rospy.get_param("~update_existing", True)

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
                "map",
                rospy.Duration(0.5)
            )

            # Publish result
            self.world_publisher.publish(pose_world)

            marker_id = msg.id
            is_new = marker_id not in self.unique_markers

            # Only vocalise the first detection of each unique ArUco marker.
            if is_new:
                chatter_msg = String()
                chatter_msg.data = "ArUco marker {} detected".format(marker_id)
                self.chatter_publisher.publish(chatter_msg)

            if is_new or self.update_existing:
                self.unique_markers[marker_id] = pose_world

            self.world_marker_publisher.publish(
                self.make_sphere_marker(marker_id, pose_world)
            )

            # Re-publish the collection when a marker is first found, or when
            # an existing marker's stored pose has been updated.
            if is_new or self.update_existing:
                self.publish_unique_markers()

            rospy.loginfo_throttle(
                1.0,
                "ArUco %d world position: "
                "x=%.3f, y=%.3f, z=%.3f",
                marker_id,
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

    def make_sphere_marker(self, marker_id, pose_world):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "aruco_points"
        marker.id = marker_id
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose = copy.deepcopy(pose_world.pose)
        marker.scale.x = self.marker_scale
        marker.scale.y = self.marker_scale
        marker.scale.z = self.marker_scale
        marker.color.r = 0.1
        marker.color.g = 0.8
        marker.color.b = 1.0
        marker.color.a = 1.0
        marker.lifetime = rospy.Duration(0)
        return marker

    def make_text_marker(self, marker_id, pose_world):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "aruco_labels"
        marker.id = marker_id
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        marker.pose = copy.deepcopy(pose_world.pose)
        marker.pose.position.z += self.marker_scale
        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 1.0
        marker.scale.z = self.marker_scale
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 1.0
        marker.text = "ArUco {}".format(marker_id)
        marker.lifetime = rospy.Duration(0)
        return marker

    def publish_unique_markers(self):
        marker_array = MarkerArray()

        for marker_id in sorted(self.unique_markers):
            pose_world = self.unique_markers[marker_id]
            marker_array.markers.append(
                self.make_sphere_marker(marker_id, pose_world)
            )
            marker_array.markers.append(
                self.make_text_marker(marker_id, pose_world)
            )

        self.marker_array_publisher.publish(marker_array)
        self.unique_ids_publisher.publish(
            Int32MultiArray(data=sorted(self.unique_markers.keys()))
        )


if __name__ == "__main__":

    try:
        ArucoNavigation()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
