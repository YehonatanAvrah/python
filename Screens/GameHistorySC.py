import tkinter
from tkinter import *
import tkinter.font as font
from PIL import Image


class GameHistory(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent  # menu
        self.main_parent = parent.parent  # login
        self.geometry("750x600")
        self.title('Games History')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=750, height=600, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)

        # ====================Icon======================
        # self.icon = PhotoImage(file="../Photos/SAL_icon.png")
        # self.iconphoto(False, self.icon)

    def create_gui(self):
        self.canvas.create_text(375, 80, text=f"Games History", fill="black", font=self.LblFont)
