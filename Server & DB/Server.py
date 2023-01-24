import socket
import threading
from UsersDB import *

SIZE = 8


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.count = 0
        self.running = True
        self.format = 'utf-8'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket
        self.userDb = Users()

    def start_server(self):
        try:
            print('[STARTING SERVER...]')
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
            server_socket.bind(self.addr)  # bind to port number
            server_socket.listen(1)  # server listens to X client at a time
            print(f"[LISTENING...] Server is listening on {self.addr}")

            while True:
                print("Waiting for a client")
                client_socket, address = server_socket.accept()  # creating connection with client
                self.conn_handler(client_socket)
                print("New client connected")
                self.send_msg("Connection with server successfully established", client_socket)
                self.count += 1
                print(self.count)

        except socket.error as e:
            print(e)

    def send_msg(self, data, client_socket):
        try:
            print("The message is: " + str(data))
            length = str(len(data)).zfill(SIZE)
            length = length.encode(self.format)
            print(length)
            if type(data) != bytes:
                data = data.encode()
            print(data)
            msg = length + data
            print("message with length is " + str(msg))
            client_socket.send(msg)
        except:
            print("Error with sending msg")

    def recv_msg(self, client_socket, ret_type="string"):  # ret_type is string by default unless stated otherwise
        try:
            length = client_socket.recv(SIZE).decode(self.format)
            if not length:
                print("NO LENGTH!")
                return None
            print("The length is " + length)
            data = client_socket.recv(int(length))  # .decode(self.format)
            if not data:
                print("NO DATA!")
                return None
            print("The data is: " + str(data))
            if ret_type == "string":
                data = data.decode(self.format)
            print(data)
            return data
        except:
            print("Error with receiving msg")

    def conn_handler(self, client_socket):
        client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
        client_handler.start()

    def handle_client(self, client_socket):
        running = True
        print(running)
        while running:
            try:
                server_data = self.recv_msg(client_socket)
                if server_data is None:
                    break
                print(server_data)
                arr = server_data.split(",")
                print(server_data)
                print(arr)
                cmd = arr[0]
                if arr and cmd == "register" and len(arr) == 6 and arr[4] != "False":
                    print("Register")
                    print(arr)
                    server_data = self.userDb.insert_user(arr[1], arr[2], arr[3], arr[4], arr[5])
                    print("server data:", server_data)
                    if server_data == "Email exists":
                        self.send_msg("Email already exists", client_socket)
                    if server_data:
                        self.send_msg("Successfully registered!", client_socket)
                    elif not server_data:
                        self.send_msg("EROR>>> Failed to register user", client_socket)

                elif arr and cmd == "login" and len(arr) == 3:
                    print("login")
                    print(arr)
                    server_data = self.userDb.ret_user_by_email_and_pswrd(arr[1], arr[2])
                    print("server data:", server_data)
                    if server_data:
                        # msg = "Logged in successfully, Welcome back " + str(server_data)
                        # print(msg)
                        self.send_msg(server_data, client_socket)
                    elif not server_data:
                        print("EROR>>> Failed to login")
                        # err_msg = "Failed to log in, please register if you don't have an account"
                        # print(err_msg)
                        self.send_msg("False", client_socket)

                elif arr and cmd == "exit" and len(arr) == 1:
                    print("exit")
                    running = False  # change the variable to exit the loop
                    server_data = "You've successfully disconnected"
                    self.count -= 1
                    self.send_msg(server_data, client_socket)

                else:  # if the data from the client is false according to the protocol
                    server_data = "Please send data according to protocol"
                    self.send_msg(server_data, client_socket)
                # print("server sends>>> " + server_data)

            except socket.error as e:
                print(e)
                running = False
                break
        client_socket.close()


if __name__ == '__main__':
    ip = '127.0.0.1'  # 127.0.0.1 means that it's this pc
    port = 1956
    S = Server(ip, port)
    S.start_server()
