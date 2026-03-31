from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='eurobot_navigation',
            executable='route_navigation',
            name='route_navigation',
            output='screen',
            parameters=[{'use_sim_time': False}],
        ),
    ])
