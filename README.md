# Bachelorarbeit

The work examines the possibility of dynamic and adaptive gait transitions through a behavior tree-based control architecture.


The repository contains the logic of the control architecture, as well as two scenarios that are intended to demonstrate the suitability of BTs as a control architecture.
The robot can react to suddenly appearing obstacles and can also better traverse uneven terrain through dynamic gait transitions.
For the tests, nodes were implemented that determine the position of the robot after 60 seconds and spawn an obstacle at any time and distance.

The robot model was adapted to match the real model. Additionally, a separate world was created to examine behavior in uneven terrain.

The system is based on ROS 1, which is why Ubuntu 20.04 is required. A Dockerfile is provided for this reason.

Two launch files are included:

- bot.launch starts the robot in the sim
- hexa.launch starts the real Hexapod


