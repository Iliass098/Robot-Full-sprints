from glob import glob
import os

from setuptools import find_packages, setup


package_name = 'eurobot_perception'


setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'templates'), glob('templates/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ilias',
    maintainer_email='iliasselkamilili@gmail.com',
    description='Perception nodes for the G06 Eurobot workspace.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'template_detector = eurobot_perception.template_detector:main',
            'aruco_table_detector = eurobot_perception.aruco_table_detector:main',
            'aruco_robot_detector = eurobot_perception.aruco_robot_detector:main',
        ],
    },
)
