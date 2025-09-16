#!/usr/bin/env python3
import rospy
from gazebo_msgs.srv import SpawnModel
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Pose
import random

class SpwanObstacle:
    def __init__(self):
        rospy.init_node("spawn_obstacle_node")
        
        self.target_name = "pxmark4"
        self.position = None

        self.initial_pose = Pose()
        

        file = open('/my_project/src/interbotix_ros_crawlers/interbotix_ros_xshexapods/interbotix_xshexapod_gazebo/models/big_box/model.sdf')
        self.sdff = file.read()

        # akutelle Positon speichern
        rospy.Subscriber("/gazebo/model_states", ModelStates, self.callback)
        
        self.timing = random.randint(8, 15)
        # Timer ruft spawn_box nach 10s genau einmal auf
        rospy.Timer(rospy.Duration(self.timing), self.spawn_box, oneshot=True)

        rospy.spin()  

    def callback(self, msg):
        if self.target_name in msg.name:
            index = msg.name.index(self.target_name)
            self.position = msg.pose[index].position

    def spawn_box(self, event):
        self.initial_pose.position.x = self.position.x + 1.6 if self.position else 3
        self.initial_pose.position.y = 0
        self.initial_pose.position.z = 0.5
        print(self.initial_pose.position.x)

        rospy.loginfo("Spawning box in Gazebo...")
        rospy.wait_for_service('gazebo/spawn_sdf_model')
        spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
        spawn_model_prox("Box", self.sdff, "", self.initial_pose, "world")

if __name__ == "__main__":
    try:
        SpwanObstacle()
    except rospy.ROSInterruptException:
        pass
        
    