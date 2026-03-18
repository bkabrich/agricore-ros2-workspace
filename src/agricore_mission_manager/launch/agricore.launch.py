# ~/agricore/ros_ws/src/agricore_mission_manager/launch/agricore.launch.py

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # ────────────────────────────────────────────────
        # MAVROS node - minimal / standard configuration
        # No namespace, no custom name → uses default internal naming
        # ────────────────────────────────────────────────
        Node(
            package='mavros',
            executable='mavros_node',
            # name='mavros_container',          # ← REMOVED (this was causing issues)
            # namespace='mavros',               # ← REMOVED
            output='screen',
            parameters=[{
                'fcu_url': 'serial:///dev/ttyAMA0:115200',
                'gcs_url': '',                    # empty = no GCS forwarding
                'target_system_id': 1,
                'target_component_id': 1,
                'conn_timeout': 30.0,             # give more time for initial connection
                'heartbeat_rate': 1.0,
            }]
        ),

        # ────────────────────────────────────────────────
        # Your custom nodes (unchanged)
        # ────────────────────────────────────────────────
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
