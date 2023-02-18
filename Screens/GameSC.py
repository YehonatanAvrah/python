import tkinter
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image


class Game(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent
        self.geometry("750x600")
        self.title('Game Screen - Snakes And Ladders')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=750, height=600, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.Username = str(parent.Username)  # self.parent.UserData.get()
        #self.create_gui()

        # ====================Logo and Icon======================
        self.icon = PhotoImage(file="../Photos/SAL_icon.png")
        self.iconphoto(False, self.icon)
        self.logo_photo = Image.open("../Photos/SAL_Logo.png")
        self.logo = ImageTk.PhotoImage(self.logo_photo)
        self.canvas.create_image(15, 120, image=self.logo, anchor=NW)
