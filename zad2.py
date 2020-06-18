#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

global x
global y
global i
i = 0
global new_vel


def callback(pose):
    global new_vel
    global x
    global y
    global i
    if (i == 4):
        new_vel.linear.x = 0
        new_vel.angular.z = 0
    target_pose = Pose()
    target_pose.x = x[i]
    target_pose.y = y[i]
    curr_pose = pose
    curr_pose.x = round(pose.x, 4)
    curr_pose.y = round(pose.y, 4)

    if i != 4:
        new_vel.linear.x = get_lin_vel(curr_pose, target_pose)
        new_vel.angular.z = get_ang_vel(curr_pose, target_pose)
        print(str(curr_pose.x) + " " + str(curr_pose.y))
        print(str(target_pose.x) + " " + str(target_pose.y))

    rospy.loginfo("Pozycja x: %8.2f", pose.x)
    rospy.loginfo("Pozycja y: %8.2f", pose.y)
    rospy.loginfo("Pozycja theta: %8.2f", pose.theta)

    if get_distance(curr_pose, target_pose) < 0.1:
        new_vel.linear.x = 0
        new_vel.angular.z = 0
        if i <= 3:
            i = i + 1


# new_vel = Twist()

def get_distance(curr_pose, target_pose):
    return sqrt(pow((target_pose.x - curr_pose.x), 2) + pow((target_pose.y - curr_pose.y), 2))


def get_lin_vel(curr_pose, target_pose):
    return 1.1 * get_distance(curr_pose, target_pose)


def get_angle(curr_pose, target_pose):
    return atan2(target_pose.y - curr_pose.y, target_pose.x - curr_pose.x)


def get_ang_vel(curr_pose, target_pose):
    return 4 * (get_angle(curr_pose, target_pose) - curr_pose.theta)


if __name__ == "__main__":
    global x
    global y
    global i

    x = [1, 3, 7, 5, 9]
    y = [1, 7, 7, 5, 8]
    global new_vel
    new_vel = Twist()
    rospy.init_node('zad2', anonymous=True)
    print("ready")
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/pose', Pose, callback)

    rate = rospy.Rate(10)  # 10Hz
    while not rospy.is_shutdown():
        pub.publish(new_vel)  # wyslaniepredkoscizadanej
        rate.sleep()

    print("END")
