import socket
import struct
import argparse
import time
import json

MULTICAST_GROUP = "224.1.1.1"
PORT = 5007
BUFFER_SIZE = 1024

parser = argparse.ArgumentParser()
parser.add_argument("--duration", type=int, default=15, help="seconds to listen before leaving")
args = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(("", PORT))

mreq = struct.pack("4sL", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

sock.settimeout(1)

print(f"Joined multicast group {MULTICAST_GROUP}:{PORT}")

start_time = time.time()

while time.time() - start_time < args.duration:
    try:
        data, addr = sock.recvfrom(BUFFER_SIZE)

        try:
            text = data.decode("utf-8")
            try:
                parsed = json.loads(text)
                print(f"Received JSON from {addr}: {parsed}")
            except json.JSONDecodeError:
                print(f"Received text from {addr}: {text}")
        except UnicodeDecodeError:
            print(f"Received binary from {addr}: {data}")

    except socket.timeout:
        pass

sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
print("Leaving multicast group")
sock.close()