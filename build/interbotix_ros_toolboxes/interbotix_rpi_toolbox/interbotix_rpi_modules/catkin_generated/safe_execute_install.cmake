execute_process(COMMAND "/my_project/build/interbotix_ros_toolboxes/interbotix_rpi_toolbox/interbotix_rpi_modules/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/my_project/build/interbotix_ros_toolboxes/interbotix_rpi_toolbox/interbotix_rpi_modules/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
