#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

from espeak import espeak

def callback(msg_in):
    text = msg_in.data
    espeak.synth(text)
    rospy.loginfo(text)
    
if __name__ == "__main__":

    rospy.init_node('synth')
    pub = rospy.Subscriber("chatter", String, callback)
    
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
