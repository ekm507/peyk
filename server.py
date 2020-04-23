import socket
import sys
import threading
import time

class server:
    def __init__(self, ip, port, max_clients, buffer_size, username, password):
        self.ip = ip
        self.port = port
        self.counter = 0
        self.clients = dict()
        self.logins = dict()
        self.buffer = buffer_size
        self.max_clients = max_clients
    
    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.ip, self.port))
            self.socket.listen(self.max_clients)
            
            while True:
                client_socket, address = self.socket.accept()
                self.counter += 1
                client_id = self.counter # DON'T DO THIS AT HOME
                self.clients[client_id] = client_socket
                threading.Thread(target=self.data_handler, args=(client_socket, client_id)).start()

        except socket.error:
            print("Error, terminating connection ...")
            time.sleep(0.5)
            sys.exit()

    def data_handler(self, client_socket, client_id):
        hello_message = "FROM SERVER: you are doomed."

        client_socket.send(hello_message.encode("utf-8"))

        while True:
            try:
                data = client_socket.recv(self.buffer)
                if not data:
                    break
                self.send(data)
            except ConnectionResetError:
                break

    def send(self, data):
        for client_id, client_socket in self.clients:
            client_socket.send(data)
    
    def shutdown(self):
        for client_id, client_socket in self.clients:
            client_socket.send(data)