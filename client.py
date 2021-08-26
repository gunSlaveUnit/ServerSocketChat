import socket
import threading


class Client:
    def __init__(self, host='127.0.0.1', port=9876):
        self.host = host
        self.port = port
        self.username = input("Enter username: ")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.client.connect((self.host, self.port))

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'GETUSERNAME':
                    self.client.send(self.username.encode('utf-8'))
                else:
                    print(message)
            except:
                print("Something was wrong")
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{input(f"[{self.username}]/: ")}'
            self.client.send(message.encode('utf-8'))


if __name__ == '__main__':
    client_chat = Client()
    client_chat.run()
