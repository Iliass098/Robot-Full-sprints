from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='eurobot_cositas',
            executable='estados',
            name='star_robot_fsm',
            output='screen'
        )
    ])