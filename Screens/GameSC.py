import tkinter
import random
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image


class Game(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent
        self.geometry("1800x1010")
        self.title('Game Screen - Snakes And Ladders')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=1800, height=1010, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.Username = str(parent.Username)  # self.parent.UserData.get()
        self.create_gui()
        self.get_index()
        self.snakes = {38: 2, 50: 14, 55: 34, 65: 37, 93: 75, 99: 64}
        self.ladders = {4: 36, 29: 73, 42: 60, 63: 85, 71: 89}

    def create_gui(self):
        # --------Board--------
        self.board = Image.open("../Photos/Game_Board.png")  # Cyber/ProjectSAL/Photos/Game_Board.png
        self.board_resize = self.board.resize((1000, 800), Image.Resampling.LANCZOS)
        self.game_board = ImageTk.PhotoImage(self.board_resize)
        self.canvas.create_image(100, 20, image=self.game_board, anchor=NW)
        self.start = Image.open("../Photos/start_block.png")
        self.start_resize = self.start.resize((150, 150), Image.Resampling.LANCZOS)
        self.start_point = ImageTk.PhotoImage(self.start_resize)
        self.canvas.create_image(150, 975, image=self.start_point, anchor=S)

        # --------Dice--------
        self.arr_dice = []
        self.dice = Image.open("../Photos/Dice.png")
        self.dice_resize = self.dice.resize((65, 65), Image.Resampling.LANCZOS)
        self.dice_icon = ImageTk.PhotoImage(self.dice_resize)
        self.load_dice_nums()
        self.btn_roll = Button(self, image=self.dice_icon, command=self.roll_dice, height=80, width=80,
                               background="#AC94F4", activebackground="#AC94F4")
        self.btn_roll.place(x=1300, y=300)

        # --------pawns--------
        self.pawn1 = Image.open("../Photos/red_pawn.png")
        self.pawn1_resize = self.pawn1.resize((50, 50), Image.Resampling.LANCZOS)
        self.pawn_red = ImageTk.PhotoImage(self.pawn1_resize)
        self.player_1 = self.canvas.create_image(120, 925, image=self.pawn_red, anchor=S)
        self.player_pos1 = 0  # set the current position of the player1

        self.pawn2 = Image.open("../Photos/blue_pawn.png")
        self.pawn2_resize = self.pawn2.resize((50, 50), Image.Resampling.LANCZOS)
        self.pawn_blue = ImageTk.PhotoImage(self.pawn2_resize)
        self.player_2 = self.canvas.create_image(180, 925, image=self.pawn_blue, anchor=S)
        self.player_pos2 = 0  # set the current position of the player2


    def load_dice_nums(self):
        nums = ["../Photos/dice1.png", "../Photos/dice2.png", "../Photos/dice3.png", "../Photos/dice4.png",
                "../Photos/dice5.png", "../Photos/dice6.png"]
        for num in nums:
            self.dice_img = Image.open(num)
            self.dice_num_resize = self.dice_img.resize((65, 65), Image.Resampling.LANCZOS)
            self.dice_num = ImageTk.PhotoImage(self.dice_num_resize)
            self.arr_dice.append(self.dice_num)

    def roll_dice(self):
        r = random.randint(1, 6)
        # print(r)
        self.btn_roll.config(image=self.arr_dice[r - 1])

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
        for x in range(1, 11):
            row = 160  # x
            for y in range(1, 11):
                self.square_index[self.squares[i]] = (row, col)
                row = row + 100
                i = i + 1
            col = col + 80
        # print(self.square_index)

    def move_pawn(self, dice_result):
        self.player_pos1 = self.player_pos1 + dice_result  # calculate the new position of the player1
        # self.player_pos2 = self.player_pos2 + dice_result  # calculate the new position of the player2
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
        else:
            self.canvas.coords(self.player_1, self.square_index[self.player_pos1][0],
                               self.square_index[self.player_pos1][1])
        # self.canvas.coords(self.player_2, self.square_index[self.player_pos2][0], self.square_index[self.player_pos2][1])
