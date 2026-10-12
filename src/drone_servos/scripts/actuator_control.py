#!/usr/bin/env python3
import rospy
import RPi.GPIO as GPIO
from std_msgs.msg import Bool
import time
#test
sub_1 = None
sub_2 = None
chan_list = [12, 13]

def move_servo(pin, is_180):
	duty = 12.5 if is_180 else 2.5
	angle = "180" if is_180 else "0"

	rospy.loginfo(f"Setting pin {pin} to {angle} degrees!")
	
	pwm = GPIO.PWM(pin, 50)
	pwm.start(0)
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)
	pwm.stop()

def callback_1(msg_in):
	move_servo(chan_list[0], msg_in.data)

def callback_2(msg_in):
	move_servo(chan_list[1], msg_in.data)

def shutdown():
	if sub_1 is not None:
		sub_1.unregister()
	if sub_2 is not None:
		sub_2.unregister()

	GPIO.cleanup()

if __name__ == '__main__':
	rospy.init_node('actuator_controller', anonymous=True)

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(chan_list, GPIO.OUT)

	sub_1 = rospy.Subscriber('/actuator_control/servo1', Bool, callback_1)
	sub_2 = rospy.Subscriber('/actuator_control/servo2', Bool, callback_2)

	rospy.on_shutdown(shutdown)

	rospy.loginfo("Servo's ready")

	rospy.spin()