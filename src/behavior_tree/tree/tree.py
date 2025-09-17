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
        rospy.loginfo(f"Calling move_forward() in {self.name}")
        self.hexapod.move_forward()
            
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
        rospy.loginfo(f"Calling move_forward() in {self.name}")
        self.hexapod.move_forward(gait_type='wave')
            
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
        rospy.loginfo(f"Calling move_forward() in {self.name} with negative x stride")
        self.hexapod.move_forward(gait_type='Tripod', x_stride=-0.06)
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
        rospy.loginfo(f"Calling move_in_place() in {self.name}")
        self.hexapod.rotate(yaw_stride = 0.1)
            
        return py_trees.common.Status.RUNNING

    def terminate(self, new_status):
        rospy.loginfo(f"Terminating {self.name}")

class CheckForObstacleBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="CheckForObstacle"):
        super(CheckForObstacleBehaviour, self).__init__(name)
        self.obstacle_detected = False
        self.msg_received = False

    def setup(self, **kwargs):
        rospy.loginfo(f"Setup {self.name}")
        rospy.Subscriber("/obstacles_detected", Bool, self.check_obstacle)
        return True

    def initialise(self):
        rospy.loginfo(f"Initialising {self.name}")
        self.msg_received = False

    def check_obstacle(self, msg: Bool):
        self.obstacle_detected = msg.data
        self.msg_received = True

    def update(self):
        if not self.msg_received:
            rospy.loginfo("Waiting for obstacle detection message...")
            return py_trees.common.Status.RUNNING

        rospy.loginfo(f"Obstacle detected: {self.obstacle_detected}")
        return (
            py_trees.common.Status.FAILURE
            if self.obstacle_detected
            else py_trees.common.Status.SUCCESS
        )


    def terminate(self, new_status):
        rospy.loginfo(f"Terminating {self.name}")

class AdaptiveGaitSwitcher(py_trees.behaviour.Behaviour):
    def __init__(self, hexapod, name="AdaptiveGaitSwitcher"):
        super(AdaptiveGaitSwitcher, self).__init__(name)
        self.hexapod = hexapod
        self.done = False
        self.pich_threshold = 1.5
        self.roll_threshold = 1.5
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
        """ rospy.loginfo(f"IMU Roll: {roll}, Pitch: {pitch}, Yaw: {yaw}") """

        if abs(pitch) > self.pich_threshold or abs(roll) > self.roll_threshold:
            self.uneven = True
            """ rospy.loginfo("Uneven terrain detected, switching to wave gait.") """
        else:
            if self.uneven:
                """ rospy.loginfo("Terrain is even again, switching back to tripod gait.")    """ 
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
    
    
    rotate_behaviour = RotateBehaviour(hexapod=hexapod)
   
    # Erstelle Walk-Action
    repeat_walk_tripod = WalkForwardTripodBehavior(hexapod=hexapod)
    

    # Fallback-Sequenz für Hindernisvermeidung
    obstacle_fallback = py_trees.composites.Selector("ObstacleSequence", memory=False)
    obstacle_fallback.add_child(check_obstacle)
    obstacle_fallback.add_child(rotate_behaviour)
    
    # Erstelle die Wurzel des Baums
    root = py_trees.composites.Sequence("MainSequence", memory=False)
    root.add_child(obstacle_fallback)
    root.add_child(repeat_walk_tripod)
    
    
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
    tree = py_trees.trees.BehaviourTree(create_tree_obstacle_avoidance())

    rospy.loginfo("Behavior Tree gestartet")

    while not rospy.is_shutdown():
        tree.tick_tock(

            period_ms=500,

            number_of_iterations=py_trees.trees.CONTINUOUS_TICK_TOCK,

            pre_tick_handler=None,

            post_tick_handler=None,

        )
        

if __name__ == '__main__':
    main()
