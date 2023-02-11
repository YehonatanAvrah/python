import tkinter
import threading
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from GameSC import Game
import time


class Lobby(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent
        self.geometry("750x600")
        self.title('Lobby')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=750, height=600, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.Username = str(parent.Username)  # self.parent.UserData.get()
        self.create_gui()

        # ====================Logo and Icon======================
        self.icon = PhotoImage(file="../Photos/SAL_icon.png")
        self.iconphoto(False, self.icon)
        self.logo_photo = Image.open("../Photos/SAL_Logo.png")
        self.logo = ImageTk.PhotoImage(self.logo_photo)
        self.canvas.create_image(15, 120, image=self.logo, anchor=NW)

    def create_gui(self):
        # ====================Labels======================
        self.canvas.create_text(85, 20, text="Party Members", fill="black", font=self.LblFont)
        self.timer = StringVar()
        self.timer.set("5")
        self.TimerLbl = Label(self.canvas, textvariable=self.timer)
        self.player_list = Listbox(self)
        self.player_list.place(x=25, y=40)
        self.handle_wait_for_player()

    def handle_wait_for_player(self):
        self.client_handler = threading.Thread(target=self.wait_for_player, args=())
        self.client_handler.daemon = True
        self.client_handler.start()

    def wait_for_player(self):
        try:
            print("wait for player")
            arr = ["waiting_room", self.Username]
            str_insert = ",".join(arr)
            print(str_insert)
            self.parent.parent.send_msg(str_insert, self.parent.parent.client_socket)
            data = self.parent.parent.recv_msg(self.parent.parent.client_socket)
            if data is not None:
                arr_data = data.split(",")
                if arr_data[0] == "Wait":  # one player in lobby
                    print("one player")
                    self.player_list.insert(1, arr_data[1])
                elif arr_data[0] == "Start":  # full party
                    print("two player")
                    self.player_list.insert(2, arr_data[1])
                    self.countdown()
        except:
            print("fail- lobby")

    def open_game(self):
        window = Game(self)
        window.grab_set()
        self.withdraw()

    def countdown(self):
        if str(self.timer) >= "0":
            # self.UserData.set("Logged in successfully, Welcome back")
            self.TimerLbl.config(str(self.timer))
            self.TimerLbl.after(1000, self.countdown, int(str(self.timer)) - 1)
        else:
            self.open_game()

    def start_queue(self):
        arr_players = []
        for i in self.player_list:
            arr_players.append(self.player_list.get(i))
        players_str = ",".join(arr_players)
        counter = 5
        TimerLbl = StringVar()
        TimerLbl.set(f"Waiting in queue {counter}")

        self.open_game(players_str)


