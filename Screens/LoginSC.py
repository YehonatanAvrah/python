import socket
import threading
import tkinter
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from tkinter.messagebox import showerror
from RegistrySC import Register
from MenuSC import Menu

SIZE = 8


class MainWindow(tkinter.Tk):  # create a window
    def __init__(self):
        super().__init__()
        self.title('Snakes and Ladders')
        self.geometry("650x650")
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handle_thread_socket()
        self.format = 'utf-8'

        self.icon = PhotoImage(file="../Photos/SAL_icon.png")
        self.iconphoto(False, self.icon)
        self.img = Image.open('../Photos/loginBG.png')
        self.resize = self.img.resize((650, 650), Image.Resampling.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.resize)
        self.imgLabel = Label(self, image=self.bg)
        self.imgLabel.pack(expand=YES)

        self.Email = StringVar()
        self.EmailLbl = Label(self, text="Email: ", width=10, font=self.LblFont)  # place a label on the window
        self.EmailLbl.place(x=100, y=25)
        self.EntEmail = Entry(self, textvariable=self.Email, font=self.LblFont)
        self.EntEmail.place(x=225, y=25)

        self.Password = StringVar()
        self.PasswordLbl = Label(self, text="Password: ", width=10, font=self.LblFont)  # place a label on the window
        self.PasswordLbl.place(x=100, y=75)
        self.EntPass = Entry(self, show='●', textvariable=self.Password, font=self.LblFont)
        self.EntPass.place(x=225, y=75)

        self.ShowIcon = Image.open('../photos/Show.png')
        self.ShowIconResize = self.ShowIcon.resize((22, 22), Image.Resampling.LANCZOS)
        self.ShowEye = ImageTk.PhotoImage(self.ShowIconResize)
        self.HideIcon = Image.open('../photos/Hide.png')
        self.HideIconResize = self.HideIcon.resize((22, 22), Image.Resampling.LANCZOS)
        self.HideEye = ImageTk.PhotoImage(self.HideIconResize)
        self.ShowHidePass = Button(self, image=self.ShowEye, command=self.toggle_pswrd, font=self.LblFont)
        self.ShowHidePass.place(x=435, y=75)

        self.UserData = StringVar()
        self.UserData.set("Please Login To Enter The Game")
        self.UserDataLbl = Label(self, textvariable=self.UserData, font=self.LblFont, background="yellow")
        self.UserDataLbl.place(x=100, y=125)

        self.NoAcc = Label(self, text="Don't have an account? Sign Up!", font=self.LblFont, fg="light blue", bg="red")
        self.NoAcc.place(x=100, y=275)

        self.btn_submit = Button(self, text="Login", command=self.login, width=10, background="lime", font=self.LblFont)
        self.btn_submit.place(x=100, y=175)
        self.btn_clear = Button(self, text="Clear", command=self.clear, width=10, background="red", font=self.LblFont)
        self.btn_clear.place(x=220, y=175)
        self.btn_register = Button(self, text='Sign Up', command=self.open_register, width=10, background="cyan", font=self.LblFont)
        self.btn_register.place(x=170, y=325)

    def clear(self):
        self.EntEmail.delete(0, END)
        self.EntPass.delete(0, END)

    def open_register(self):
        window = Register(self)
        window.grab_set()
        self.withdraw()

    def open_menu(self):
        window = Menu(self)
        window.grab_set()
        self.withdraw()

    def login(self):
        try:
            print("[logging in...]")
            arr = ["login", self.Email.get(), self.Password.get()]
            str_insert = ",".join(arr)
            print(str_insert)
            self.send_msg(str_insert, self.client_socket)
            data = self.recv_msg(self.client_socket)
            if data != "False":
                self.UserData.set(str(data))
                self.open_menu()
            else:
                err_msg = "Failed to log in, please register if you don't have an account"
                self.UserData.set(err_msg)
            print(data)
            return data
        except:
            print("fail :(")
            showerror("ERROR", 'Failed logging in')

    def toggle_pswrd(self):
        try:
            if self.EntPass.cget('show') == '':
                self.EntPass.config(show='●')
                self.ShowHidePass.config(image=self.ShowEye)
            else:
                self.EntPass.config(show='')
                self.ShowHidePass.config(image=self.HideEye)
        except:
            print("failed to show/hide")
            return False

    def handle_thread_socket(self):
        client_handler = threading.Thread(target=self.create_socket, args=())
        client_handler.daemon = True
        client_handler.start()

    def create_socket(self):
        self.client_socket.connect(('127.0.0.1', 1956))
        data = self.client_socket.recv(1024).decode()
        print("Data is " + data)
        print("Hello ", self.client_socket)

    def send_msg(self, data, client_socket):
        try:
            print("The message is: " + str(data))
            length = str(len(data)).zfill(SIZE)
            length = length.encode(self.format)
            print(length)
            if type(data) != bytes:
                data = data.encode()
            print(data)
            msg = length + data
            print("message with length is " + str(msg))
            client_socket.send(msg)
        except:
            print("Error with sending msg")

    def recv_msg(self, client_socket, ret_type="string"):  # ret_type is string by default unless stated otherwise
        try:
            length = client_socket.recv(SIZE).decode(self.format)
            if not length:
                print("NO LENGTH!")
                return None
            print("The length is " + length)
            data = client_socket.recv(int(length))  # .decode(self.format)
            if not data:
                print("NO DATA!")
                return None
            print("The data is: " + str(data))
            if ret_type == "string":
                data = data.decode(self.format)
            print(data)
            return data
        except:
            print("Error with receiving msg")


if __name__ == "__main__":
    M = MainWindow()
    M.mainloop()  # keep the window displaying
