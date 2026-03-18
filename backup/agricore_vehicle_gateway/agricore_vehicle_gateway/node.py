#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
class VehicleGatewayNode(Node):
    """
    Phase 1 stub:
    - publishes a heartbeat
    - logs startup and shutdown
    - no motion authority yet
    """
    def __init__(self):
        super().__init__('agricore_vehicle_gateway')
        self.pub = self.create_publisher(String, 'agricore/heartbeat', 10)
        self.timer = self.create_timer(1.0, self._tick)
        self.get_logger().info('VehicleGatewayNode started (Phase 1 stub).')

    def _tick(self):
        msg = String()
        msg.data = 'vehicle_gateway:alive'
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = VehicleGatewayNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info('VehicleGatewayNode shutting down.')
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
