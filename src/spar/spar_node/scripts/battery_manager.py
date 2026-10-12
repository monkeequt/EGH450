#!/usr/bin/env python3

"""
Common battery source for emulator and physical UAV operation.

Common output used by the landing/guidance node:
    /uav/battery

Automatic inputs:
    /mavros/battery   -> physical UAV
    /uavasr/battery   -> UAVASR emulator

Physical MAVROS telemetry always has priority when it is present.

For emulator testing, the simulated battery can be configured to reach the
same failsafe threshold used by guidance after an exact amount of airborne
time. For example, with:

    battery_threshold = 0.15
    emulator_time_to_threshold_seconds = 60.0

the simulated battery is 15% at 60 seconds of airborne time.

Set emulator_time_to_threshold_seconds to 0.0 to disable artificial emulator
discharge and pass the emulator battery percentage through unchanged.
"""

import copy
import math

import rospy

from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import BatteryState


class BatteryManager:
    def __init__(self):

        # Common output consumed by landing in BOTH environments.
        self.output_topic = rospy.get_param("~output_topic", "/uav/battery")

        # Automatic source topics.
        self.mavros_topic = rospy.get_param("~mavros_topic", "/mavros/battery")
        self.emulator_topic = rospy.get_param("~emulator_topic", "/uavasr/battery")
        self.emulator_pose_topic = rospy.get_param(
            "~emulator_pose_topic",
            "/uavasr/pose"
        )

        # A recent MAVROS message means this is physical flight.
        self.physical_timeout = rospy.get_param("~physical_timeout", 2.0)
        self.last_physical_msg_time = rospy.Time(0)

        # The same threshold used by the guidance failsafe.
        # BatteryState.percentage is in the range 0.0 to 1.0.
        self.battery_threshold = rospy.get_param("~battery_threshold", 0.15)

        # Emulator battery profile.
        # This is the exact AIRBORNE time at which the simulated battery reaches
        # battery_threshold. Set to 0.0 to disable artificial emulator discharge.
        self.emulator_time_to_threshold_seconds = rospy.get_param(
            "~emulator_time_to_threshold_seconds",
            360.0
        )
        self.emulator_airborne_altitude = rospy.get_param(
            "~emulator_airborne_altitude",
            0.20
        )

        if not 0.0 < self.battery_threshold < 1.0:
            raise ValueError(
                "~battery_threshold must be between 0.0 and 1.0, exclusive"
            )

        if self.emulator_time_to_threshold_seconds < 0.0:
            raise ValueError(
                "~emulator_time_to_threshold_seconds must be >= 0.0"
            )

        self.emulator_start_time = None
        self.emulator_airborne = False

        # Log source selection once only.
        self.reported_physical_source = False
        self.reported_emulator_source = False

        self.pub_battery = rospy.Publisher(
            self.output_topic,
            BatteryState,
            queue_size=1,
            latch=True
        )

        self.sub_physical = rospy.Subscriber(
            self.mavros_topic,
            BatteryState,
            self.callback_physical,
            queue_size=1
        )

        self.sub_emulator = rospy.Subscriber(
            self.emulator_topic,
            BatteryState,
            self.callback_emulator,
            queue_size=1
        )

        self.sub_emulator_pose = rospy.Subscriber(
            self.emulator_pose_topic,
            PoseStamped,
            self.callback_emulator_pose,
            queue_size=1
        )

        rospy.loginfo(
            "Battery manager ready. Common output: %s",
            self.output_topic
        )

        if self.emulator_time_to_threshold_seconds > 0.0:
            rospy.loginfo(
                "Emulator battery profile: %.1f%% after %.1f airborne seconds.",
                self.battery_threshold * 100.0,
                self.emulator_time_to_threshold_seconds
            )
        else:
            rospy.loginfo(
                "Artificial emulator battery discharge disabled; "
                "passing emulator percentage through unchanged."
            )

    def physical_is_recent(self):
        if self.last_physical_msg_time == rospy.Time(0):
            return False

        age = (rospy.Time.now() - self.last_physical_msg_time).to_sec()
        return age <= self.physical_timeout

    def callback_emulator_pose(self, msg_in):
        # This callback only starts the EMULATED discharge timer.
        # It has no effect on physical MAVROS battery telemetry.
        if self.physical_is_recent():
            return

        if (
            not self.emulator_airborne and
            msg_in.pose.position.z >= self.emulator_airborne_altitude
        ):
            self.emulator_airborne = True
            self.emulator_start_time = rospy.Time.now()

            if self.emulator_time_to_threshold_seconds > 0.0:
                rospy.loginfo(
                    "UAV airborne. Starting simulated battery discharge; "
                    "%.1f%% will be reached after %.1f seconds.",
                    self.battery_threshold * 100.0,
                    self.emulator_time_to_threshold_seconds
                )

    def callback_physical(self, msg_in):
        # Real flight-controller telemetry always wins whenever available.
        self.last_physical_msg_time = rospy.Time.now()

        if not self.reported_physical_source:
            rospy.loginfo("Battery source selected: MAVROS physical UAV.")
            self.reported_physical_source = True

        msg_out = copy.deepcopy(msg_in)
        msg_out.header.stamp = rospy.Time.now()

        self.pub_battery.publish(msg_out)

        if math.isnan(msg_out.percentage) or msg_out.percentage < 0.0:
            rospy.logwarn_throttle(
                10.0,
                "MAVROS battery percentage is unavailable."
            )

    def callback_emulator(self, msg_in):
        # Never overwrite active physical telemetry with emulator data.
        if self.physical_is_recent():
            return

        if not self.reported_emulator_source:
            rospy.loginfo("Battery source selected: UAVASR emulator.")
            self.reported_emulator_source = True

        msg_out = copy.deepcopy(msg_in)
        msg_out.header.stamp = rospy.Time.now()

        if self.emulator_time_to_threshold_seconds > 0.0:
            if not self.emulator_airborne or self.emulator_start_time is None:
                # Do not consume simulated battery before the UAV is airborne.
                msg_out.percentage = 1.0
            else:
                elapsed = (
                    rospy.Time.now() - self.emulator_start_time
                ).to_sec()

                # Linear discharge selected so that:
                #
                #   percentage(0) = 1.0
                #   percentage(T) = battery_threshold
                #
                # where T = emulator_time_to_threshold_seconds.
                # After T it continues at the same rate toward 0%.
                discharge_rate = (
                    (1.0 - self.battery_threshold) /
                    self.emulator_time_to_threshold_seconds
                )

                msg_out.percentage = max(
                    0.0,
                    1.0 - (elapsed * discharge_rate)
                )

        self.pub_battery.publish(msg_out)


if __name__ == "__main__":
    rospy.init_node("battery_manager")
    BatteryManager()
    rospy.spin()
