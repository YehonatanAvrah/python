import tkinter
import random
from tkinter import *
import threading
import tkinter.font as font
from PIL import ImageTk, Image
from GameOverSC import Winning_Screen


class Game(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent  # lobby
        self.main_parent = parent.parent.parent  # login
        self.geometry("1800x1010")
        self.title('Game Screen - Snakes And Ladders')
        self.format = 'utf-8'
        self.bg_color = self.parent.parent.bg_color
        self.canvas = Canvas(self, width=1800, height=1010, bg=self.bg_color)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.Username = str(self.parent.Username)
        self.opponent_name = self.get_opp_name()
        self.player_id1 = None
        self.player_id2 = None
        self.current_player = None
        self.winner = None
        self.set_player_id()
        self.create_gui()
        self.get_index()
        self.snakes = {38: 2, 50: 14, 55: 34, 65: 37, 93: 75, 99: 64}  # top to bottom
        self.ladders = {4: 36, 29: 73, 42: 60, 63: 85, 71: 89}  # bottom to top
        self.running = True
        self.handle_recv_dice_result()

    def create_gui(self):
        # ====================Icon======================
        # self.icon = PhotoImage(file="../Photos/SAL_icon.png")
        # self.iconphoto(False, self.icon)

        # --------Board--------
        self.board = Image.open("../Photos/Game_Board.png")  # Cyber/ProjectSAL/Photos/Game_Board.png
        self.board_resize = self.board.resize((1000, 800), Image.Resampling.LANCZOS)
        self.game_board = ImageTk.PhotoImage(self.board_resize)
        self.canvas.create_image(100, 20, image=self.game_board, anchor=NW)
        self.start = Image.open("../Photos/start_block.png")
        self.start_resize = self.start.resize((150, 150), Image.Resampling.LANCZOS)
        self.start_point = ImageTk.PhotoImage(self.start_resize)
        self.canvas.create_image(150, 975, image=self.start_point, anchor=S)

        # --------Labels--------
        self.current_player = self.player_id1
        self.turn_lbl = Label(self, text=self.current_player + "'s turn!", width=20, height=5, font=self.LblFont,
                              fg="red", bg="yellow")
        self.turn_lbl.place(x=1200, y=110)
        if self.current_player != self.Username:
            self.turn_lbl.config(text=self.current_player + "'s turn!")
        else:
            self.turn_lbl.config(text="Your turn!")

        # --------Dice--------
        self.arr_dice = []
        self.dice = Image.open("../Photos/Dice.png")
        self.dice_resize = self.dice.resize((65, 65), Image.Resampling.LANCZOS)
        self.dice_icon = ImageTk.PhotoImage(self.dice_resize)
        self.load_dice_nums()
        self.btn_roll = Button(self, image=self.dice_icon, command=self.roll_dice, height=80, width=80,
                               background=self.bg_color, activebackground=self.bg_color)
        self.btn_roll.place(x=1300, y=300)
        if self.Username != self.player_id1:
            self.btn_roll.configure(state="disabled")
        else:
            self.btn_roll.configure(state="active")

        # --------pawns--------
        self.pawn1 = Image.open("../Photos/red_pawn.png")
        self.pawn1_resize = self.pawn1.resize((50, 50), Image.Resampling.LANCZOS)
        self.pawn_red = ImageTk.PhotoImage(self.pawn1_resize)
        self.player_1 = self.canvas.create_image(120, 925, image=self.pawn_red, anchor=S)
        self.player_pos1 = 90  # set the current position of the player1

        self.pawn2 = Image.open("../Photos/blue_pawn.png")
        self.pawn2_resize = self.pawn2.resize((50, 50), Image.Resampling.LANCZOS)
        self.pawn_blue = ImageTk.PhotoImage(self.pawn2_resize)
        self.player_2 = self.canvas.create_image(180, 925, image=self.pawn_blue, anchor=S)
        self.player_pos2 = 90  # set the current position of the player2

    def get_opp_name(self):
        try:
            print("oppo name")
            arr = ["GetOppoName", self.Username]
            str_insert = ",".join(arr)
            print(str_insert)
            self.main_parent.send_msg(str_insert, self.main_parent.client_socket)
            data = self.main_parent.recv_msg(self.main_parent.client_socket)
            print(data)
            return data
        except:
            print("FAIL- GetOppoName")
            return "FAIL- GetOppoName"

    def set_player_id(self):
        try:
            print("set id")
            arr = ["GetID", self.Username]
            str_insert = ",".join(arr)
            print(str_insert)
            self.main_parent.send_msg(str_insert, self.main_parent.client_socket)
            data = self.main_parent.recv_msg(self.main_parent.client_socket)
            print("The first player who entered the lobby: " + str(data))
            if str(data) == self.Username:
                self.player_id1 = self.Username
                self.player_id2 = self.opponent_name
            elif str(data) == self.opponent_name:
                self.player_id1 = self.opponent_name
                self.player_id2 = self.Username
        except:
            print("FAIL- set id")

    def player_turn(self):
        try:
            print("Finished his turn")
            arr = ["TurnFinish", self.Username]
            str_insert = ",".join(arr)
            print(str_insert)
            self.main_parent.send_msg(str_insert, self.main_parent.client_socket)
            data = self.main_parent.recv_msg(self.main_parent.client_socket)
            print(data)
            if data is not None:
                if data == "PlayerID1Turn":  # player1 turn
                    print("Player_id1 turn")
                    self.current_player = self.player_id1
                    # self.turn = 1
                    self.turn_lbl.config(text=self.current_player + "'s turn!")
                    if self.Username != self.current_player:
                        self.btn_roll.configure(state="disabled")
                    else:
                        self.btn_roll.configure(state="active")
                elif data == "PlayerID2Turn":  # player2 turn
                    print("Player_id2 Turn")
                    self.current_player = self.player_id2
                    # self.turn = 2
                    self.turn_lbl.config(text=self.current_player + "'s turn!")
                    if self.Username != self.current_player:
                        self.btn_roll.configure(state="disabled")
                    else:
                        self.btn_roll.configure(state="active")
        except:
            print("fail- game turn")

    def load_dice_nums(self):
        nums = ["../Photos/dice1.png", "../Photos/dice2.png", "../Photos/dice3.png", "../Photos/dice4.png",
                "../Photos/dice5.png", "../Photos/dice6.png"]
        for num in nums:
            self.dice_img = Image.open(num)
            self.dice_num_resize = self.dice_img.resize((65, 65), Image.Resampling.LANCZOS)
            self.dice_num = ImageTk.PhotoImage(self.dice_num_resize)
            self.arr_dice.append(self.dice_num)

    def handle_recv_dice_result(self):
        client_handler = threading.Thread(target=self.recv_dice_result, args=())
        client_handler.daemon = True
        client_handler.start()

    def recv_dice_result(self):
        try:
            if self.player_pos1 >= 100 or self.player_pos2 >= 100:
                self.running = False
            while self.running:
                if self.player_pos1 >= 100 or self.player_pos2 >= 100:
                    break
                # state = self.btn_roll.cget("state")
                # print("Button state:", state)
                # if state == "disabled":
                if self.current_player == self.opponent_name:
                    print("entered recv res")
                    if (self.running and self.player_pos1 < 100) or (self.running and self.player_pos2 < 100):
                        data = self.main_parent.recv_msg(self.main_parent.client_socket)
                        # if data == "Err_Recv":
                        #     self.running = False
                        #     break
                        print("Received data:", data)
                        data = data.split(",")
                        if data[0] == "ResExist":
                            print("Opponent's result exists.")
                            result = int(data[1])
                            print("Opponent's result:", result)
                            self.move_pawn(result)
                            #self.after(100, self.move_pawn, result)
                            self.after(200, self.btn_roll.configure(state="active"))
                        # self.btn_roll.configure(state="active")
                        else:
                            print("Invalid data received:", data)
                else:
                    # print("Receive operation skipped when it’s your turn")
                    pass
            print("out of while running>>>game over")
        except:
            print("failed in recv_dice_res")

    def roll_dice(self):
        r = random.randint(1, 6)
        # print(r)
        self.btn_roll.config(image=self.arr_dice[r - 1])
        self.after(300, self.btn_roll.configure(state="disabled"))
        # self.btn_roll.configure(state="disabled")
        print("current player playing: " + self.current_player)
        arr = ["DiceResult", str(r), self.Username]
        str_insert = ",".join(arr)
        print(str_insert)
        self.main_parent.send_msg(str_insert, self.main_parent.client_socket)
        self.after(300, self.move_pawn, r)

    def get_index(self):
        # X- difference of 100 btwn each square, Y- difference of 80 btwn each square
        # board starts at 100X20, every square is 100x80
        self.squares = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91,
                        81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
                        80, 79, 78, 77, 76, 75, 74, 73, 72, 71,
                        61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
                        60, 59, 58, 57, 56, 55, 54, 53, 52, 51,
                        41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                        40, 39, 38, 37, 36, 35, 34, 33, 32, 31,
                        21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                        20, 19, 18, 17, 16, 15, 14, 13, 12, 11,
                        1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        col = 90  # y
        i = 0
        self.square_index = {}  # to store x and y of every square
        for x in range(1, 11):  # rows
            row = 160  # x
            for y in range(1, 11):  # columns
                self.square_index[self.squares[i]] = (row, col)
                row = row + 100
                i = i + 1
            col = col + 80
        # print(self.square_index)

    def move_pawn(self, dice_result):
        # print(self.current_player)
        if self.current_player == self.player_id1:
            self.player_pos1 = self.player_pos1 + dice_result  # calculate the new position of the player1
            if self.player_pos1 >= 100:
                self.player_pos1 = 100
                self.running = False
            self.canvas.coords(self.player_1, self.square_index[self.player_pos1][0],
                               self.square_index[self.player_pos1][1])
            self.after(350, self.check_ladder_or_snake)
            if self.player_pos1 != 100:
                self.current_player = self.player_id2
                if self.current_player != self.Username:
                    self.turn_lbl.config(text=self.current_player + "'s turn!")
                else:
                    self.turn_lbl.config(text="Your turn!")
            else:
                self.winner = self.current_player
                self.after(350, self.handle_winner)
            #self.after(100, self.player_turn)
        elif self.current_player == self.player_id2:
            self.player_pos2 = self.player_pos2 + dice_result  # calculate the new position of the player2
            if self.player_pos2 >= 100:
                self.player_pos2 = 100
                self.running = False
            self.canvas.coords(self.player_2, self.square_index[self.player_pos2][0],
                               self.square_index[self.player_pos2][1])
            self.after(350, self.check_ladder_or_snake)
            if self.player_pos2 != 100:
                self.current_player = self.player_id1
                if self.current_player != self.Username:
                    self.turn_lbl.config(text=self.current_player + "'s turn!")
                else:
                    self.turn_lbl.config(text="Your turn!")
            else:
                self.winner = self.current_player
                self.after(350, self.handle_winner)

            # self.after(100, self.player_turn)

    def check_ladder_or_snake(self):
        if self.current_player == self.player_id1:
            if self.player_pos1 in self.ladders.keys():
                top_of_ladder = self.ladders[self.player_pos1]
                self.canvas.coords(self.player_1, self.square_index[top_of_ladder][0],
                                   self.square_index[top_of_ladder][1])
                self.player_pos1 = top_of_ladder
            elif self.player_pos1 in self.snakes.keys():
                bottom_of_snake = self.snakes[self.player_pos1]
                self.canvas.coords(self.player_1, self.square_index[bottom_of_snake][0],
                                   self.square_index[bottom_of_snake][1])
                self.player_pos1 = bottom_of_snake
        elif self.current_player == self.player_id2:
            if self.player_pos2 in self.ladders.keys():
                top_of_ladder = self.ladders[self.player_pos2]
                self.canvas.coords(self.player_2, self.square_index[top_of_ladder][0],
                                   self.square_index[top_of_ladder][1])
                self.player_pos2 = top_of_ladder
            elif self.player_pos2 in self.snakes.keys():
                bottom_of_snake = self.snakes[self.player_pos2]
                self.canvas.coords(self.player_2, self.square_index[bottom_of_snake][0],
                                   self.square_index[bottom_of_snake][1])
                self.player_pos2 = bottom_of_snake

    def open_win_screen(self):
        window = Winning_Screen(self)  # , self.winner
        window.grab_set()
        self.withdraw()

    def handle_winner(self):
        print(f"user: {self.Username}, curplayer: {self.current_player}, running: {self.running}")
        if self.Username == self.current_player:
            arr = ["WinnerExist", self.current_player]
            str_insert = ",".join(arr)
            print(str_insert)
            self.main_parent.send_msg(str_insert, self.main_parent.client_socket)
            data = self.main_parent.recv_msg(self.main_parent.client_socket)
            if data == "GameOver":
                self.open_win_screen()
            # self.handle_recv_dice_result()
        else:
            data = self.main_parent.recv_msg(self.main_parent.client_socket)
            if data == "GameOver":
                self.open_win_screen()
            # self.handle_recv_dice_result()
            # self.after(350, self.open_win_screen)
