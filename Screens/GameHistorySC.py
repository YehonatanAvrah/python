import tkinter
from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font as font


class GameHistory(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent  # menu
        self.main_parent = parent.parent  # login
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry("750x600")
        self.title('Games History')
        self.format = 'utf-8'
        self.canvas = Canvas(self, width=750, height=600, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)

        self.create_gui()

    def create_gui(self):
        self.canvas.create_text(375, 80, text=f"Games History", fill="black", font=self.LblFont)
        self.table = ttk.Treeview(self, columns=("GameId", "Player1", "Player2", "Winner"), show="headings", height=7)
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
        self.table.place(x=150, y=100)
        self.history_tbl()

        # ====================Buttons======================
        self.btn_close = Button(self.canvas, text="Previous Window", command=self.open_menu, background="#d4af37",
                                font=self.LblFont)
        self.btn_close.place(x=155, y=20)
        self.btn_refresh = Button(self.canvas, text="Refresh Table", command=self.refresh_table,
                                  background="grey", font=self.LblFont)
        self.btn_refresh.place(x=375, y=20)

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
            self.destroy()
            self.main_parent.client_socket.close()

