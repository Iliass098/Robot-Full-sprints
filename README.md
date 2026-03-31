# G06 Eurobot Workspace

Clean ROS 2 workspace for the G06 project. The source tree is split by domain so each package has a clear responsibility.

## Packages

- `src/eurobot_perception`: ArUco and template-based vision nodes.
- `src/eurobot_control`: line following and scripted FSM control.
- `src/eurobot_navigation`: route navigation and runtime topic monitoring.
- `src/eurobot_bringup`: launch files, simulation assets, configs, and the interactive menu.

## Quick Start

```bash
colcon build
source install/setup.bash
ros2 run eurobot_bringup workspace_menu
```

Or use the repo shortcut:

```bash
./menu.sh
```

## Direct Launch Commands

```bash
ros2 launch eurobot_bringup simulation.launch.py
ros2 launch eurobot_bringup perception.launch.py
ros2 launch eurobot_bringup line_follower.launch.py
ros2 run eurobot_control camera_debug_viewer
ros2 launch eurobot_bringup line_follower_with_viewer.launch.py
ros2 launch eurobot_bringup star_fsm.launch.py
ros2 launch eurobot_bringup navigation.launch.py
ros2 launch eurobot_bringup monitor.launch.py
ros2 launch eurobot_bringup full_demo.launch.py
```

## Structure

- `src/`: ROS 2 packages only.
- `assets/`: rosbag and non-package project assets.
- `world/`: shared Gazebo models.
- `frames.pdf`: reference document.
