#!/usr/bin/env python3

import shutil
import subprocess
import sys


MENU_OPTIONS = [
    ('Simulation World', ['ros2', 'launch', 'eurobot_bringup', 'simulation.launch.py']),
    ('Perception Stack', ['ros2', 'launch', 'eurobot_bringup', 'perception.launch.py']),
    ('Line Follower', ['ros2', 'launch', 'eurobot_bringup', 'line_follower.launch.py']),
    ('Star FSM', ['ros2', 'launch', 'eurobot_bringup', 'star_fsm.launch.py']),
    ('Route Navigation', ['ros2', 'launch', 'eurobot_bringup', 'navigation.launch.py']),
    ('Topic Monitor', ['ros2', 'launch', 'eurobot_bringup', 'monitor.launch.py']),
    ('Full Demo Stack', ['ros2', 'launch', 'eurobot_bringup', 'full_demo.launch.py']),
]


def print_menu():
    print('\nG06 Workspace Menu')
    print('=' * 72)
    for index, (label, command) in enumerate(MENU_OPTIONS, start=1):
        print(f'{index}. {label:<18} {" ".join(command)}')
    print('0. Exit')
    print('=' * 72)


def main():
    if shutil.which('ros2') is None:
        print('`ros2` is not available in PATH. Source your workspace first.')
        return 1

    while True:
        print_menu()
        try:
            choice = input('Select an option: ').strip()
        except EOFError:
            print()
            return 0

        if choice == '0':
            return 0

        if not choice.isdigit():
            print('Invalid option. Enter a number from the menu.')
            continue

        index = int(choice) - 1
        if index < 0 or index >= len(MENU_OPTIONS):
            print('Invalid option. Enter a number from the menu.')
            continue

        label, command = MENU_OPTIONS[index]
        print(f'\nLaunching {label}...\n')
        try:
            subprocess.run(command, check=False)
        except KeyboardInterrupt:
            print('\nLaunch interrupted.\n')


if __name__ == '__main__':
    sys.exit(main())
