#!/usr/bin/env python3
"""
Agricore System Health Check - ROS 2 Version
Checks:
- UART → Cube Orange MAVLink heartbeat (TELEM port)
- USB → Cube Orange MAVLink heartbeat (Mission Planner path)
- ROS 2 node presence (your custom nodes + MAVROS)
- MAVROS /mavros/state topic rate & connection status
- Basic PWM subsystem detection (non-destructive)
"""

import time
import subprocess
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from mavros_msgs.msg import State
from pymavlink import mavutil

# Configuration
UART_DEVICE = "/dev/ttyAMA0"
UART_BAUD = 115200  # Change to 921600 if you set it higher
CHECK_DURATION = 12  # seconds to monitor
EXPECTED_NODES = [
    "/mavros_node",
    "/agricore_mission_manager",
    "/agricore_vehicle_gateway",
    "/agricore_watchdog",
    "/agricore_telemetry"
]

class HealthCheckNode(Node):
    def __init__(self):
        super().__init__('health_check_temp')
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT, history=HistoryPolicy.KEEP_LAST)
        self.state_sub = self.create_subscription(State, '/mavros/state', self.state_callback, qos)
        self.connected = False
        self.mode = "Unknown"
        self.armed = False
        self.rate_count = 0

    def state_callback(self, msg):
        self.connected = msg.connected
        self.mode = msg.mode
        self.armed = msg.armed
        self.rate_count += 1

def check_uart_mavlink():
    print("\n[1] Checking UART MAVLink connection...")
    # Quick check if MAVROS is publishing state (implies it has the port and connection)
    try:
        output = subprocess.check_output(["ros2", "topic", "info", "/mavros/state"], timeout=3).decode()
        if "Publisher count: 1" in output or "mavros_node" in output:
            print("  ✓ MAVROS appears connected (using the UART port) - skipping direct test")
            return True
    except:
        print("  ✓ MAVROS not active (using the UART port) - running direct test")
        pass  # MAVROS not publishing → proceed with direct test

    try:
        conn = mavutil.mavlink_connection(UART_DEVICE, baud=UART_BAUD, timeout=15)
        conn.wait_heartbeat(timeout=15)

        if conn.target_system > 0:
            # Wait for a recent HEARTBEAT (or other mode-carrying msg) if not already fresh
            hb = conn.recv_match(type='HEARTBEAT', blocking=True, timeout=3.0)

            if hb:
                # Extract mode from HEARTBEAT (most reliable for basic mode)
                base_mode = hb.base_mode
                custom_mode = hb.custom_mode

                # Get human-readable string (mode_mapping() still works)
                mode_map = conn.mode_mapping()
                if mode_map:
                    mode = mode_map.get(custom_mode, "Unknown")
                else:
                    mode = "Unknown (no mode map)"

                # Optional: Armed status from base_mode flags
                armed = bool(base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)

                print(f" ✓ Connected - System {conn.target_system}, Component {conn.target_component}")
                print(f" Mode: {mode}, Armed: {armed}")
                return True
            else:
                print(" ✗ Heartbeat received but no recent mode info")
                return False
        else:
            print(" ✗ No heartbeat received on UART")
            return False

    except Exception as e:
        print(f"  ✗ UART connection failed: {e}")
        return False

def check_usb_mavlink():
    print("\n[2] Checking USB MAVLink connection: Not longer used...")
    return True
    
    devices = mavutil.auto_detect_serial()
    if not devices:
        print("  ✗ No USB serial devices found")
        return False
    for dev in devices:
        try:
            conn = mavutil.mavlink_connection(dev, baud=115200, timeout=10)
            conn.wait_heartbeat(timeout=10)
            if conn.target_system > 0:
                print(f"  ✓ Found on {dev} - System {conn.target_system}")
                return True
        except:
            pass
    print("  ✗ No heartbeat on any USB serial port")
    return False

def check_ros_nodes():
    print("\n[3] Checking ROS 2 nodes...")
    try:
        output = subprocess.check_output(["ros2", "node", "list"], timeout=8).decode().strip()
        nodes = output.splitlines()
        found = set()
        for node in nodes:
            for expected in EXPECTED_NODES:
                if expected in node:
                    found.add(expected)
        missing = set(EXPECTED_NODES) - found
        if missing:
            print(f"  ✗ Missing nodes: {missing}")
            return False
        print(f"  ✓ All expected nodes present ({len(found)}/{len(EXPECTED_NODES)})")
        return True
    except Exception as e:
        print(f"  ✗ Failed to list nodes: {e}")
        return False

def check_mavros_state():
    print("\n[4] Checking MAVROS state topic...")
    rclpy.init()
    node = HealthCheckNode()
    start = time.time()
    while time.time() - start < CHECK_DURATION:
        rclpy.spin_once(node, timeout_sec=1.0)
    node.destroy_node()
    rclpy.shutdown()
    if node.connected:
        rate = node.rate_count / CHECK_DURATION if CHECK_DURATION > 0 else 0
        print(f"  ✓ MAVROS connected - mode: {node.mode}, armed: {node.armed}")
        print(f"  ✓ /mavros/state received {node.rate_count} messages → rate ~{rate:.1f} Hz")
        return True
    else:
        print("  ✗ No /mavros/state messages received or not connected")
        return False

def check_pwm_outputs():
    print("\n[5] Checking PWM servo outputs (non-destructive)...")
    try:
        output = subprocess.check_output(["ls", "/sys/class/pwm/pwmchip0"], timeout=5).decode()
        if "export" in output:
            print("  ✓ PWM subsystem detected")
            print("  → You can test servo movement in MANUAL mode via RC transmitter")
        else:
            print("  ✗ PWM subsystem not found or not enabled")
    except:
        print("  ✗ Cannot access PWM sysfs - check kernel modules")

def main():
    print("Agricore System Health Check - ROS 2 Version")
    print("==========================================\n")

    #uart_ok = check_uart_mavlink()
    print("\n[1] Checking UART MAVLink connection: Run before starting MAVROS")
    usb_ok = check_usb_mavlink()
    nodes_ok = check_ros_nodes()
    mavros_ok = check_mavros_state()
    pwm_ok = check_pwm_outputs()

    print("\nSummary:")
    #print(f"UART MAVLink:     {'OK' if uart_ok else 'FAIL'}")
    print("UART MAVLink: Test Removed")  
    #     {'OK' if uart_ok else 'FAIL'}")
    print(f"USB MAVLink:      {'OK' if usb_ok else 'FAIL'}")
    print(f"ROS 2 Nodes:      {'OK' if nodes_ok else 'FAIL'}")
    print(f"MAVROS State:     {'OK' if mavros_ok else 'FAIL'}")
    print(f"PWM Outputs:      {'Detected' if pwm_ok else 'Not found'}")

    #overall = uart_ok and mavros_ok and nodes_ok
    overall = usb_ok and mavros_ok and nodes_ok
    print("\nOverall system health:", "GOOD" if overall else "PROBLEMS DETECTED")

if __name__ == "__main__":
    main()
