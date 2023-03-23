import tkinter
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image


class Game(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent
        self.geometry("1500x900")
        self.title('Game Screen - Snakes And Ladders')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=1500, height=900, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=True, height=True)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.Username = str(parent.Username)  # self.parent.UserData.get()
        self.create_gui()

    def create_gui(self):
        # --------Board--------
        self.board = Image.open("../Photos/Game_Board.png")
        self.board_resize = self.board.resize((800, 600), Image.Resampling.LANCZOS)
        self.game_board = ImageTk.PhotoImage(self.board_resize)
        self.canvas.create_image(100, 20, image=self.game_board, anchor=NW)
        self.start = Image.open("../Photos/start_block.png")
        self.start_resize = self.start.resize((100, 100), Image.Resampling.LANCZOS)
        self.start_point = ImageTk.PhotoImage(self.start_resize)
        self.canvas.create_image(50, 600, image=self.start_point, anchor=NW)

        # --------Dice--------
        self.dice = Image.open("../Photos/Dice.png")
        self.dice_resize = self.dice.resize((65, 65), Image.Resampling.LANCZOS)
        self.dice_icon = ImageTk.PhotoImage(self.dice_resize)
        self.btn_roll = Button(self, image=self.dice_icon, height=80, width=80, background="#AC94F4")
        self.btn_roll.place(x=1300, y=300)

        # --------pawns--------
        self.pawn1 = Image.open("../Photos/red_pawn.png")
        self.pawn1_resize = self.pawn1.resize((100, 100), Image.Resampling.LANCZOS)
        self.pawn_red = ImageTk.PhotoImage(self.pawn1_resize)
        self.canvas.create_image(50, 600, image=self.pawn_red, anchor=NW)

        self.pawn2 = Image.open("../Photos/blue_pawn.png")
        self.pawn2_resize = self.pawn2.resize((100, 100), Image.Resampling.LANCZOS)
        self.pawn_blue = ImageTk.PhotoImage(self.pawn2_resize)
        self.canvas.create_image(60, 600, image=self.pawn_blue, anchor=NW)
