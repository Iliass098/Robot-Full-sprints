import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    bringup_launch_dir = os.path.join(
        get_package_share_directory('eurobot_bringup'),
        'launch',
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(bringup_launch_dir, 'simulation.launch.py')
            ),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(bringup_launch_dir, 'static_robot_aruco_tf.launch.py')
            ),
        ),
        Node(
            package='eurobot_navigation',
            executable='route_navigation',
            name='route_navigation',
            output='screen',
        ),
        Node(
            package='eurobot_navigation',
            executable='topic_monitor',
            name='topic_monitor',
            output='screen',
        ),
        Node(
            package='eurobot_control',
            executable='line_follower',
            name='line_follower',
            output='screen',
            parameters=[
                os.path.join(
                    get_package_share_directory('eurobot_bringup'),
                    'config',
                    'line_follower_params.yaml',
                )
            ],
        ),
    ])
