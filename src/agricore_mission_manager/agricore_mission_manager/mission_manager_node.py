import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String as StringMsg


class AgriCoreMissionManager(Node):
    def __init__(self):
        super().__init__("agricore_mission_manager")

        self.sub_cmd = self.create_subscription(
            StringMsg, "/agricore/mission_cmd", self._on_cmd, 10
        )
        self.pub_status = self.create_publisher(StringMsg, "/agricore/mission/status", 10)

        self._state = "idle"
        self._active_mission_id = None

        self.get_logger().info("Mission Manager ready. Listening on /agricore/mission_cmd")

    def _publish_status(self, state: str, mission_id=None, note: str = ""):
        msg = {
            "state": state,
            "mission_id": mission_id,
            "note": note,
        }
        out = StringMsg()
        out.data = json.dumps(msg)
        self.pub_status.publish(out)

    def _on_cmd(self, msg: StringMsg):
        try:
            cmd = json.loads(msg.data)
        except Exception as e:
            self.get_logger().warn(f"Bad cmd JSON: {e} | raw={msg.data!r}")
            return

        action = cmd.get("cmd")
        mission_id = cmd.get("mission_id")

        if action == "start":
            self._state = "running"
            self._active_mission_id = mission_id
            self.get_logger().info(f"START requested: mission_id={mission_id}")
            # Phase 2: dry-run only (no vehicle movement yet)
            self._publish_status(self._state, mission_id, note="Phase2 dry-run: start received")

        elif action == "stop":
            self.get_logger().info("STOP requested")
            self._state = "idle"
            self._active_mission_id = None
            self._publish_status(self._state, None, note="Phase2 dry-run: stop received")

        else:
            self.get_logger().warn(f"Unknown cmd: {action} | full={cmd}")


def main(args=None):
    rclpy.init(args=args)
    node = AgriCoreMissionManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

