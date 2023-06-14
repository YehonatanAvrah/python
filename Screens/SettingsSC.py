import tkinter
from tkinter import *
import tkinter.font as font
from tkinter import messagebox
from tkinter.colorchooser import askcolor


class Settings(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent  # menu
        self.main_parent = parent.parent  # login
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry("950x620")
        self.title('Settings')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=950, height=620, bg='#bbbbbb')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.LblFontUnder = font.Font(family='Comic Sans MS', weight="bold", size=15, underline=True)

        self.create_gui()

    def create_gui(self):
        # ====================Labels======================
        self.canvas.create_text(140, 95, text="Game Instructions", fill="black", font=self.LblFontUnder)
        self.canvas.create_rectangle(50, 125, 900, 595, fill="#AC94F4", outline="black")
        self.canvas.create_text(150, 155, text="Game Accessories", fill="black", font=self.LblFontUnder)

        self.canvas.create_text(190, 220, text="● Board with 100 slots\n"
                                               "● Game Cube\n"
                                               "● Game Soldiers", fill="black", font=self.LblFont)

        self.canvas.create_text(120, 335, text="Game Rules", fill="black", font=self.LblFontUnder)
        self.canvas.create_text(460, 460, text="On the game board, there are numbers from 1 to 100 on each slot.\n"
                                               "In turns, the players roll a die. The number of slots that a player\n"
                                               "moves is equal to the value that comes out on the die.\n"
                                               "Some squares have ladders to help you go up the board to"
                                               " a higher number\n"
                                               "and skip some squares. There are also snakes that take you down to"
                                               " a lower\n"
                                               "number square, making you go back. The first player to reach the"
                                               " last square\n"
                                               "on the board, where the number 100 is written, wins!",
                                fill="black", font=self.LblFont)

        # ====================Buttons======================
        self.btn_logout = Button(self.canvas, text="Logout", command=self.open_login, background="red",
                                   font=self.LblFont)
        self.btn_logout.place(x=820, y=20)
        self.btn_close = Button(self.canvas, text="Previous Window", command=self.open_menu, background="#d4af37",
                                 font=self.LblFont)
        self.btn_close.place(x=620, y=20)
        self.btn_color = Button(self.canvas, text="Change Background", command=self.backgroundcolor,
                                background="light blue", font=self.LblFont)
        self.btn_color.place(x=50, y=20)

    def open_login(self):
        self.main_parent.deiconify()  # show main parent
        self.destroy()  # close and destroy this screen

    def open_menu(self):
        self.parent.deiconify()  # show parent
        self.destroy()  # close and destroy this screen

    def on_closing(self):
        if messagebox.askokcancel("Quit Game", "Do you want to quit?"):
            self.main_parent.send_msg("exit", self.main_parent.client_socket)
            self.main_parent.destroy()
            self.main_parent.client_socket.close()

    def backgroundcolor(self):
        color = askcolor()[1]
        self.parent.canvas.configure(bg=color)
        self.parent.bg_color = color
