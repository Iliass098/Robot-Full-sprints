from setuptools import find_packages, setup


package_name = 'eurobot_navigation'


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
    description='Navigation and monitoring nodes for the G06 Eurobot workspace.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'route_navigation = eurobot_navigation.route_navigation:main',
            'topic_monitor = eurobot_navigation.topic_monitor:main',
        ],
    },
)
