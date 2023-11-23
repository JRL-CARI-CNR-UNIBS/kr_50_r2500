# Copyright 2023 Áron Svastits
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.substitutions import Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.conditions import IfCondition
from moveit_configs_utils import MoveItConfigsBuilder
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def launch_setup(context, *args, **kwargs):

    # args that can be set from the command line or a default will be used
    prefix = LaunchConfiguration("prefix")
    robot_name = LaunchConfiguration("robot_name")
    fake = LaunchConfiguration('fake')
    rviz_gui = LaunchConfiguration('rviz_gui')

    robot_description = {
        'robot_description':
        ParameterValue(
           Command(
               [PathJoinSubstitution([FindExecutable(name='xacro')]),
                " ",
                PathJoinSubstitution(
                    [FindPackageShare('kr_50_r2500_description'),
                     "urdf",
                     "kr_50_r2500_rviz.xacro"]
                ),
                " ",
                "robot_name:=",
                robot_name.perform(context),
                " ",
                "prefix:=",
                prefix.perform(context),
                " ",
                "use_fake_hardware:=",
                fake.perform(context),]
           ),
           value_type=str
        )
    }

    controller_config = PathJoinSubstitution(
        [FindPackageShare("kr_50_r2500_description"),
         "config",
         "ros2_controller_config.yaml"]
    )
    moveit_config = (
        MoveItConfigsBuilder("kr_50_r2500")
        .robot_description(file_path="config/kr_50_r2500.urdf.xacro")
        .planning_scene_monitor(
            publish_robot_description=True, publish_robot_description_semantic=True
        )
        .robot_description_semantic(file_path="config/kr_50_r2500.srdf")
        .planning_pipelines("ompl", pipelines=["ompl", "pilz_industrial_motion_planner"])
        .to_moveit_configs()
    )

    joint_traj_controller_config = PathJoinSubstitution(
        [FindPackageShare("kr_50_r2500_description"),
         "config",
         "joint_trajectory_controller_config.yaml"]
    )
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("kr_50_r2500_description"),
         "config",
         "view_cell.rviz"]
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, controller_config],
        output="both",
    )

    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics
        ],
        condition=IfCondition(rviz_gui),
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster",
                   "--controller-manager",
                   "/controller_manager"],
    )
    current_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["current_broadcaster",
                   "--controller-manager",
                   "/controller_manager"],
    )

    joint_trajectory_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller",
                   "-c",
                   "/controller_manager",
                   "-p",
                   joint_traj_controller_config],
    )

    move_group_node = Node(
           package="moveit_ros_move_group",
           executable="move_group",
           output="screen",
           parameters=[moveit_config.to_dict()],
           arguments=["--ros-args", "--log-level", "info"],
    )

    nodes_to_start = [
        control_node,
        robot_state_pub_node,
        rviz_node,
        joint_state_broadcaster_spawner,
        current_broadcaster_spawner,
        joint_trajectory_controller_spawner,
        move_group_node
        ]

    return nodes_to_start


def generate_launch_description():
    launch_arguments = []
    launch_arguments.append(DeclareLaunchArgument(
        'prefix',
        default_value=''
    ))
    launch_arguments.append(DeclareLaunchArgument(
        'robot_name',
        default_value="kr_50_r2500"
    ))
    launch_arguments.append(DeclareLaunchArgument(
        'fake',
        default_value="false"
    ))
    launch_arguments.append(DeclareLaunchArgument(
        'rviz_gui',
        default_value="true"
    ))
    ld = LaunchDescription(launch_arguments +
                           [OpaqueFunction(function=launch_setup)])

    return ld
