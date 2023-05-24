import tkinter
from tkinter import *
import tkinter.font as font
from PIL import Image


class Winning_Screen(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent  # Game
        self.main_parent = parent.parent.parent.parent  # login
        self.geometry("750x600")
        self.title('Game Over')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=750, height=600, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.Username = self.parent.Username
        self.opponent_name = self.parent.opponent_name
        self.winner = None
        self.loser = None
        self.get_winner()

        # ====================Icon======================
        # self.icon = PhotoImage(file="../Photos/SAL_icon.png")
        # self.iconphoto(False, self.icon)

        self.create_gui()

    def create_gui(self):
        # ====================Labels======================
        print(self.Username)
        self.canvas.create_text(400, 120, text=f"WINNER: {self.winner}", fill="black", font=self.LblFont)
        self.canvas.create_text(400, 180, text=f"LOSER: {self.loser}", fill="black", font=self.LblFont)

    def get_winner(self):
        try:
            print("get winner")
            arr = ["GetWinner", self.Username]
            str_insert = ",".join(arr)
            print(str_insert)
            self.main_parent.send_msg(str_insert, self.main_parent.client_socket)
            data = self.main_parent.recv_msg(self.main_parent.client_socket)
            print("Winner: " + str(data))
            if str(data) == self.Username:
                self.winner = self.Username
                self.loser = self.opponent_name
            elif str(data) == self.opponent_name:
                self.winner = self.opponent_name
                self.loser = self.Username
        except:
            print("FAIL- set winner")



