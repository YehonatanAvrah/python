import socket
import threading
from UsersDB import *
from Player import *

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
        self.players = []

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
                print(f"current amount of clients: {self.count}")

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
                print("---------------------------------")
                server_data = self.recv_msg(client_socket)
                if server_data is None:
                    break
                print(server_data)
                arr = server_data.split(",")
                print(server_data)
                print(arr)
                cmd = arr[0]

                if arr and cmd == "register" and len(arr) == 6 and arr[4] != "Err_NotExist":
                    print("Register")
                    print(arr)
                    server_data = self.userDb.insert_user(arr[1], arr[2], arr[3], arr[4], arr[5])
                    print("server data:", server_data)
                    if server_data == "Email exists":
                        self.send_msg("Email already exists", client_socket)
                    if server_data:
                        self.send_msg("Successfully registered!", client_socket)
                    elif not server_data:
                        self.send_msg("ERROR>>> Failed to register user", client_socket)

                elif arr and cmd == "login" and len(arr) == 3:
                    print("login")
                    print(arr)
                    server_data = self.userDb.ret_user_by_email_and_pswrd(arr[1], arr[2])  # arr[1, 2] = email, password
                    print("server data:", server_data)
                    if server_data:
                        # msg = "Logged in successfully, Welcome back " + str(server_data)
                        # print(msg)
                        self.send_msg(server_data, client_socket)
                    elif not server_data:
                        print("ERROR>>> Failed to login")
                        # err_msg = "Failed to log in, please register if you don't have an account"
                        # print(err_msg)
                        self.send_msg("Err_NotExist", client_socket)

                elif arr and cmd == "waiting_room" and len(arr) == 2:
                    print("enter lobby " + arr[1])
                    self.handle_lobby(arr[1], client_socket)  # arr[1] = username

                elif arr and cmd == "GetOppoName" and len(arr) == 2:
                    print(arr[1] + "is requesting for opponent's name")
                    self.get_names(arr[1])  # arr[1] = username

                elif arr and cmd == "GetID" and len(arr) == 1:
                    print("Get order of entrance to game")
                    self.get_id()

                elif arr and cmd == "TurnFinish" and len(arr) == 2:
                    print("Check turn")
                    self.handle_game(arr[1])  # arr[1] = username

                elif arr and cmd == "DiceResult" and len(arr) == 3:
                    print(f"Dice result: {arr[1]}")
                    self.handle_dice(arr[1], arr[2])  # arr[1] = result, arr[2] = username

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
                self.count -= 1
                break
        client_socket.close()

    def handle_lobby(self, username, client_socket):
        print("handle lobby")
        player = Player(client_socket, username)
        self.players.append(player)
        print(len(self.players))
        if len(self.players) == 1:
            print("1 player")
            data = ["Wait", username]
            join_data = ",".join(data)
            self.send_msg(join_data, client_socket)
        elif len(self.players) == 2:
            print("2 players")
            player1 = self.players[0]
            player2 = self.players[1]
            socket1 = player1.client_socket
            socket2 = player2.client_socket
            data1 = ["Start", player1.name]
            data2 = ["Start", player2.name]
            str_data1 = ",".join(data1)
            str_data2 = ",".join(data2)
            print("Sending data")
            self.send_msg(str_data2, socket1)
            self.send_msg(str_data1, socket2)

    def handle_game(self, username):
        print("handle game")
        player1 = self.players[0]
        player2 = self.players[1]
        if username == player1.name:
            print(f"{player2.name} turn")
            self.send_msg("PlayerID2Turn", player1.client_socket)
            self.send_msg("PlayerID2Turn", player2.client_socket)
        elif username == player2.name:
            print(f"{player1.name} turn")
            self.send_msg("PlayerID1Turn", player1.client_socket)
            self.send_msg("PlayerID1Turn", player2.client_socket)

    def handle_dice(self, result, username):
        print("dice result")
        player1 = self.players[0]
        player2 = self.players[1]
        data = ["ResExist", result]
        str_data = ",".join(data)
        if username == player1.name:
            print(f"{player1.name} dice result")
            self.send_msg(str_data, player2.client_socket)
           # self.send_msg("WaitResult", player1.client_socket)
            #self.send_msg("PlayerID2Turn", player2.client_socket)
        elif username == player2.name:
            print(f"{player2.name} dice result")
            self.send_msg(str_data, player1.client_socket)
           # self.send_msg("WaitResult", player2.client_socket)

    def get_names(self, username):
        player1 = self.players[0]
        player2 = self.players[1]
        print(f"{player1.name, player2.name}")
        if player1.name == username:
            self.send_msg(player2.name, player1.client_socket)
        elif player2.name == username:
            self.send_msg(player1.name, player2.client_socket)

    def get_id(self):
        player1 = self.players[0]
        player2 = self.players[1]
        print(f"{player1.name, player2.name}")
        self.send_msg(player1.name, player1.client_socket)  # sending the first player who entered the lobby
        self.send_msg(player1.name, player2.client_socket)


if __name__ == '__main__':
    ip = '127.0.0.1'  # 127.0.0.1 means that it's this pc
    port = 1956
    S = Server(ip, port)
    S.start_server()
