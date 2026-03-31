from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='aruco_robot_to_base_tf',
            arguments=[
                '0', '0', '0',
                '0', '0', '0',
                'aruco_robot',
                'base_link',
            ],
            parameters=[{'use_sim_time': True}],
        ),
    ])
