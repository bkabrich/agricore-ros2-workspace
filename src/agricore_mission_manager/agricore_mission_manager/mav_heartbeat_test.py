from pymavlink import mavutil
import time

# Use the working baud and device (change if needed)
connection = mavutil.mavlink_connection('/dev/ttyAMA0', baud=115200)  # or '/dev/ttyAMA0'

print("Waiting for heartbeat...")
heartbeat = connection.wait_heartbeat(timeout=10)

if heartbeat:
    print("Heartbeat received!")
    print(f"  System ID: {connection.target_system}")
    print(f"  Component ID: {connection.target_component}")
    
    # MAVLink version is usually in the HEARTBEAT payload itself
    # (field 'mavlink_version' in the msg)
    print(f"  MAVLink version from HEARTBEAT: {heartbeat.mavlink_version}")
    
    # Or access other fields from the parsed heartbeat msg
    print(f"  Vehicle type: {heartbeat.type} ({mavutil.mavlink.enums['MAV_TYPE'].get(heartbeat.type, 'Unknown')})")
    print(f"  Autopilot: {heartbeat.autopilot} ({mavutil.mavlink.enums['MAV_AUTOPILOT'].get(heartbeat.autopilot, 'Unknown')})")
else:
    print("No heartbeat received within timeout.")
