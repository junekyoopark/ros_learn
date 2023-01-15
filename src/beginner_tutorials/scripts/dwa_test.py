#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Software License Agreement (JKP License; for more info go to https://www.youtube.com/watch?v=dQw4w9WgXcQ)
#ROS Melodic TurtleSim Custom Node (Utilizing DWA algorithm)

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import dynamic_window_approach as dwa
import math
import time
from std_srvs.srv import Empty
import numpy as np

# Logic
# dwa_test node subscribes to /turtleX/Pose topic (both turtle1 and turtle2)
# dwa_test node does some processing (the DWA algorithm is run)
# dwa_test node publishes the processed data (message) to /turtleX/cmd_vel

#Config for DWA algorithm, copied from dynamic_window_approach.py
class Config:
    """
    simulation parameter class
    """

    def __init__(self):
        # robot parameter
        self.max_speed = 1.0  # [m/s]
        self.min_speed = -0.5  # [m/s]
        self.max_yaw_rate = 40.0 * math.pi / 180.0  # [rad/s]
        self.max_accel = 0.2  # [m/ss]
        self.max_delta_yaw_rate = 40.0 * math.pi / 180.0  # [rad/ss]
        self.v_resolution = 0.01  # [m/s]
        self.yaw_rate_resolution = 0.1 * math.pi / 180.0  # [rad/s]
        self.dt = 0.1  # [s] Time tick for motion prediction
        self.predict_time = 3.0  # [s]
        self.to_goal_cost_gain = 0.15
        self.speed_cost_gain = 1.0
        self.obstacle_cost_gain = 1.0
        self.robot_stuck_flag_cons = 0.001  # constant to prevent robot stucked
        # self.robot_type = RobotType.circle

        # if robot_type == RobotType.circle
        # Also used to check if goal is reached in both types
        self.robot_radius = 0.5  # [m] for collision check

        # if robot_type == RobotType.rectangle
        self.robot_width = 0.5  # [m] for collision check
        self.robot_length = 1.2  # [m] for collision check
        # obstacles [x(m) y(m), ....]
        self.ob = np.empty((1,2))

        #additional obstacles (fine tuning)
        #set walls as obstacles too
        #x and y values of coordinates
        xvalues = np.arange(0, 11.5, 0.01)
        yvalues = np.arange(0, 11.5, 0.01)
        #set meshgrid
        self.ob_wall_mgrid = np.meshgrid(xvalues, yvalues)
        #select the boundaries of the mesh (the boundary of the window) using np.where
        self.ob_wall_bottom = np.where(self.ob_wall_mgrid[1]== 1.0)
        #rearrange into obstacles format
        self.ob_wall_bottom = (np.stack((self.ob_wall_bottom[0],self.ob_wall_bottom[1]), axis=1))
        #repeat for other 3 sides
        self.ob_wall_top = np.where(self.ob_wall_mgrid[1]==10.0)
        self.ob_wall_top = (np.stack((self.ob_wall_top[0],self.ob_wall_top[1]), axis=1))
        self.ob_wall_left = np.where(self.ob_wall_mgrid[0]==1.0)
        self.ob_wall_left = (np.stack((self.ob_wall_left[0],self.ob_wall_left[1]), axis=1))
        self.ob_wall_right = np.where(self.ob_wall_mgrid[0] == 10.0)
        self.ob_wall_right = (np.stack((self.ob_wall_right[0],self.ob_wall_right[1]), axis=1))
        #concatenate the 4 walls into one array
        self.ob_wall_list = np.concatenate((self.ob_wall_bottom, self.ob_wall_top, self.ob_wall_left, self.ob_wall_right), axis=0)

        #waypoints to hit (과제에서 주어진 값들)
        self.waypoints = np.array([[8.58, 2.5],
                          [2.5, 8.58],
                          [2.5, 2.5],
                          [8.58, 8.58]
                          ])
    @property
    def robot_type(self):
        return self._robot_type

    @robot_type.setter
    def robot_type(self, value):
        if not isinstance(value, RobotType):
            raise TypeError("robot_type must be an instance of RobotType")
        self._robot_type = value

#Processing Data (Main part)
class Process:
    def __init__(self):
        #subscribing to the pose topic of the obstacle 
        self.obstacle_sub = rospy.Subscriber("/turtle1/pose", Pose, self.obstacle_callback)
        
        #subscribing to the pose topic of the turtle we want to move
        self.moving_sub = rospy.Subscriber("/turtle2/pose", Pose, self.turtle2_pose_callback)

        #publishing to the cmd_vel topic of hte turtle we want to move
        self.moving_pub = rospy.Publisher("/turtle2/cmd_vel", Twist, queue_size = 10)

        #load the Config from above
        self.config = Config()

        #counter for hit waypoints
        self.waypoint_index = 0

        #init cmd_vel variables
        self.turtle2_cmd_vel_x = 0
        self.turtle2_cmd_vel_ang_z=0

        #init pose variables
        self.turtle2_pose_x = 0
        self.turtle2_pose_y = 0
        self.turtle2_pose_theta = 0
        self.turtle2_pose_lin_velocity = 0
        self.turtle2_pose_ang_velocity = 0

    #callback function that puts obstacle information into Config.ob
    #(in this case the data is turtle1/Pose)
    def obstacle_callback(self, data):
        self.config.ob = np.array([[data.x, data.y]])

    #callback function that puts pose information into 'turtle2_pose'
    #rosmsg info turtlesim/Pose (to get info about msg structure)
    def turtle2_pose_callback(self, data):
        self.turtle2_pose_x = data.x
        self.turtle2_pose_y = data.y
        self.turtle2_pose_theta = data.theta
        self.turtle2_pose_lin_velocity = data.linear_velocity
        self.turtle2_pose_ang_velocity = data.angular_velocity


    def run_dwa(self):
        #concatenate the turtle1 position and the 4 sides for obstacles
        obstacle = np.concatenate((self.config.ob,self.config.ob_wall_list))

        #loop waypoints (return to first waypoint after hitting last waypoint)
        # if self.waypoint_index == len(self.config.waypoints):
        #     self.waypoint_index = 0

        #set goal as waypoint
        goal = self.config.waypoints[self.waypoint_index]

        #setting new waypoint if a waypoint is hit
        #referred to chanjoon senpai's code
        #https://github.com/ChanJoon/turtlesim_dwa_planner/blob/main/script/main.py
        dist_to_goal = math.hypot(self.turtle2_pose_x - goal[0], self.turtle2_pose_y - goal[1])
        if dist_to_goal <= self.config.robot_radius:
            print("----------[ Waypoint Hit ]----------")
            self.waypoint_index += 1

        #the variable x in dynamic_window_approach.py file is an array of:
        self.x = np.array([self.turtle2_pose_x, self.turtle2_pose_y, self.turtle2_pose_theta, self.turtle2_pose_lin_velocity, self.turtle2_pose_ang_velocity])


        #call the dwa_control function from dynamic_window_approach.py
        u, trajectory = dwa.dwa_control(self.x, self.config, goal, obstacle)

        self.turtle2_cmd_vel_x = u[0]
        self.turtle2_cmd_vel_ang_z = u[1]



    def publish_cmd_vel(self):
        self.run_dwa()
        msg = Twist()
        msg.linear.x = self.turtle2_cmd_vel_x
        msg.angular.z = self.turtle2_cmd_vel_ang_z
        self.moving_pub.publish(msg)

        rospy.loginfo("\nCurrent pose x: %.2f, y: %.2f", self.turtle2_pose_x, self.turtle2_pose_y)
        # print("Goal    pose x: {}, y: {}".format(self.run_dwa.goal[0], self.run_dwa.goal[1]))
        print("\nlinear\n   x: {}\nangular\n   z: {}\n".format(msg.linear.x, msg.angular.z))

        
    
def main():
    # 노드 초기화.
    rospy.init_node('dwa_process_node', anonymous=False)
    rate = rospy.Rate(1)

    process = Process()
    while not rospy.is_shutdown():
        process.publish_cmd_vel()
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass