from setuptools import find_packages, setup


package_name = 'eurobot_control'


setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ilias',
    maintainer_email='iliasselkamilili@gmail.com',
    description='Robot control nodes for the G06 Eurobot workspace.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'line_follower = eurobot_control.line_follower:main',
            'star_fsm = eurobot_control.star_fsm:main',
        ],
    },
)
