# Install script for directory: /home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/uavteam6/catkin_ws_G6/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
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

# Set path to fallback-tool for dependency-resolution.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/depthai_ros_msgs/msg" TYPE FILE FILES
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/msg/AutoFocusCtrl.msg"
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/msg/FFMPEGPacket.msg"
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/msg/HandLandmark.msg"
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/msg/HandLandmarkArray.msg"
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/msg/SpatialDetection.msg"
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/msg/SpatialDetectionArray.msg"
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/msg/ImuWithMagneticField.msg"
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/msg/TrackDetection2D.msg"
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/msg/TrackDetection2DArray.msg"
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/msg/TrackedFeature.msg"
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/msg/TrackedFeatures.msg"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/depthai_ros_msgs/srv" TYPE FILE FILES
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/srv/TriggerNamed.srv"
    "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/srv/NormalizedImageCrop.srv"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/depthai_ros_msgs/cmake" TYPE FILE FILES "/home/uavteam6/catkin_ws_G6/build/depthai-ros/depthai_ros_msgs/catkin_generated/installspace/depthai_ros_msgs-msg-paths.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/uavteam6/catkin_ws_G6/devel/include/depthai_ros_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/uavteam6/catkin_ws_G6/devel/share/roseus/ros/depthai_ros_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/uavteam6/catkin_ws_G6/devel/share/common-lisp/ros/depthai_ros_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/uavteam6/catkin_ws_G6/devel/share/gennodejs/ros/depthai_ros_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/uavteam6/catkin_ws_G6/devel/lib/python3/dist-packages/depthai_ros_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/uavteam6/catkin_ws_G6/devel/lib/python3/dist-packages/depthai_ros_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/uavteam6/catkin_ws_G6/build/depthai-ros/depthai_ros_msgs/catkin_generated/installspace/depthai_ros_msgs.pc")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/depthai_ros_msgs/cmake" TYPE FILE FILES "/home/uavteam6/catkin_ws_G6/build/depthai-ros/depthai_ros_msgs/catkin_generated/installspace/depthai_ros_msgs-msg-extras.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/depthai_ros_msgs/cmake" TYPE FILE FILES
    "/home/uavteam6/catkin_ws_G6/build/depthai-ros/depthai_ros_msgs/catkin_generated/installspace/depthai_ros_msgsConfig.cmake"
    "/home/uavteam6/catkin_ws_G6/build/depthai-ros/depthai_ros_msgs/catkin_generated/installspace/depthai_ros_msgsConfig-version.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/depthai_ros_msgs" TYPE FILE FILES "/home/uavteam6/catkin_ws_G6/src/depthai-ros/depthai_ros_msgs/package.xml")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/home/uavteam6/catkin_ws_G6/build/depthai-ros/depthai_ros_msgs/install_local_manifest.txt"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
