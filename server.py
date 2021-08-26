import socket
import threading
import time


class Server:
    def __init__(self, host='127.0.0.1', port=9876):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

    def run(self):
        print(f"[ Server started at {self.host}:{self.port} ]")
        while True:
            client, address = self.server.accept()
            time_connection = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
            print(f"[{address[0]}]=[{address[1]}]=[{time_connection}]/: New Connection")

            client.send('GETUSERNAME'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)

            time_connection = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
            self.send_broadcast_message(f"[{self.host}]=[{self.port}]=[{time_connection}]/[SERVER]: {nickname} => joined the chat".encode('utf8'))
            thread = threading.Thread(target=self.handle_client, args=(client, nickname))
            thread.start()

    def send_broadcast_message(self, message):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client, username):
        while True:
            try:
                message = client.recv(1024)
                self.send_broadcast_message(f"[{username}]/:".encode('utf8') + message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                break


if __name__ == '__main__':
    server_chat = Server()
    server_chat.run()
