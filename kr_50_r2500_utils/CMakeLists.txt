cmake_minimum_required(VERSION 3.0.2)
project(kr_50_r2500_utils)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  rospy
  std_msgs
)

## Generate services in the 'srv' folder
add_service_files(
  FILES
  SetMongoByParam.srv
  SetParamByMongo.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES kr_50_r2500_utils
#  CATKIN_DEPENDS eigen_conversions geometry_msgs moveit_core moveit_msgs moveit_ros_planning moveit_ros_planning_interface object_loader_msgs roscpp rosparam_utilities std_msgs std_srvs tf_conversions
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
