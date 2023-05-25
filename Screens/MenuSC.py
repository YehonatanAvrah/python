import threading
import tkinter
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from LobbySC import Lobby
from SettingsSC import Settings


class Menu(tkinter.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent
        self.geometry("750x600")
        self.title('Main Menu')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=750, height=600, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)

        # ====================Logo======================
        # self.icon = PhotoImage(file="../Photos/SAL_icon.png")
        # self.iconphoto(False, self.icon)
        self.logo_photo = Image.open("../Photos/SAL_Logo.png")
        self.logo = ImageTk.PhotoImage(self.logo_photo)
        self.canvas.create_image(15, 120, image=self.logo, anchor=NW)
        self.Username = str(username)  # self.parent.UserData.get()
        # wins_msg = ["GetWins", self.Username]
        # self.parent.send_msg(wins_msg, self.parent.client_socket)
        # self.UserWins = self.parent.recv_msg(self.parent.client_socket)
        self.create_gui()

    def create_gui(self):
        # ====================Labels======================
        print(self.Username)
        self.canvas.create_text(400, 120, text=f"Welcome back, {self.Username}", fill="black", font=self.LblFont)
        # self.WelMsg = "Welcome back, username" # + str(self.Username)
        # self.WelMsgLbl = Label(self, text=self.WelMsg, font=self.LblFont, bg='#AC94F4')
        # self.WelMsgLbl.place(x=255, y=120)
        # self.UserInfo = Label(self, text="username", font=self.LblFont, bg='light blue')
        # self.UserInfo.place(x=20, y=20)
        self.canvas.create_oval(20, 20, 225, 150, fill="light blue", outline="black", width=5)
        self.canvas.create_text(80, 82, text=self.Username, fill="black", font=self.LblFont)

        # ====================Buttons======================
        self.btn_settings = Button(self.canvas, text="Settings", command=self.open_settings, background="Gray", font=self.LblFont)
        self.btn_settings.place(x=625, y=20)
        self.btn_history = Button(self.canvas, text="Game History", command=self.open_history, background="#ff8b3d",
                                  font=self.LblFont)
        self.btn_history.place(x=125, y=420)
        self.btn_game = Button(self.canvas, text="Ready", command=self.open_lobby, background="lime", font=self.LblFont)
        self.btn_game.place(x=575, y=420)

        # self.btn_close = Button(self, text="Close", command=self.close, background="red", font=self.LblFont)
        # self.btn_close.place(x=625, y=80)

    def open_history(self):
        pass

    def open_settings(self):
        window = Settings(self)
        window.grab_set()
        self.withdraw()

    def open_lobby(self):
        window = Lobby(self)
        window.grab_set()
        self.withdraw()

    # def close(self):
    #     self.parent.deiconify()  # show parent
    #     self.destroy()  # close and destroy this screen

# M = Menu("Johnny")
# M.mainloop()

