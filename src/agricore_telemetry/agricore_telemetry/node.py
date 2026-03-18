#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TelemetryAggregatorNode(Node):
    """
    Phase 1 stub:
    - subscribes to heartbeat
    - republishes a consolidated 'system telemetry' topic
    - later: publishes pose/speed/state for the web UI
    """
    def __init__(self):
        super().__init__('agricore_telemetry')
        self.pub = self.create_publisher(String, 'agricore/telemetry/system', 10)
        self.sub = self.create_subscription(String, 'agricore/heartbeat', self._on_hb, 10)
        self.get_logger().info('TelemetryAggregatorNode started (Phase 1 stub).')

    def _on_hb(self, msg: String):
        out = String()
        out.data = f'system_seen:{msg.data}'
        self.pub.publish(out)


def main():
    rclpy.init()
    node = TelemetryAggregatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info('TelemetryAggregatorNode shutting down.')
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
