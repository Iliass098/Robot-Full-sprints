from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='eurobot_navigation',
            executable='topic_monitor',
            name='topic_monitor',
            output='screen',
        ),
    ])
