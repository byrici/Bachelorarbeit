#!/usr/bin/env python3
import rospy
from gazebo_msgs.msg import ModelStates

class ExtractPosition:
    def __init__(self):
        rospy.init_node("extract_position_node")
        
        self.target_name = "pxmark4"
        self.position = None

        rospy.Subscriber("/gazebo/model_states", ModelStates, self.callback)

        rospy.loginfo("Node gestartet. Warte 60 Sekunden...")

        # Timer ruft print_position nach 60s genau einmal auf
        rospy.Timer(rospy.Duration(60), self.print_position, oneshot=True)

        rospy.spin()  

    def callback(self, msg):
        if self.target_name in msg.name:
            index = msg.name.index(self.target_name)
            self.position = msg.pose[index].position

    def print_position(self, event):
        if self.position:
            rospy.loginfo(f"Position von {self.target_name} nach 60 Sekunden:")
            rospy.loginfo(f"x: {self.position.x:.3f}, y: {self.position.y:.3f}, z: {self.position.z:.3f}")
        else:
            rospy.logwarn(f"Keine Position für {self.target_name} erhalten!")

if __name__ == "__main__":
    try:
        ExtractPosition()
    except rospy.ROSInterruptException:
        pass