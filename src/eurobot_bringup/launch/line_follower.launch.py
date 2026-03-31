import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_share = get_package_share_directory('eurobot_bringup')
    params_file = os.path.join(package_share, 'config', 'line_follower_params.yaml')

    return LaunchDescription([
        Node(
            package='eurobot_control',
            executable='line_follower',
            name='line_follower',
            output='screen',
            parameters=[params_file],
        ),
    ])
