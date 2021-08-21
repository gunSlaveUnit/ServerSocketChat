import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5000))

while True:
    message = input("/: ")
    client_socket.send(message.encode())
    response = client_socket.recv(4096)
    print(response.decode())
