import os
from glob import glob
from setuptools import setup

package_name = 'agricore_mission_manager'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Bruce',
    maintainer_email='your.email@example.com',
    description='Mission manager for Agricore autonomous mower system',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mission_manager_node = agricore_mission_manager.mission_manager_node:main',
            'system_health_check = agricore_mission_manager.system_health_check:main',
        ],
    },
)
