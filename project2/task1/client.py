import socket

HOST = "server"   # IMPORTANT: this matches docker-compose alias
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

data = client_socket.recv(1024)

print("Received:", data.decode())

client_socket.close()