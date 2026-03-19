import socket
import sys

HOST = "0.0.0.0"
PORT = 5000

# get server name from command line (server1, server2, server3)
server_name = sys.argv[1]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"{server_name} ready on port {PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"{server_name} accepted connection from {addr}")

    message = f"Hello from {server_name}"
    conn.sendall(message.encode())

    conn.close()