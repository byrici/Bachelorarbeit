#!/usr/bin/env python3

import rospy
import numpy as np
import py_trees
import py_trees.blackboard
import sys
import os
import cv2
import math
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import Imu
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

# nodes zum Python-Importpfad hinzufügen
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'nodes'))

import walk_forward  # importiere die Funktion aus walk_forward.py
import switch_gait 
from walk_forward import HexapodWrapper # importiere die Funktion aus switch_gait.py
from obstacle_check import obstacle_check


class WalkForwardTripodBehavior(py_trees.behaviour.Behaviour):
    def __init__(self, hexapod, name="WalkForwardTripod"):
        super(WalkForwardTripodBehavior, self).__init__(name)
        self.hexapod = hexapod
        self.done = False

    def setup(self, **kwargs):
        rospy.loginfo(f"Setup {self.name}")
        return True

    def initialise(self):
        rospy.loginfo(f"Initialising {self.name}")
        self.done = False

    def update(self):
        if not self.done:
            rospy.loginfo(f"Calling move_forward() in {self.name}")
            self.hexapod.move_forward()
            self.done = True
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.SUCCESS

    def terminate(self, new_status):
        rospy.loginfo(f"Terminating {self.name}")

class WalkForwardWaveBehavior(py_trees.behaviour.Behaviour):
    def __init__(self, hexapod, name="WalkForwardWave"):
        super(WalkForwardWaveBehavior, self).__init__(name)
        self.hexapod = hexapod
        self.done = False

    def setup(self, **kwargs):
        rospy.loginfo(f"Setup {self.name}")
        return True

    def initialise(self):
        rospy.loginfo(f"Initialising {self.name}")
        self.done = False

    def update(self):
        if not self.done:
            rospy.loginfo(f"Calling move_forward() in {self.name}")
            self.hexapod.move_forward(gait_type='wave')
            self.done = True
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.SUCCESS

    def terminate(self, new_status):
        rospy.loginfo(f"Terminating {self.name}")


class WalkBackwardsTripodBehavior(py_trees.behaviour.Behaviour):
    def __init__(self, hexapod, name="WalkBackwardsTripod"):
        super(WalkBackwardsTripodBehavior, self).__init__(name)
        self.hexapod = hexapod
        self.done = False

    def setup(self, **kwargs):
        rospy.loginfo(f"Setup {self.name}")
        return True

    def initialise(self):
        rospy.loginfo(f"Initialising {self.name}")
        self.done = False

    def update(self):
        if not self.done:
            rospy.loginfo(f"Calling move_forward() in {self.name} with negative x stride")
            self.hexapod.move_forward(gait_type='Tripod', x_stride=-0.06)
            self.done = True
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.SUCCESS

    def terminate(self, new_status):
        rospy.loginfo(f"Terminating {self.name}")

class RotateBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, hexapod, name="Rotate"):
        super(RotateBehaviour, self).__init__(name)
        self.hexapod = hexapod
        self.done = False

    def setup(self, **kwargs):
        rospy.loginfo(f"Setup {self.name}")
        return True

    def initialise(self):
        rospy.loginfo(f"Initialising {self.name}")
        self.done = False

    def update(self):
        if not self.done:
            rospy.loginfo(f"Calling move_in_place() in {self.name}")
            self.hexapod.rotate(yaw_stride = 0.1)
            self.done = True
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.SUCCESS

    def terminate(self, new_status):
        rospy.loginfo(f"Terminating {self.name}")

class CheckForObstacleBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="CheckForObstacle"):
        super(CheckForObstacleBehaviour, self).__init__(name)
        self.obstacle_detected = False
        self.bridge = CvBridge()
        self.stop_distance = 0.5  # Distance in meters to stop before an obstacle
        self.msg_received = False

    def setup(self, **kwargs):
        rospy.loginfo(f"Setup {self.name}")
        return True

    def initialise(self):
        rospy.loginfo(f"Initialising {self.name}")
        self.msg_received = False
        rospy.Subscriber("/camera/depth/image_raw", Image, self.check_obstacle)
        
    
    def check_obstacle(self, msg):
        depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        valid_depth = np.where((depth_image > 0.0) & (depth_image < np.inf), depth_image, np.inf)
        #Interessanten Bereich des Bildes auswählen
        h, w = depth_image.shape
        #Hier wird der mittlere Bereich des Bildes ausgewählt
        roi = valid_depth[h//3:2*h//3, :]

        #Werte von Millimeter in Meter umrechnen
        roi_m = roi / 1000.0

        #Kleinsten gültigen Bereich finden
        min_distance = np.min(roi_m)

        #Abstand prüfen
        self.obstacle_detected = min_distance < self.stop_distance
        self.msg_received = True

    def update(self):
        if not self.msg_received:
            print("Waiting for depth image message...")
            return py_trees.common.Status.RUNNING
        print("message received, checking obstacle status...")
        return py_trees.common.Status.FAILURE if self.obstacle_detected else py_trees.common.Status.SUCCESS
            

    def terminate(self, new_status):
        rospy.loginfo(f"Terminating {self.name}")

class AdaptiveGaitSwitcher(py_trees.behaviour.Behaviour):
    def __init__(self, hexapod, name="AdaptiveGaitSwitcher"):
        super(AdaptiveGaitSwitcher, self).__init__(name)
        self.hexapod = hexapod
        self.done = False
        self.pich_threshold = 12.0
        self.roll_threshold = 10.0
        self.uneven = False 
        self.msg_received = False

    def setup(self, **kwargs):
        rospy.loginfo(f"Setup {self.name}")
        return True

    def initialise(self):
        rospy.loginfo(f"Initialising {self.name}")
        self.done = False
        rospy.Subscriber("/pxmark4/camera_imu", Imu, self.imu_callback)

    def imu_callback(self, msg):
        roll, pitch, yaw = self.get_rpy(msg)
        rospy.loginfo(f"IMU Roll: {roll}, Pitch: {pitch}, Yaw: {yaw}")

        if abs(pitch) > self.pich_threshold or abs(roll) > self.roll_threshold:
            self.uneven = True
            rospy.loginfo("Uneven terrain detected, switching to wave gait.")
        else:
            if self.uneven:
                rospy.loginfo("Terrain is even again, switching back to tripod gait.")    
            self.uneven = False

        self.msg_received = True

    def update(self):
        if not self.msg_received:
            rospy.loginfo("Waiting for IMU message...")
            return py_trees.common.Status.RUNNING

        return py_trees.common.Status.FAILURE if self.uneven else py_trees.common.Status.SUCCESS

    def get_rpy(self, msg):
        orientation = msg.orientation
        roll, pitch, yaw = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)
    
    def terminate(self, new_status):
        rospy.loginfo(f"Terminating {self.name}")

            
def create_tree_obstacle_avoidance():

    hexapod = HexapodWrapper(robot_name='pxmark4', init_node=False)
    
    check_obstacle = CheckForObstacleBehaviour()
    
    # Output muss invertiert werden, damit die Rotation ausgeführt wird, bis kein Hindernis erkannt wird
    rotate_behaviour = py_trees.decorators.Inverter(
        child=RotateBehaviour(hexapod=hexapod),
        name="RotateInverter"
    )
    

    # Erstelle Walk-Actions
    repeat_walk_tripod = WalkForwardTripodBehavior(hexapod=hexapod)
    repeat_walk_wave = WalkForwardWaveBehavior(hexapod=hexapod)

    # Laufsequenz erstellen
    walk_sequence = py_trees.composites.Sequence("WalkSequence", memory=False)
    walk_sequence.add_child(repeat_walk_tripod)
    walk_sequence.add_child(repeat_walk_wave)

    # Fallback-Sequenz für Hindernisvermeidung
    obstacle_fallback = py_trees.composites.Selector("ObstacleSequence", memory=False)
    obstacle_fallback.add_child(check_obstacle)
    obstacle_fallback.add_child(rotate_behaviour)
    
    # Erstelle die Wurzel des Baums
    root = py_trees.composites.Sequence("MainSequence", memory=False)
    root.add_child(obstacle_fallback)
    root.add_child(walk_sequence)
    
    
    return root

def create_tree_adaptive_gait_switch():
    hexapod = HexapodWrapper(robot_name='pxmark4', init_node=False)

    check_stability = AdaptiveGaitSwitcher(hexapod=hexapod)

    # Erstelle Walk-Actions
    repeat_walk_tripod = WalkForwardTripodBehavior(hexapod=hexapod)
    repeat_walk_wave = WalkForwardWaveBehavior(hexapod=hexapod)

    # Fallback-Sequenz für den Unebenheitscheck
    stablility_fallback = py_trees.composites.Selector("StabilitySequence", memory=False)
    stablility_fallback.add_child(check_stability)
    stablility_fallback.add_child(repeat_walk_wave)

    # Erstelle die Wurzel des Baums
    root = py_trees.composites.Sequence("MainSequence", memory=False)
    root.add_child(stablility_fallback)
    root.add_child(repeat_walk_tripod)

    return root
    

def main():
    rospy.init_node("bt_hexapod_controller")

    # BT erstellen
    tree = py_trees.trees.BehaviourTree(create_tree_adaptive_gait_switch())

    rospy.loginfo("Behavior Tree gestartet")

    rate = rospy.Rate(1.0)
    while not rospy.is_shutdown():
        tree.tick()
        rate.sleep()

if __name__ == '__main__':
    main()
