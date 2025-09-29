#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64

class JointStateToGazeboBridge:
    def __init__(self):
        rospy.init_node("joint_state_to_gazebo_bridge")
        
        # Mapping joint name zu Gazebo command topic
        self.joint_to_topic = {
            "left_back_coxa":    "/pxmark4/left_back_coxa_controller/command",
            "left_back_femur":   "/pxmark4/left_back_femur_controller/command",
            "left_back_tibia":   "/pxmark4/left_back_tibia_controller/command",
            "left_middle_coxa":  "/pxmark4/left_middle_coxa_controller/command",
            "left_middle_femur": "/pxmark4/left_middle_femur_controller/command",
            "left_middle_tibia": "/pxmark4/left_middle_tibia_controller/command",
            "left_front_coxa":   "/pxmark4/left_front_coxa_controller/command",
            "left_front_femur":  "/pxmark4/left_front_femur_controller/command",
            "left_front_tibia":  "/pxmark4/left_front_tibia_controller/command",
            "right_front_coxa":  "/pxmark4/right_front_coxa_controller/command",
            "right_front_femur": "/pxmark4/right_front_femur_controller/command",
            "right_front_tibia": "/pxmark4/right_front_tibia_controller/command",
            "right_middle_coxa": "/pxmark4/right_middle_coxa_controller/command",
            "right_middle_femur":"/pxmark4/right_middle_femur_controller/command",
            "right_middle_tibia":"/pxmark4/right_middle_tibia_controller/command",
            "right_back_coxa":   "/pxmark4/right_back_coxa_controller/command",
            "right_back_femur":  "/pxmark4/right_back_femur_controller/command",
            "right_back_tibia":  "/pxmark4/right_back_tibia_controller/command",
        }

        # Erzeuge einen Publisher pro Joint
        self.publishers = {
            joint: rospy.Publisher(topic, Float64, queue_size=10)
            for joint, topic in self.joint_to_topic.items()
        }

        # Abonniere das JointState-Topic
        rospy.Subscriber("/pxmark4/joint_states", JointState, self.jointstate_callback)
        rospy.loginfo("JointState: Gazebo bridge started.")
        rospy.spin()

    def jointstate_callback(self, msg):
        joint_data = dict(zip(msg.name, msg.position))
        for joint_name, position in joint_data.items():
            if joint_name in self.publishers:
                self.publishers[joint_name].publish(Float64(position))


if __name__ == "__main__":
    try:
        JointStateToGazeboBridge()
    except rospy.ROSInterruptException:
        pass
