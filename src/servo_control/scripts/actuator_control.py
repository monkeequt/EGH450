#!/usr/bin/env python3

#importing the required libraries
import rospy    				#ROS library for Python
import RPi.GPIO as GPIO			#Library for controlling GPIO pins on Raspberry Pi
from std_msgs.msg import Bool	#ROS message type for boolean values
import time						#Library for time-related functions i use this for time delays


#initializing subsciber variables
sub_1 = None
sub_2 = None

#GPIO pin numbers for the servos
chan_list = [12, 13]

def move_servo(pin, is_180):

	#duty sets duty cycle to 12.5 if the message recived is true, closing the servo. This is done manually
	#when false is recived, the duty cycle is set to 2.5, opening the servo. This is done autonomously during flight
	#the name is_180 is legacy name carried from a script i made in sem 1 using string values rather than boolean. 
	duty = 12.5 if is_180 else 2.5 	

	angle = "180" if is_180 else "0"	#angle is used for logging purposes

	rospy.loginfo(f"Setting pin {pin} to {angle} degrees!")	#displaying the angle and pin number in the terminal for debugging purposes
	
	#initializing PWN on pin to 50Hz
	pwm = GPIO.PWM(pin, 50)
	pwm.start(0)				#starts PWM without sending signal 

	pwm.ChangeDutyCycle(duty)	#sets duty cycle to move servo to desired angle
	time.sleep(1)				#Gives the servo time to move before stopping the signal
	pwm.stop()


#called when a boolean message is recieved from below. 
#passes the pin number assosiate with the servo and the boolean value to move_servo functiod
def callback_1(msg_in):
	move_servo(chan_list[0], msg_in.data)

def callback_2(msg_in):
	move_servo(chan_list[1], msg_in.data)

#Cleans the ROS subscriber if they were set, avoids messages in logs
#from tutorial 3
def shutdown():
	if sub_1 is not None:
		sub_1.unregister()
	if sub_2 is not None:
		sub_2.unregister()

	GPIO.cleanup()

if __name__ == '__main__':
	rospy.init_node('actuator_controller', anonymous=True)	#initializes the ROS node with the name actuator_controller,
															#anonymous allows multiple nodes to run with the same name
															#This may be redundant but I left it in after using for debugging

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(chan_list, GPIO.OUT)

	#subrsibing to ROS topics to allow control
	#listens for boolean messages from terminal for manual control and from the control scripts for autonomous control
	sub_1 = rospy.Subscriber('/actuator_control/servo1', Bool, callback_1)	#servo 1 deploys on fire, this is arbitrary and can be changed inside the control scripts
	sub_2 = rospy.Subscriber('/actuator_control/servo2', Bool, callback_2)	#servo 2 deploys on smoke, this is arbitrary and can be changed inside the control scripts

	#nessisary shutdown function
	rospy.on_shutdown(shutdown)

	#debugging, indicates script is working
	rospy.loginfo("Servo's ready")

	#keeps script awake
	rospy.spin()