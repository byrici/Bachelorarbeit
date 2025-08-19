# Install script for directory: /my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/my_project/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/interbotix_xs_msgs/msg" TYPE FILE FILES
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/msg/JointGroupCommand.msg"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/msg/JointSingleCommand.msg"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/msg/JointTrajectoryCommand.msg"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/msg/JointTemps.msg"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/msg/ArmJoy.msg"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/msg/HexJoy.msg"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/msg/LocobotJoy.msg"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/msg/TurretJoy.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/interbotix_xs_msgs/srv" TYPE FILE FILES
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/srv/Reboot.srv"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/srv/RobotInfo.srv"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/srv/MotorGains.srv"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/srv/TorqueEnable.srv"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/srv/OperatingModes.srv"
    "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/srv/RegisterValues.srv"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/interbotix_xs_msgs/cmake" TYPE FILE FILES "/my_project/build/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/catkin_generated/installspace/interbotix_xs_msgs-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/my_project/devel/include/interbotix_xs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/my_project/devel/share/roseus/ros/interbotix_xs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/my_project/devel/share/common-lisp/ros/interbotix_xs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/my_project/devel/share/gennodejs/ros/interbotix_xs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/my_project/devel/lib/python3/dist-packages/interbotix_xs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/my_project/devel/lib/python3/dist-packages/interbotix_xs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/my_project/build/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/catkin_generated/installspace/interbotix_xs_msgs.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/interbotix_xs_msgs/cmake" TYPE FILE FILES "/my_project/build/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/catkin_generated/installspace/interbotix_xs_msgs-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/interbotix_xs_msgs/cmake" TYPE FILE FILES
    "/my_project/build/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/catkin_generated/installspace/interbotix_xs_msgsConfig.cmake"
    "/my_project/build/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/catkin_generated/installspace/interbotix_xs_msgsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/interbotix_xs_msgs" TYPE FILE FILES "/my_project/src/interbotix_ros_core/interbotix_ros_xseries/interbotix_xs_msgs/package.xml")
endif()

