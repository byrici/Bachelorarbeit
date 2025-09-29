#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Bool

bridge = CvBridge()

STOP_DISTANCE = 0.5  # Distance in meters to stop before an obstacle

class ObstacleCheckNode:
    def __init__(self):
        rospy.init_node("obstacle_check_node")
        
        self.obstacle_detected = False

        self.pub = rospy.Publisher("/obstacles_detected", Bool, queue_size=10)

        rospy.Subscriber("/camera/depth/image_raw", Image, self.obstacle_check)

        rospy.loginfo("Obstacle Check Node started.")
        rospy.spin()
        

    def obstacle_check(self, msg):
        depth_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        valid_depth = np.where((depth_image > 0.0) & (depth_image < np.inf), depth_image, np.inf)
        #Interessanten Bereich des Bildes auswählen
        h, w = depth_image.shape
        # Hier wird der mittlere Bereich des Bildes ausgewählt
        roi = valid_depth[h//3:2*h//3, w//3:2*w//3]

        #Werte von Millimeter in Meter umrechnen
        roi_m = roi / 1000.0

        #Kleinsten gültigen Bereich finden
        min_distance = np.min(roi_m)

        #Abstand prüfen
        print(min_distance)
        if min_distance < STOP_DISTANCE:
            rospy.loginfo("Obstacle detected within stopping distance: {:.2f}m".format(min_distance))
            self.obstacle_detected = True
        else:
            rospy.loginfo("No obstacles detected within stopping distance.")
            self.obstacle_detected = False

        self.pub.publish(self.obstacle_detected)    

if __name__ == "__main__":
    try:
        ObstacleCheckNode()
    except rospy.ROSInterruptException:
        pass



    