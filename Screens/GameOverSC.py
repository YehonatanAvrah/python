import tkinter
from tkinter import *
import tkinter.font as font


class Winning_Screen(tkinter.Toplevel):
    def __init__(self, parent):  # , winner
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
        self.set_winner()

        self.create_gui()

    def create_gui(self):
        # ====================Labels======================
        print(self.Username)
        self.canvas.create_text(400, 120, text=f"WINNER: {self.winner}", fill="black", font=self.LblFont)
        self.canvas.create_text(400, 180, text=f"LOSER: {self.loser}", fill="black", font=self.LblFont)
        self.btn_close = Button(self.canvas, text="Back To Menu", command=self.open_menu, background="#d4af37",
                                font=self.LblFont)
        self.btn_close.place(x=155, y=250)

    def set_winner(self):
        try:
            print("get winner")
            arr = ["GetWinner", self.Username]
            str_insert = ",".join(arr)
            print(str_insert)
            self.main_parent.send_msg(str_insert, self.main_parent.client_socket)
            data = self.main_parent.recv_msg(self.main_parent.client_socket)
            print("Winner: " + str(data))
            # data = self.winner
            if str(data) == self.Username:
                self.winner = self.Username
                self.loser = self.opponent_name
            elif str(data) == self.opponent_name:
                self.winner = self.opponent_name
                self.loser = self.Username
        except:
            print("FAIL- set winner")

    def open_menu(self):
        arr = ["leave_win", self.Username]
        str_insert = ",".join(arr)
        print(str_insert)
        self.main_parent.send_msg(str_insert, self.main_parent.client_socket)
        self.parent.parent.parent.deiconify()  # show menu
        self.destroy()  # close and destroy this screen
