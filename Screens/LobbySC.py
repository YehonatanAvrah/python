import tkinter
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
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
        self.player_list = Listbox(self)


        # ====================Logo and Icon======================
        self.icon = PhotoImage(file="../Photos/SAL_icon.png")
        self.iconphoto(False, self.icon)
        self.logo_photo = Image.open("../Photos/SAL_Logo.png")
        self.logo = ImageTk.PhotoImage(self.logo_photo)
        self.canvas.create_image(15, 120, image=self.logo, anchor=NW)
        self.Username = str(parent.username)  # self.parent.UserData.get()

        self.create_gui()

    def create_gui(self):
        # ====================Labels======================
        self.canvas.create_text(20, 20, text="Party Members", fill="black", font=self.LblFont)

    def lobby(self):
        try:
            print("lobby")
            arr = ["lobby", self.Username]
            str_insert = ",".join(arr)
            print(str_insert)
            self.parent.send_msg(str_insert, self.parent.client_socket)
            data = self.parent.recv_msg(self.parent.client_socket)
            if data is not None:
                arr_data = data.split(",")
                if arr_data[0] == "Wait":
                    self.player_list.insert(0, arr_data[1])
                elif arr_data[0] == "Start":
                    self.player_list.insert(1, arr_data[1])
                    self.start_queue()
        except:
            print("fail- lobby")

    def open_game(self, players):
        pass

    def start_queue(self):
        arr_players = []
        for i in self.player_list:
            arr_players.append(self.player_list.get(i))
        players_str = ",".join(arr_players)
        counter = 5
        TimerLbl = StringVar()
        TimerLbl.set(f"Waiting in queue {counter}")

        self.open_game(players_str)


