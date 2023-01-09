#!/usr/bin/env python
#
#
#
#Software License Agreement (JKP License; for more info go to https://www.youtube.com/watch?v=dQw4w9WgXcQ)
#
#ROS Melodic TurtleSim Custom Node

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from beginner_tutorials.msg import Num
import math
import time
from std_srvs.srv import Empty

x=0
y=0
z=0
yaw=0

# def poseCallback(pose_message):
# 	global x
# 	global y, z, yaw
# 	x = pose_message.x
# 	y = pose_message.y
# 	yaw = pose_message.theta

# def move(speed, distance, is_forward):
# 	velocity_message = Twist()
# 	global x, y
# 	x0 = x
# 	y0 = y

# 	if (is_forward):
# 		velocity_message.linear.x = abs(speed)
# 	else:
# 		velocity_message.linear.x = -abs(speed)

# 	distance_moved = 0.0
# 	loop_rate = rospy.Rate(10)
# 	cmd_vel_topic = '/turtle1/cmd_vel'
# 	velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

# 	while True:
# 		rospy.loginfo("Turtlesim moves forwards")
# 		velocity_publisher.publish(velocity_message)

# 		loop_rate.sleep()

# 		distance_moved = distance_moved + abs(0.5 * math.sqrt(((x-x0)**2) + ((y-y0)**2)))
# 		print(distance_moved)

# 		if not (distance_moved<distance):
# 			rospy.loginfo("reached")
# 			break

# 	velocity_message.linear.x = 0
# 	velocity_publisher.publish(velocity_message)

def circle(radius, velocity, direction):
    # velocity_message = Twist()
    # velocity_message.linear.x = velocity
    # velocity_message.linear.y = 0
    # velocity_message.linear.z = 0
    # velocity_message.angular.x = 0
    # velocity_message.angular.y = 0
    # velocity_message.angular.z = velocity/radius

    velocity_message = Num()
    velocity_message.radius = radius
    velocity_message.velocity = velocity
    velocity_message.direction = direction
    
    loop_rate = rospy.Rate(10)
    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Num, queue_size=10)

    while True:
        rospy.loginfo("Turtle moves in a circle")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()


# def rotate(angular_speed_degree, relative_angle_degree, clockwise):

# 	global yaw
# 	velocity_message = Twist()
# 	velocity_message.linear.x = 1
# 	velocity_message.linear.y = 0
# 	velocity_message.linear.z = 0
# 	velocity_message.angular.x = 0
# 	velocity_message.angular.y = 0
# 	velocity_message.angular.z = 0

# 	theta0 = yaw
# 	angular_speed = math.radians(abs(angular_speed_degree))

# 	if (clockwise):
# 		velocity_message.angular.z = -abs(angular_speed)
# 	else:
# 		velocity_message.angular.z = abs(angular_speed)

# 	angle_moved = 0.0
# 	loop_rate = rospy.Rate(10)
# 	cmd_vel_topic = '/turtle1/cmd_vel'
# 	velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

# 	t0 = rospy.Time.now().to_sec()

# 	while True:
# 		rospy.loginfo("Turtlesim rotates")
# 		velocity_publisher.publish(velocity_message)

# 		t1 = rospy.Time.now().to_sec()
# 		current_angle_degree = (t1-t0)*angular_speed_degree
# 		loop_rate.sleep()

# 		if (current_angle_degree > relative_angle_degree):
# 			rospy.loginfo("reached")
# 			break

# 	velocity_message.angular.z = 0
# 	velocity_publisher.publish(velocity_message)

# def go_to_goal(x_goal, y_goal):
# 	global x
# 	global y, z, yaw

# 	velocity_message = Twist()
# 	cmd_vel_topic = '/turtle1/cmd_vel'

# 	while True:
# 		K_linear: 

# def setDesiredOrientation(desired_angle_radians):
# 	relative_angle_radians = desired_angle_radians - yaw
# 	if relative_angle_radians < 0:
# 		clockwise = 1
# 	else:
# 		clockwise = 0
# 	print(relative_angle_radians)
# 	print(desired_angle_radians)
# 	rotate(30, math.degrees(abs(relative_angle_radians)), clockwise)

if __name__ == '__main__':
	try:

		rospy.init_node('turtlesim_advanced')

		cmd_vel_topic = '/turtle1/cmd_vel'

		velocity_publisher = rospy.Publisher(cmd_vel_topic, Num, queue_size = 10)

		# position_topic = "/turtle1/pose"
		# pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
		time.sleep(2)
		
		circle(4,5,1)

	except rospy.ROSInterruptException:
		rospy.loginfo("node terminated.")

# import rospy
# from geometry_msgs.msg import Twist
# import sys
 
 
# def turtle_circle(radius):
#     rospy.init_node('turtlesim', anonymous=True)
#     pub = rospy.Publisher('/turtle1/cmd_vel',
#                           Twist, queue_size=10)
#     rate = rospy.Rate(10)
#     vel = Twist()
#     while not rospy.is_shutdown():
#         vel.linear.x = radius
#         vel.linear.y = 0
#         vel.linear.z = 0
#         vel.angular.x = 0
#         vel.angular.y = 0
#         vel.angular.z = 1
#         rospy.loginfo("Radius = %f",
#                       radius)
#         pub.publish(vel)
#         rate.sleep()
 
 
# if __name__ == '__main__':
#     try:
#         turtle_circle(float(sys.argv[1]))
#     except rospy.ROSInterruptException:
#         pass		










