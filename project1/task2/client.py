import os
import socket

HOST = os.environ.get("SERVER_HOST", "server")   # Compose service name
PORT = int(os.environ.get("SERVER_PORT", "50007"))

# this will connect to the server and send a message
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

# this will print the response from the server
print("CLIENT: received", repr(data), flush=True)