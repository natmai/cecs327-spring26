import socket

HOST = ""        # all interfaces
PORT = 50007     # example non-privileged port (from Python docs)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"SERVER: listening on port {PORT}", flush=True)

    while True:
        conn, addr = s.accept()
        with conn:
            print("SERVER: connected by", addr, flush=True)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)  # echo back