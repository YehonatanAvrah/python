import socket
import threading
import tkinter
from tkinter import *
import tkinter.font as font
# from PIL import ImageTk, Image
from tkinter.messagebox import showerror
# from Registery import Register


class MainWindow(tkinter.Tk):  # create a window
    def __init__(self):
        super().__init__()
        self.title('Snakes and Ladders')
        self.geometry("800x500")
        self.resizable(width=False, height=False)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handle_thread_socket()

        # self.img = Image.open('Anya.jpg')
        # self.resize = self.img.resize((800, 500), Image.Resampling.LANCZOS)
        # self.bg = ImageTk.PhotoImage(self.resize)
        # self.imgLabel = Label(self, image=self.bg)
        # self.imgLabel.pack(expand=YES)

        self.EmailP = StringVar()
        self.Email = Label(self, text="Email: ", width=10, font=self.LblFont)  # place a label on the window
        self.Email.place(x=100, y=25)
        self.EntEmail = Entry(self, textvariable=self.EmailP, font=self.LblFont)
        self.EntEmail.place(x=225, y=25)

        self.PasswordP = StringVar()
        self.Password = Label(self, text="Password: ", width=10, font=self.LblFont)  # place a label on the window
        self.Password.place(x=100, y=75)
        self.EntPass = Entry(self, show='*', textvariable=self.PasswordP, font=self.LblFont)
        self.EntPass.place(x=225, y=75)

        self.FNameP = StringVar()
        self.FName = Label(self, text="First Name: ", width=10, font=self.LblFont)  # place a label on the window
        self.FName.place(x=100, y=125)
        self.EntFName = Entry(self, textvariable=self.FNameP, font=self.LblFont)
        self.EntFName.place(x=225, y=125)

        # self.addressprint = StringVar()
        # self.address = Label(self, text="Address")  # place a label on the window
        # self.address.place(x=100, y=200)
        #
        # self.etaddress = Entry(self, textvariable=self.addressprint)
        # self.etaddress.place(x=200, y=200)
        #
        # self.phonenumprint = StringVar()
        # self.phonenum = Label(self, text="Phone Number")  # place a label on the window
        # self.phonenum.place(x=100, y=250)
        #
        # self.etphonenum = Entry(self, textvariable=self.phonenumprint)
        # self.etphonenum.place(x=200, y=250)
        # self.UserData = "Please Login"

        self.UserData = StringVar()
        self.UserData.set("Please Login")
        self.UserDataLbl = Label(textvariable=self.UserData, font=self.LblFont, background="yellow")
        self.UserDataLbl.place(x=100, y=125)  # , height=30

        self.btn_submit = Button(self, text="Login", command=self.login, background="lime", font=self.LblFont)
        self.btn_submit.place(x=100, y=325)
        self.btn_clear = Button(self, text="Clear", command=self.clear, background="red", font=self.LblFont)
        self.btn_clear.place(x=200, y=325)
        self.btn_register = Button(self, text='Register', command=self.open_register, background="cyan", font=self.LblFont)  # place a button on the window
        self.btn_register.place(x=300, y=325)


    def clear(self):
        self.EntEmail.delete(0, END)
        self.EntPass.delete(0, END)

    # def open_register(self):
    #     window = Register(self)
    #     window.grab_set()
    #     self.withdraw()

    def login(self):
        try:
            print("[logging in...]")
            arr = ["login", self.EmailP.get(), self.PasswordP.get()]
            str_insert = ",".join(arr)
            print(str_insert)
            self.client_socket.send(str_insert.encode())
            data = self.client_socket.recv(1024).decode()
            self.UserData.set(data)
            print(data)
            return data
        except:
            print("fail :(")
            showerror("ERROR", 'Failed logging in')

    def handle_thread_socket(self):
        client_handler = threading.Thread(target=self.create_socket, args=())
        client_handler.daemon = True
        client_handler.start()

    def create_socket(self):
        self.client_socket.connect(('127.0.0.1', 1956))
        data = self.client_socket.recv(1024).decode()
        print("Data is " + data)
        print("Hello ", self.client_socket)


if __name__ == "__main__":
    M = MainWindow()
    M.mainloop()  # keep the window displaying
