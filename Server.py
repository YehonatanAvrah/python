import socket
import threading
from Users import *


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.count = 0
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Create a TCP/IP socket

        self.userDb = User()

    def start(self):
        try:
            print('server starting up on ip %s port %s' % (self.ip, self.port))
            self.sock.bind((self.ip, self.port))
            self.sock.listen(3)

            while True:
                print('waiting for a new client')
                client_socket, client_addresses = self.sock.accept()
                print('new client entered')
                client_socket.send('Hello this is server'.encode())
                self.count += 1
                print(self.count)
                self.conn_handler(client_socket)

        except socket.error as e:
            print(e)

    def conn_handler(self, client_socket):
        client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
        client_handler.start()

    def handle_client(self, client_socket):
        not_crash = True
        print(not_crash)
        while self.running:
            while not_crash:
                try:
                    server_data = client_socket.recv(1024).decode('utf-8')
                    # insert,email,password,firstname
                    arr = server_data.split(",")
                    print(server_data)

                    if arr and arr[0] == "register" and len(arr) == 4:
                        print("register user")
                        print(arr)
                        server_data = self.userDb.insert_user(arr[1], arr[2], arr[3])
                        print("server data:", server_data)
                        if server_data:
                            client_socket.send("success register".encode())
                        elif server_data:
                            client_socket.send("failed register".encode())

                    elif arr and arr[0] == "login" and len(arr) == 3:
                        print("user logging in")
                        print(arr)
                        server_data = self.userDb.return_user_by_email(arr[1], arr[2])
                        print("server data:", server_data)
                        if server_data:
                            msg = "Logged in successfully, Welcome back " + str(server_data)
                            print(msg)
                            client_socket.send(msg.encode())
                        elif not server_data:
                            client_socket.send("Failed to log in, please register if you don't have an account".encode())

                    elif arr and arr[0] == "get_all_users" and len(arr) == 1:
                        print("get_all_users")
                        server_data = self.userDb.select_all_users()
                        server_data = ",".join(server_data)  # convert data to string
                        client_socket.send(server_data.encode())

                    else:
                        server_data = "There was an error"
                        client_socket.send(server_data.encode())
                except:
                    print("error")
                    not_crash = False
                    break


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 1956
    s = Server(ip, port)
    s.start()
