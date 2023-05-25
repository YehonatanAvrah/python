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
        self.geometry("750x600")
        self.title('Lobby')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=750, height=600, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.bind("<Unmap>", self.minimize_window)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.Username = str(parent.Username)  # self.parent.UserData.get()
        self.create_gui()

        # ====================Logo and Icon======================
        # self.icon = PhotoImage(file="../Photos/SAL_icon.png")
        # self.iconphoto(False, self.icon)
        self.logo_photo = Image.open("../Photos/SAL_Logo.png")
        self.logo = ImageTk.PhotoImage(self.logo_photo)
        self.canvas.create_image(15, 120, image=self.logo, anchor=NW)

    def create_gui(self):
        # ====================Labels======================
        self.canvas.create_text(85, 20, text="Party Members", fill="black", font=self.LblFont)
        self.wait = self.canvas.create_text(300, 450, text="Waiting For Players...", fill="Lime", font=self.LblFont)
        self.timer = 5
        #self.timer.set("5")
        self.TimerLbl = Label(self.canvas, text=self.timer)
        self.TimerLbl.place(x=630, y=15)
        self.player_list = Listbox(self, font=self.LblFont)
        self.player_list.insert(1, self.Username)
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
        # self.timer = 5  # int(self.timer)
        # print(type(self.timer))
        self.canvas.itemconfig(self.wait, text="Full Party, Starting Queue...")  # (self.wait, state='hidden')
        if self.timer >= 0:
            # self.UserData.set("Logged in successfully, Welcome back")
            self.TimerLbl.configure(text="%d" % self.timer)
            self.timer -= 1
            self.TimerLbl.after(1000, self.countdown)
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

    def minimize_window(self, event):
        self.iconify()

