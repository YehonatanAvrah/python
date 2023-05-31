import socket
import threading
from UsersDB import *
from GameHistoryDB import *
from Player import *
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import pickle

SIZE = 8


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.count = 0
        self.running = True
        self.format = 'utf-8'
        self.server_socket = None

        self.key = RSA.generate(2048)  # Generate RSA key pair
        self.private_key = self.key.export_key()  # private key
        self.public_key = self.key.publickey().export_key()  # public key

        self.userDb = Users()
        self.historyDb = GameHistory()
        self.players = []
        self.winner = None
        self.winners = []

    def start_server(self):
        try:
            print('[STARTING SERVER...]')
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
            self.server_socket.bind(self.addr)  # bind to port number
            self.server_socket.listen(1)  # server listens to X client at a time
            print(f"[LISTENING...] Server is listening on {self.addr}")

            while True:
                # Perform three-way handshake
                print("Waiting for a client")
                client_socket, address = self.server_socket.accept()  # create connection with client, first step: SYN
                print("New client connected")
                # self.send_msg("Connection with server successfully established", client_socket)
                self.send_msg(self.public_key, client_socket)  # Second step: SYN-ACK
                self.recv_msg(client_socket)  # Third step: ACK
                self.conn_handler(client_socket)
                self.count += 1
                print(f"current amount of clients: {self.count}")

        except socket.error as e:
            print(f"Socket error occurred: {e}")

    def encrypt(self, data):
        try:
            public_key = RSA.import_key(self.public_key)
            cipher = PKCS1_OAEP.new(public_key)
            encrypted_data = cipher.encrypt(data)
            return encrypted_data
        except:
            print("fail - encryption")
            return False

    def decrypt(self, encrypted_data):
        try:
            private_key = RSA.import_key(self.private_key)
            cipher = PKCS1_OAEP.new(private_key)
            decrypted_data = cipher.decrypt(encrypted_data)
            return decrypted_data
        except:
            print("fail - decryption")
            return False

    def send_msg(self, data, client_socket, msg_type="normal"):
        try:
            print("The message is: " + str(data))
            if type(data) != bytes and type(data) != list:
                data = data.encode()

            if msg_type == "encrypted":
                encrypted_data = self.encrypt(data)
                msg = b"encrypted" + encrypted_data
            elif msg_type == "list":
                print(type(data))
                msg = pickle.dumps(data)
                print(msg)
            else:
                msg = data

            length = str(len(msg)).zfill(SIZE)
            length = length.encode(self.format)
            print(length)

            msg_with_length = length + msg
            print("Message with length is: " + str(msg_with_length))
            client_socket.send(msg_with_length)
        except:
            print("Error with sending msg")

    def recv_msg(self, client_socket, ret_type="string"):
        try:
            length = client_socket.recv(SIZE).decode(self.format)
            if not length:
                print("NO LENGTH!")
                return None
            print("The length is " + length)

            data = b""
            remaining = int(length)
            while remaining > 0:
                chunk = client_socket.recv(remaining)
                if not chunk:
                    print("NO DATA!")
                    return None
                data += chunk
                remaining -= len(chunk)
            print("The data is: " + str(data))

            if data.startswith(b"encrypted"):
                encrypted_data = data[len(b"encrypted"):]
                decrypted_data = self.decrypt(encrypted_data)
                return decrypted_data.decode(self.format)
            else:
                if ret_type == "string":
                    return data.decode(self.format)
                else:
                    return data
        except:
            print("Error with receiving msg")
            return False

    def conn_handler(self, client_socket):
        client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
        client_handler.start()

    def handle_client(self, client_socket):
        running = True
        print(running)
        while running:
            try:
                print("---------------------------------\n")
                server_data = self.recv_msg(client_socket)
                if server_data is None or type(server_data) is bool:
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
                    if server_data == "Email exists":  # needs to add or server_data == "username_exists"
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
                    print(arr[1] + " is requesting for opponent's name")
                    self.get_names(arr[1])  # arr[1] = username

                elif arr and cmd == "GetID" and len(arr) == 2:
                    print(arr[1] + " is requesting for first player's name")
                    self.get_id(arr[1])  # arr[1] = username

                elif arr and cmd == "DiceResult" and len(arr) == 3:
                    print(f"Dice result: {arr[1]}")
                    self.handle_dice(arr[1], arr[2])  # arr[1] = result, arr[2] = username

                elif arr and cmd == "WinnerExist" and len(arr) == 2:
                    print(arr[1] + " sent the winner")
                    self.set_winner(arr[1])  # arr[1] = username

                elif arr and cmd == "GetWinner" and len(arr) == 2:
                    print(arr[1] + " is requesting for the winner's name")
                    self.get_winner(arr[1])  # arr[1] = username

                elif arr and cmd == "Games_History" and len(arr) == 1:
                    server_data = self.historyDb.get_history()
                    print("Server data: ", server_data)
                    self.send_msg(server_data, client_socket, "list")


                elif arr and cmd == "exit" and len(arr) == 1:
                    print("exit")
                    running = False  # change the variable to exit the loop
                    # server_data = "You've successfully disconnected"
                    self.count -= 1
                    # self.send_msg(server_data, client_socket)

                else:  # if the data from the client is false according to the protocol
                    server_data = "Please send data according to protocol"
                    self.send_msg(server_data, client_socket)  # General Error
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
            print(f"{player1.name}'s dice result")
            self.send_msg(str_data, player2.client_socket)
            # self.send_msg("WaitResult", player1.client_socket)
            # self.send_msg("PlayerID2Turn", player2.client_socket)
        elif username == player2.name:
            print(f"{player2.name}'s dice result")
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

    def get_id(self, username):
        player1 = self.players[0]
        player2 = self.players[1]
        print(f"{player1.name, player2.name}")
        if player1.name == username:
            self.send_msg(player1.name, player1.client_socket)
        elif player2.name == username:
            self.send_msg(player1.name, player2.client_socket)
        # self.send_msg(player1.name, player1.client_socket)  # sending the first player who entered the lobby
        # self.send_msg(player1.name, player2.client_socket)

    def set_winner(self, winner):
        player1 = self.players[0]
        player2 = self.players[1]
        #self.winner = None
        print(f"players: {player1.name, player2.name}, winner: {winner}")
        if player1.name == winner:
            self.winner = player1.name
        elif player2.name == winner:
            self.winner = player2.name
        self.historyDb.insert_game(player1.name, player2.name, self.winner)
        self.userDb.update_wins(self.winner)

    def get_winner(self, username):
        try:
            player1 = self.players[0]
            player2 = self.players[1]
            print("0")
            if player1.name == username:
                self.send_msg(self.winner, player1.client_socket)
                print("1")
            elif player2.name == username:
                self.send_msg(self.winner, player2.client_socket)
                print("2")
        except:
            print("fail - get winner")


if __name__ == '__main__':
    ip = '0.0.0.0'  # 127.0.0.1 means that it's this pc
    port = 1956
    S = Server(ip, port)
    S.start_server()
