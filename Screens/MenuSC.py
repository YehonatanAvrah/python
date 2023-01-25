import threading
import tkinter
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image


class Menu(tkinter.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent
        self.geometry("1200x720")
        self.configure(bg='#D3D3D3')
        self.title('Main Menu')
        self.format = 'utf-8'
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.Username = username # self.parent.UserData.get()
        # self.img = Image.open('../Photos/Anya.jpg')
        # self.resizable(width=False, height=False)
        # self.resize = self.img.resize((1200, 720), Image.Resampling.LANCZOS)
        # self.bg = ImageTk.PhotoImage(self.resize)
        # self.imgLabel = Label(self, image=self.bg)
        # self.imgLabel.pack(expand=YES)


        # wins_msg = ["GetWins", self.Username]
        # self.parent.send_msg(wins_msg, self.parent.client_socket)
        # self.UserWins = self.parent.recv_msg(self.parent.client_socket)
        self.create_gui()

    def create_gui(self):
        print(self.Username)
        self.WelMsg = "Welcome back, " + str(self.Username)
        self.WelMsgLbl = Label(self, text=self.WelMsg, font=self.LblFont, bg='#D3D3D3')
        self.WelMsgLbl.place(x=500, y=250)

        self.btn_close = Button(self, text="Close", command=self.close, background="red", font=self.LblFont)
        self.btn_close.place(x=200, y=275)

    def close(self):
        self.parent.deiconify()  # show parent
        self.destroy()  # close and destroy this screen


