#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class WatchdogNode(Node):
    """
    Phase 1 stub:
    - listens for heartbeats
    - reports last-seen timing
    - later: enforces HOLD/ESTOP on missing heartbeat
    """
    def __init__(self):
        super().__init__('agricore_watchdog')
        self.last_seen = {}
        self.sub = self.create_subscription(String, 'agricore/heartbeat', self._on_hb, 10)
        self.timer = self.create_timer(2.0, self._report)
        self.get_logger().info('WatchdogNode started (Phase 1 stub).')

    def _on_hb(self, msg: String):
        self.last_seen[msg.data] = time.time()

    def _report(self):
        now = time.time()
        if not self.last_seen:
            self.get_logger().warn('No heartbeats observed yet.')
            return
        # Print a compact summary
        parts = []
        for k, ts in sorted(self.last_seen.items()):
            age = now - ts
            parts.append(f'{k} age={age:.1f}s')
        self.get_logger().info(' | '.join(parts))


def main():
    rclpy.init()
    node = WatchdogNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info('WatchdogNode shutting down.')
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
