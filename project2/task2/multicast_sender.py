import socket
import struct
import json
import time
import sys
import os

MULTICAST_GROUP = "224.1.1.1"
PORT = 5007
TTL = 2

sensor_name = "temp"
if len(sys.argv) > 1:
    sensor_name = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack("b", TTL))

for i in range(5):
    json_message = {
        "sensor": sensor_name,
        "value": round(20 + i + (0.5 if sensor_name == "temp" else 10.0), 2)
    }

    encoded_json = json.dumps(json_message).encode("utf-8")
    sock.sendto(encoded_json, (MULTICAST_GROUP, PORT))
    print(f"Sent JSON: {json_message}")

    binary_message = os.urandom(8)
    sock.sendto(binary_message, (MULTICAST_GROUP, PORT))
    print(f"Sent binary: {binary_message}")

    time.sleep(2)

sock.close()