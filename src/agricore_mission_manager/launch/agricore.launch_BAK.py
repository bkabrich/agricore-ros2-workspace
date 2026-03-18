from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='mavros',
            executable='mavros_node',
            #name='mavros_container',
            #name='mavros_node',
            #namespace='mavros',
            output='screen',
            arguments=[
                '--ros-args',
                '--log-level', 'info',
            ],
            parameters=[{
                'fcu_url': 'serial:///dev/ttyAMA0:115200',
                'gcs_url': '',
                'target_system_id': 1,
                'target_component_id': 1,
            }]
        ),
        Node(
            package='agricore_mission_manager',
            executable='mission_manager_node',
            name='agricore_mission_manager',
            output='screen'
        ),
        Node(
            package='agricore_vehicle_gateway',
            executable='agricore_vehicle_gateway_node',
            name='agricore_vehicle_gateway',
            output='screen'
        ),
        Node(
            package='agricore_watchdog',
            executable='agricore_watchdog_node',
            name='agricore_watchdog',
            output='screen'
        ),
        Node(
            package='agricore_telemetry',
            executable='agricore_telemetry_node',
            name='agricore_telemetry',
            output='screen'
        ),
    ])
