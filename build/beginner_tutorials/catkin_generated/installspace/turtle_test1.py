#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from beginner_tutorials.msg import Num
import math
import time
from std_srvs.srv import Empty


class Calc:
    def __init__(self):
        rospy.Subscriber("/new_command", Num, self.first_topic_callback)
        self.pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
        
        self.linear.x = 0
        self.linear.y = 0
        self.linear.z = 0
        self.angular.x = 0
        self.angular.y = 0
        self.angular.z = 0

        # self.radius = 0
        # self.velocity = 0
        # self.direction = 0
        
    # 퍼블리셔 노드로부터 토픽을 받아들이는 콜백 함수
    def first_topic_callback(self, data):
        self.linear.x = data.velocity
        self.linear.y = 0
        self.linear.z = 0
        self.angular.x = 0
        self.angular.y = 0
        self.angular.z = data.velocity / data.radius

        # 받은 내용(data)를 터미널에 출력
        rospy.loginfo("------")

    def second_msg_publish(self):
        msg = Twist()	# 메시지 변수 선언

        # 메시지 내용 담기
        ## start_time: start_node가 메시지를 생성해 publish 하는 시각
        ## msg_seq: 메시지 순서(번호)
        ## original_num: 계산의 대상이 될 수
        ## square_num: original_num의 제곱
        ## sqrt_num: original_num의 제곱근
        msg.linear.x = self.linear.x
        msg.linear.y = self.linear.y
        msg.linear.z = self.linear.z
        msg.angular.x = self.angular.x
        msg.angular.y = self.angular.y
        msg.angular.z = self.angular.z

        self.pub.publish(msg)
    
def main():
    # 노드 초기화.
    rospy.init_node('publishernode', anonymous=False)
    rate = rospy.Rate(1)

    calc = Calc()
    while not rospy.is_shutdown():
        calc.second_msg_publish()
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass