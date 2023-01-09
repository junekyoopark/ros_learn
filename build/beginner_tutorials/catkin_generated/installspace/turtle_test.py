#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from beginner_tutorials.msg import Num
import math
import time
from std_srvs.srv import Empty

def circle(radius, velocity, direction):
    new_cmd = Num()
    new_cmd.radius = radius
    new_cmd.velocity = velocity
    new_cmd.direction = direction

def main():
    # 퍼블리시 노드 초기화
    rospy.init_node('turtle_test', anonymous=False)
    
    # 퍼블리셔 변수
    pub = rospy.Publisher('new_command', Num, queue_size=10)
    
    # 1초마다 반복(변수=rate)
    rate = rospy.Rate(1) #1Hz

    msg = Num()	# 메시지 변수 선언
    count = 1

    # 중단되거나 사용자가 강제종료(ctrl+C) 전까지 계속 실행
    while not rospy.is_shutdown():
        # 메시지 내용 담기
        
        msg.radius = 1
        msg.velocity = 1
        msg.direction = 1

        # 터미널에 출력
        rospy.loginfo("you spin me right round baby right round")
                
        # 메시지를 퍼블리시
        pub.publish(msg)
        
        # 정해둔 주기(hz)만큼 일시중단
        rate.sleep()

        count += 1

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass