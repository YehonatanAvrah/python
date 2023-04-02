import tkinter
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

    def create_gui(self):
        # --------Board--------
        self.board = Image.open("../Cyber/ProjectSAL/Photos/Game_Board.png")  # Cyber/ProjectSAL/Photos/Game_Board.png
        self.board_resize = self.board.resize((1000, 800), Image.Resampling.LANCZOS)
        self.game_board = ImageTk.PhotoImage(self.board_resize)
        self.canvas.create_image(100, 20, image=self.game_board, anchor=NW)
        self.start = Image.open("../Cyber/ProjectSAL/Photos/start_block.png")
        self.start_resize = self.start.resize((150, 150), Image.Resampling.LANCZOS)
        self.start_point = ImageTk.PhotoImage(self.start_resize)
        self.canvas.create_image(150, 975, image=self.start_point, anchor=S)

        # --------Dice--------
        self.arr_dice = []
        self.dice = Image.open("../Cyber/ProjectSAL/Photos/Dice.png")
        self.dice_resize = self.dice.resize((65, 65), Image.Resampling.LANCZOS)
        self.dice_icon = ImageTk.PhotoImage(self.dice_resize)
        self.load_dice_nums()
        self.btn_roll = Button(self, image=self.dice_icon, command=self.roll_dice, height=80, width=80,
                               background="#AC94F4", activebackground="#AC94F4")
        self.btn_roll.place(x=1300, y=300)

        # --------pawns--------
        self.pawn1 = Image.open("../Cyber/ProjectSAL/Photos/red_pawn.png")
        self.pawn1_resize = self.pawn1.resize((50, 50), Image.Resampling.LANCZOS)
        self.pawn_red = ImageTk.PhotoImage(self.pawn1_resize)
        self.canvas.create_image(120, 925, image=self.pawn_red, anchor=S)

        self.pawn2 = Image.open("../Cyber/ProjectSAL/Photos/blue_pawn.png")
        self.pawn2_resize = self.pawn2.resize((50, 50), Image.Resampling.LANCZOS)
        self.pawn_blue = ImageTk.PhotoImage(self.pawn2_resize)
        self.canvas.create_image(180, 925, image=self.pawn_blue, anchor=S)

    def load_dice_nums(self):
        nums = ["../Cyber/ProjectSAL/Photos/dice1.png", "../Cyber/ProjectSAL/Photos/dice2.png",
                "../Cyber/ProjectSAL/Photos/dice3.png", "../Cyber/ProjectSAL/Photos/dice4.png",
                "../Cyber/ProjectSAL/Photos/dice5.png", "../Cyber/ProjectSAL/Photos/dice6.png"]
        for num in nums:
            self.dice_img = Image.open(num)
            self.dice_num_resize = self.dice_img.resize((65, 65), Image.Resampling.LANCZOS)
            self.dice_num = ImageTk.PhotoImage(self.dice_num_resize)
            self.arr_dice.append(self.dice_num)

    def roll_dice(self):
        r = random.randint(1, 6)
        # print(r)
        self.btn_roll.config(image=self.arr_dice[r - 1])
