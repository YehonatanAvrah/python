import tkinter
from tkinter import *
import tkinter.font as font
from tkinter import messagebox

from PIL import ImageTk, Image


class Winning_Screen(tkinter.Toplevel):
    def __init__(self, parent):  # , winner
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent  # Game
        self.main_parent = parent.parent.parent.parent  # login
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry("750x600")
        self.title('Game Over')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=750, height=600, bg='#cc9e67')
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
        self.canvas.create_text(440, 355, text=self.winner, fill="gold", font=self.LblFont)
        self.canvas.create_text(300, 430, text=self.loser, fill="black", font=self.LblFont)
        self.btn_close = Button(self.canvas, text="Back To Menu", command=self.open_menu, background="red",
                                font=("Comic Sans MS", 13, "bold"))
        self.btn_close.place(x=10, y=10)

        # ====================Photos======================
        self.podium_photo = Image.open("../Photos/Podium.png")
        self.resize_podium = self.podium_photo.resize((290, 230), Image.Resampling.LANCZOS)
        self.podium = ImageTk.PhotoImage(self.resize_podium)
        self.canvas.create_image(375, 370, image=self.podium, anchor=N)

        self.crown_photo = Image.open("../Photos/crown.png")
        self.resize_crown = self.crown_photo.resize((55, 50), Image.Resampling.LANCZOS)
        self.crown = ImageTk.PhotoImage(self.resize_crown)
        self.canvas.create_image(440, 290, image=self.crown, anchor=N)

        if self.Username == self.winner:
            self.win_photo = Image.open("../Photos/win_banner.png")
            self.resize_win = self.win_photo.resize((500, 150), Image.Resampling.LANCZOS)
            self.win = ImageTk.PhotoImage(self.resize_win)
            self.canvas.create_image(125, 90, image=self.win, anchor=NW)
        else:
            self.lose_photo = Image.open("../Photos/lose_banner.png")
            self.resize_lose = self.lose_photo.resize((500, 150), Image.Resampling.LANCZOS)
            self.lose = ImageTk.PhotoImage(self.resize_lose)
            self.canvas.create_image(125, 90, image=self.lose, anchor=NW)

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
        self.parent.parent.parent.reset_wins_updated()  # reset the wins_updated flag
        self.parent.parent.parent.deiconify()  # show menu
        self.destroy()  # close and destroy this screen

    def on_closing(self):
        if messagebox.askokcancel("Quit Game", "Do you want to quit?"):
            self.main_parent.send_msg("exit", self.main_parent.client_socket)
            self.destroy()
            self.main_parent.client_socket.close()
