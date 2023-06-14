import tkinter
from tkinter import *
import tkinter.font as font
from tkinter import messagebox
from PIL import ImageTk, Image
from LobbySC import Lobby
from SettingsSC import Settings
from GameHistorySC import GameHistory


class Menu(tkinter.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent
        self.geometry("750x600")
        self.title('Main Menu')
        self.wins_updated = True
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Visibility>", self.on_visibility_change)
        self.format = 'utf-8'
        self.bg_color = '#AC94F4'
        self.canvas = Canvas(self, width=750, height=600, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.LblFontUnder = font.Font(family='Comic Sans MS', weight="bold", size=15, underline=True)

        # ====================Logo======================
        self.logo_photo = Image.open("../Photos/SAL_Logo.png")
        self.logo = ImageTk.PhotoImage(self.logo_photo)
        self.canvas.create_image(15, 120, image=self.logo, anchor=NW)
        self.Username = str(username)  # self.parent.UserData.get()
        self.UserWins = StringVar()
        self.create_gui()
        self.get_wins()

    def create_gui(self):
        # ====================Labels======================
        print(self.Username)
        self.wel = self.canvas.create_text(400, 120, text=f"Welcome back, {self.Username}", fill='black',
                                           font=self.LblFontUnder)
        self.canvas.create_oval(20, 20, 225, 150, fill="light blue", outline="black", width=5)
        self.canvas.create_text(80, 82, text=self.Username, fill="black", font=self.LblFont)

        self.UserWinsDataLbl = Label(self, textvariable=self.UserWins, font=self.LblFont, bg='light blue')
        self.UserWinsDataLbl.place(x=175, y=68)
        self.crown_photo = Image.open("../Photos/crown.png")
        self.resize_crown = self.crown_photo.resize((35, 30), Image.LANCZOS)
        self.crown = ImageTk.PhotoImage(self.resize_crown)
        self.canvas.create_image(155, 70, image=self.crown, anchor=N)

        # ====================Buttons======================
        self.btn_settings = Button(self.canvas, text="Settings", command=self.open_settings, background="Gray", font=self.LblFont)
        self.btn_settings.place(x=625, y=20)
        self.btn_history = Button(self.canvas, text="Game History", command=self.open_history, background="#ff8b3d",
                                  font=self.LblFont)
        self.btn_history.place(x=125, y=420)
        self.btn_game = Button(self.canvas, text="Search Game", command=self.open_lobby, background="lime", font=self.LblFont)
        self.btn_game.place(x=525, y=420)

        # self.btn_close = Button(self, text="Close", command=self.close, background="red", font=self.LblFont)
        # self.btn_close.place(x=625, y=80)

    def open_history(self):
        window = GameHistory(self)
        window.grab_set()
        self.withdraw()

    def open_settings(self):
        window = Settings(self)
        window.grab_set()
        self.withdraw()

    def open_lobby(self):
        window = Lobby(self)
        window.grab_set()
        self.withdraw()

    def get_wins(self):
        try:
            wins_msg = ["GetWins", self.Username]
            str_insert = ",".join(wins_msg)
            print(str_insert)
            self.parent.send_msg(str_insert, self.parent.client_socket)
            data = self.parent.recv_msg(self.parent.client_socket)
            if data is not None:
                self.UserWins.set(data)
            else:
                print(f"UserWins - failed: {data}")
        except:
            print("fail - wins menu")

    def on_visibility_change(self, event):
        if self.state() == "normal" and not self.wins_updated:
            self.get_wins()
            self.wins_updated = True

    def reset_wins_updated(self):
        self.wins_updated = False

    def on_closing(self):
        if messagebox.askokcancel("Quit Game", "Do you want to quit?"):
            self.parent.send_msg("exit", self.parent.client_socket)
            self.parent.destroy()
            self.parent.client_socket.close()
