import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    turtlebot_model = os.environ.get('TURTLEBOT3_MODEL', 'burger')

    world = os.path.join(
        get_package_share_directory('eurobot_bringup'),
        'world',
        'Tablero2.world',
    )
    gazebo_launch_dir = os.path.join(
        get_package_share_directory('gazebo_ros'),
        'launch',
    )
    turtlebot_launch_dir = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'launch',
    )

    return LaunchDescription([
        SetEnvironmentVariable('TURTLEBOT3_MODEL', turtlebot_model),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gazebo_launch_dir, 'gzserver.launch.py')
            ),
            launch_arguments={'world': world}.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gazebo_launch_dir, 'gzclient.launch.py')
            ),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(turtlebot_launch_dir, 'robot_state_publisher.launch.py')
            ),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('eurobot_bringup'),
                    'launch',
                    'static_overhead_camera.launch.py',
                )
            ),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('eurobot_bringup'),
                    'launch',
                    'perception.launch.py',
                )
            ),
        ),
    ])
