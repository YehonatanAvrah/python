import threading
import tkinter
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image


class Menu(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent
        self.geometry("1200x720")
        self.title('Main Menu')
        self.format = 'utf-8'

        self.img = Image.open('../Photos/Anya2.jpg')
        # self.resizable(width=False, height=False)
        self.resize = self.img.resize((1200, 720), Image.Resampling.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.resize)
        self.imgLabel = Label(self, image=self.bg)
        self.imgLabel.pack(expand=YES)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold")

        self.create_gui()

    def create_gui(self):
        self.btn_close = Button(self, text="Close", command=self.close, background="yellow", font=self.LblFont)
        self.btn_close.place(x=200, y=275)

    def close(self):
        self.parent.deiconify()  # show parent
        self.destroy()  # close and destroy this screen


