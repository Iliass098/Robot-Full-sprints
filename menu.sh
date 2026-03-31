#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -n "${ROS_DISTRO:-}" ] && [ -f "/opt/ros/${ROS_DISTRO}/setup.bash" ]; then
    # Load ROS first when the shell is not already sourced.
    source "/opt/ros/${ROS_DISTRO}/setup.bash"
fi

if [ -f "${SCRIPT_DIR}/install/setup.bash" ]; then
    source "${SCRIPT_DIR}/install/setup.bash"
else
    echo "Workspace is not built yet. Run 'colcon build' first."
    exit 1
fi

exec ros2 run eurobot_bringup workspace_menu
