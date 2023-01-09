import threading
import tkinter
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from Cyber.ProjectSAL.Databases.UsersDB import Users

SIZE = 8


class Register(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent
        self.geometry("1200x720")
        self.title('add user/register')
        self.format = 'utf-8'

        self.img = Image.open('../Photos/Anya2.jpg')
        self.resize = self.img.resize((1200, 720), Image.Resampling.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.resize)
        self.imgLabel = Label(self, image=self.bg)
        self.imgLabel.pack(expand=YES)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold")
        self.UsersDB = Users()

        self.create_gui()
        # Button(self, text='Close', command=self.close).pack(expand=True, side=BOTTOM)

    def create_gui(self):
        self.EmailP = StringVar()
        self.Email = Label(self, text="Email: ", width=10, font=self.LblFont)  # place a label on the window
        self.Email.place(x=100, y=25)
        self.EntEmail = Entry(self, textvariable=self.EmailP, font=self.LblFont)
        self.EntEmail.place(x=225, y=25)

        self.PasswordP = StringVar()
        self.Password = Label(self, text="Password: ", width=10, font=self.LblFont)  # place a label on the window
        self.Password.place(x=100, y=75)
        self.EntPass = Entry(self, textvariable=self.PasswordP, font=self.LblFont)
        self.EntPass.place(x=225, y=75)

        self.FNameP = StringVar()
        self.FName = Label(self, text="First Name: ", width=10, font=self.LblFont)  # place a label on the window
        self.FName.place(x=100, y=125)
        self.EntFName = Entry(self, textvariable=self.FNameP, font=self.LblFont)
        self.EntFName.place(x=225, y=125)

        self.button_reg = Button(self, text="Register", command=self.handle_add_user, font=self.LblFont, background="green")
        self.button_reg.place(x=100, y=175)

        self.btn_close = Button(self, text="Close", command=self.close, background="yellow", font=self.LblFont)
        self.btn_close.place(x=200, y=175)

    def handle_add_user(self):
        self.client_handler = threading.Thread(target=self.register_user, args=())
        self.client_handler.daemon = True
        self.client_handler.start()

    def register_user(self):
        print("register")
        arr = ["register", self.EmailP.get(), self.PasswordP.get(), self.FNameP.get()]
        str_insert = ",".join(arr)
        print(str_insert)
        self.parent.client_socket.send(str_insert.encode())
        data = self.parent.client_socket.recv(1024).decode()
        print(data)

    def close(self):
        self.parent.deiconify()  # show parent
        self.destroy()  # close and destroy this screen

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
