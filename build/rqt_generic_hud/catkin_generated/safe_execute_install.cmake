execute_process(COMMAND "/home/uavteam6/catkin_ws_G6/build/rqt_generic_hud/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/uavteam6/catkin_ws_G6/build/rqt_generic_hud/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
