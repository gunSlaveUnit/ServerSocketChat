import socket
import threading

clients = []


def process_connection(server_sock):
    client_socket, addr = server_sock.accept()
    print(f'Accepted connection from {addr}')
    if addr not in clients:
        clients.append(addr)
    while True:
        request = client_socket.recv(4096)
        if not request:
            break
        print(request.decode())
        client_socket.send(b'Hello')


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 5000))
server_socket.listen()

while True:
    new_client_process = threading.Thread(target=process_connection, args=[server_socket])
    new_client_process.start()
