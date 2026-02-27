import os
import socket

HOST = os.environ.get("SERVER_HOST", "server")   # Compose service name
PORT = int(os.environ.get("SERVER_PORT", "50007"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print("CLIENT: received", repr(data), flush=True)