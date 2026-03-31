from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='eurobot_perception',
            executable='template_detector',
            name='template_detector',
            output='screen',
        ),
        Node(
            package='eurobot_perception',
            executable='aruco_table_detector',
            name='aruco_table_detector',
            output='screen',
        ),
    ])
