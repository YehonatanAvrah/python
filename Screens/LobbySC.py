import tkinter
import threading
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from GameSC import Game


class Lobby(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent  # menu
        self.geometry("750x460")
        self.title('Lobby')
        self.format = 'utf-8'
        self.bg_color = self.parent.bg_color
        self.canvas = Canvas(self, width=750, height=460, bg=self.bg_color)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.LblFontUnder = font.Font(family='Comic Sans MS', weight="bold", size=15, underline=True)
        self.Username = str(parent.Username)  # self.parent.UserData.get()
        self.create_gui()

        # ====================Logo======================
        self.logo_photo = Image.open("../Photos/SAL_Logo.png")
        self.resize_logo = self.logo_photo.resize((600, 300), Image.Resampling.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.resize_logo)
        self.canvas.create_image(235, 165, image=self.logo, anchor=NW)

    def create_gui(self):
        # ====================Labels======================
        self.canvas.create_text(90, 125, text="Party Members", fill="black", font=self.LblFontUnder)
        self.canvas.create_oval(280, 40, 480, 180, fill="white", outline="black", width=5)
        self.canvas.create_oval(358, 202, 368, 212, fill="white", outline="black", width=3)
        self.canvas.create_oval(345, 190, 355, 200, fill="white", outline="black", width=3)
        self.wait = self.canvas.create_text(380, 110, text="Waiting\n For\n Players...", fill="Lime", font=self.LblFont)

        self.player_list = Listbox(self, font=self.LblFont, height=5, width=15, bg="black", fg="white")
        self.player_list.insert(1, self.Username)
        self.player_list.place(x=15, y=150)

        self.img = Image.open("../Photos/snake_timer.png")
        self.resize = self.img.resize((115, 115), Image.Resampling.LANCZOS)
        self.timer_img = ImageTk.PhotoImage(self.resize)
        self.canvas.create_image(610, 25, image=self.timer_img, anchor=NW)

        self.timer = 5
        self.timer_text = self.canvas.create_text(668, 85, text="", font=("Comic Sans MS", 20, "bold"))

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
            print(data)
            if data is not None:
                arr_data = data.split(",")
                if arr_data[0] == "Wait":  # one player in lobby
                    print("one player")
                    data = self.parent.parent.recv_msg(self.parent.parent.client_socket)
                    arr_data2 = data.split(",")
                    self.player_list.insert(2, arr_data2[1])
                    self.countdown()
                elif arr_data[0] == "Start":  # full party
                    print("two players")
                    self.player_list.insert(2, arr_data[1])
                    self.countdown()
        except:
            print("fail- lobby")

    def open_game(self):
        window = Game(self)
        window.grab_set()
        self.withdraw()

    def countdown(self):
        self.canvas.itemconfig(self.wait, text="Full Party,\n Starting Game...")  # (self.wait, state='hidden')
        if self.timer > 0:
            self.canvas.itemconfig(self.timer_text, text=str(self.timer))
            self.timer -= 1
            self.canvas.after(1000, self.countdown)
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
        self.open_game()
