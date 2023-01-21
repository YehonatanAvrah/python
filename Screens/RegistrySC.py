import threading
import tkinter
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image

SIZE = 8


class Register(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client_handler = None
        self.parent = parent
        self.geometry("1200x720")
        self.title('Registration')
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
        self.Email = StringVar()
        self.EmailLbl = Label(self, text="Email: ", width=10, font=self.LblFont)  # place a label on the window
        self.EmailLbl.place(x=100, y=25)
        self.EntEmail = Entry(self, textvariable=self.Email, font=self.LblFont)
        self.EntEmail.place(x=225, y=25)

        self.Password = StringVar()
        self.PasswordLbl = Label(self, text="Password: ", width=10, font=self.LblFont)  # place a label on the window
        self.PasswordLbl.place(x=100, y=75)
        self.EntPass = Entry(self, show='*', textvariable=self.Password, font=self.LblFont)
        self.EntPass.place(x=225, y=75)

        self.FName = StringVar()
        self.FNameLbl = Label(self, text="First Name: ", width=10, font=self.LblFont)  # place a label on the window
        self.FNameLbl.place(x=100, y=125)
        self.EntFName = Entry(self, textvariable=self.FName, font=self.LblFont)
        self.EntFName.place(x=225, y=125)

        self.LName = StringVar()
        self.LNameLbl = Label(self, text="Last Name: ", width=10, font=self.LblFont)  # place a label on the window
        self.LNameLbl.place(x=100, y=175)
        self.EntLName = Entry(self, textvariable=self.LName, font=self.LblFont)
        self.EntLName.place(x=225, y=175)

        self.Username = StringVar()
        self.UsernameLbl = Label(self, text="Username: ", width=10, font=self.LblFont)  # place a label on the window
        self.UsernameLbl.place(x=100, y=225)
        self.EntUsername = Entry(self, textvariable=self.Username, font=self.LblFont)
        self.EntUsername.place(x=225, y=225)

        self.SucReg = StringVar()
        self.SucReg.set("Please Enter Information To Register")
        self.SucRegLbl = Label(self, textvariable=self.SucReg, font=self.LblFont, background="yellow")
        self.SucRegLbl.place(x=100, y=325)

        self.button_reg = Button(self, text="Register", command=self.handle_add_user, font=self.LblFont, background="green")
        self.button_reg.place(x=100, y=275)

        self.btn_close = Button(self, text="Close", command=self.close, background="yellow", font=self.LblFont)
        self.btn_close.place(x=200, y=275)

    def handle_add_user(self):
        self.client_handler = threading.Thread(target=self.register_user, args=())
        self.client_handler.daemon = True
        self.client_handler.start()

    def register_user(self):
        print("register")
        arr = ["register", self.Email.get(), self.FName.get(), self.LName.get(), self.Username.get(),
               self.Password.get()]
        str_insert = ",".join(arr)
        print(str_insert)
        self.parent.send_msg(str_insert, self.parent.client_socket)
        data = self.parent.recv_msg(self.parent.client_socket)
        self.SucReg.set(data)
        self.EntEmail.delete(0, END)
        self.EntPass.delete(0, END)
        self.EntFName.delete(0, END)
        self.EntLName.delete(0, END)
        self.EntUsername.delete(0, END)
        print(data)

    def close(self):
        self.parent.deiconify()  # show parent
        self.destroy()  # close and destroy this screen


