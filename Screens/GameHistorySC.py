import tkinter
from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font as font
from PIL import ImageTk, Image


class GameHistory(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent  # menu
        self.main_parent = parent.parent  # login
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry("700x425")
        self.title('Games History')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=700, height=425, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.LblFontUnder = font.Font(family='Comic Sans MS', weight="bold", size=15, underline=True)

        self.img = Image.open("../Photos/white_BG.png")
        self.resize = self.img.resize((700, 425), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.resize)
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        self.create_gui()

    def create_gui(self):
        self.canvas.create_text(355, 50, text=f"Games History", fill="black", font=self.LblFontUnder)
        self.table = ttk.Treeview(self, columns=("GameId", "Player1", "Player2", "Winner"), show="headings", height=10)
        self.table.column("GameId", anchor=CENTER, width=100, minwidth=100)
        self.table.column("Player1", anchor=CENTER, width=100, minwidth=100)
        self.table.column("Player2", anchor=CENTER, width=100, minwidth=100)
        self.table.column("Winner", anchor=CENTER, width=100, minwidth=100)
        self.table.heading("GameId", text="Game ID")
        self.table.heading("Player1", text="Player 1")
        self.table.heading("Player2", text="Player 2")
        self.table.heading("Winner", text="Winner")
        for column in self.table['columns']:
            self.table.column(column, stretch=False)
        self.table.place(x=148, y=80)
        self.history_tbl()

        # ====================Buttons======================
        self.btn_close = Button(self.canvas, text="Previous Window", command=self.open_menu, background="#d4af37",
                                font=self.LblFont)
        self.btn_close.place(x=160, y=325)
        self.btn_refresh = Button(self.canvas, text="Refresh Table", command=self.refresh_table,
                                  background="grey", font=self.LblFont)
        self.btn_refresh.place(x=375, y=325)

    def history_tbl(self):
        try:
            print("History Table")
            self.main_parent.send_msg("Games_History", self.main_parent.client_socket)
            data = self.main_parent.recv_msg(self.main_parent.client_socket, "list")
            print(data)
            for item in data:
                line = item.split()
                game_id = line[0]
                player1 = line[1]
                player2 = line[2]
                winner = line[3]
                self.table.insert("", "end", values=(game_id, player1, player2, winner), tags=("data",))
        except ConnectionResetError as e:
            print("Connection reset error in history:", str(e))  # Server disconnected
            self.main_parent.client_socket.close()
            self.main_parent.destroy()
        except:
            print("fail - history tbl")

    def open_menu(self):
        self.parent.deiconify()  # show parent
        self.destroy()  # close and destroy this screen

    def refresh_table(self):
        self.table.delete(*self.table.get_children())
        self.history_tbl()

    def on_closing(self):
        if messagebox.askokcancel("Quit Game", "Do you want to quit?"):
            self.main_parent.send_msg("exit", self.main_parent.client_socket)
            self.main_parent.destroy()
            self.main_parent.client_socket.close()

