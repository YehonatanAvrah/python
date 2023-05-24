import socket
import threading
import tkinter
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter.messagebox import showerror
from RegistrySC import Register
from MenuSC import Menu

SIZE = 8


class MainWindow(tkinter.Tk):  # create a window
    def __init__(self):
        super().__init__()
        self.title('Snakes and Ladders')
        self.geometry("1000x500")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas = Canvas(width=1000, height=500, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.resizable(width=False, height=False)
        # self.Frame = Frame(self, bg='#80c1ff')
        # self.Frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold", size=15)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handle_thread_socket()
        self.format = 'utf-8'

        # ====================Logo and Icon======================
        self.icon = PhotoImage(file="../Photos/SAL_icon.png")
        self.iconphoto(True, self.icon)
        self.logo_photo = Image.open('../Photos/SAL_Logo.png')
        self.logo = ImageTk.PhotoImage(self.logo_photo)
        self.canvas.create_image(350, 75, image=self.logo, anchor=NW)

        # self.img = Image.open('../Photos/Anya.jpg')
        # self.resize = self.img.resize((650, 650), Image.Resampling.LANCZOS)
        # self.bg = ImageTk.PhotoImage(self.resize)
        # self.imgLabel = Label(self, image=self.bg)
        # self.imgLabel.pack(expand=YES)

        # ====================Labels & Entries======================
        self.Email = StringVar()
        self.EmailLbl = Label(self, text="Email: ", width=10, font=self.LblFont, bg='#AC94F4')  # place a label on the window
        self.EmailLbl.place(x=100, y=25)
        self.EntEmail = Entry(self, textvariable=self.Email, border=0, font=self.LblFont)
        self.EntEmail.place(x=225, y=25)  # x=100, y=25
        # self.EntEmail.insert(0, "Email")
        # self.EntEmail.bind('<FocusIn>', self.email_enter)
        # self.EntEmail.bind('<FocusOut>', self.email_leave)

        self.Password = StringVar()
        self.PasswordLbl = Label(self, text="Password: ", width=10, font=self.LblFont, bg='#AC94F4')
        self.PasswordLbl.place(x=100, y=75)
        self.EntPass = Entry(self, show='●', textvariable=self.Password, font=self.LblFont)
        self.EntPass.place(x=210, y=75)

        self.ShowIcon = Image.open('../photos/Show.png')
        self.ShowIconResize = self.ShowIcon.resize((27, 28), Image.Resampling.LANCZOS)
        self.ShowEye = ImageTk.PhotoImage(self.ShowIconResize)
        self.HideIcon = Image.open('../photos/Hide.png')
        self.HideIconResize = self.HideIcon.resize((27, 28), Image.Resampling.LANCZOS)
        self.HideEye = ImageTk.PhotoImage(self.HideIconResize)
        self.ShowHidePass = Button(self, image=self.ShowEye, command=self.toggle_pswrd, font=self.LblFont)
        self.ShowHidePass.place(x=460, y=75)

        self.UserData = StringVar()
        self.UserData.set("Please Login To Enter The Game")
        self.UserDataLbl = Label(self, textvariable=self.UserData, font=self.LblFont, bg='#AC94F4', fg="red")
        self.UserDataLbl.place(x=100, y=125)

        self.NoAcc = Label(self, text="Don't have an account? Sign Up!", font=self.LblFont, fg="blue", bg='#AC94F4')
        self.NoAcc.place(x=100, y=275)

        # ====================Buttons======================
        self.btn_submit = Button(self, text="Sign In", command=self.login, width=10, background="lime", font=self.LblFont)
        self.btn_submit.place(x=100, y=175)
        # self.btn_clear = Button(self, text="Clear", command=self.clear, width=10, background="red", font=self.LblFont)
        # self.btn_clear.place(x=250, y=175)
        self.btn_register = Button(self, text='Sign Up', command=self.open_register, width=10, background="cyan",
                                   font=self.LblFont)
        self.btn_register.place(x=170, y=325)

    def clear(self):
        self.EntEmail.delete(0, END)
        self.EntPass.delete(0, END)

    def on_closing(self):
        if messagebox.askokcancel("Quit Game", "Do you want to quit?"):
            self.send_msg("exit", self.client_socket)
            self.destroy()

    def email_enter(self, event):
        self.EntEmail.delete(0, END)

    def email_leave(self, event):
        current_mail = self.EntEmail.get()
        if current_mail == '':
            self.EntEmail.insert(0, "Email")

    def open_register(self):
        window = Register(self)
        window.grab_set()
        self.withdraw()

    def open_menu(self, username):
        window = Menu(self, username)
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
            if data is not None and data != "Err_NotExist" and data != "Please send data according to protocol":
                self.UserData.set("Logged in successfully, Welcome back")
                self.EntPass.delete(0, END)
                self.open_menu(data)
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
        data = self.recv_msg(self.client_socket)
        # data = self.client_socket.recv(1024).decode()
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
        #try:
        length = client_socket.recv(SIZE).decode(self.format)
        if not length:
            print("NO LENGTH!")
            return None
        print("The length is " + length)  # error: The length is 00000007The length is Bondman
        data = b""
        remaining = int(length)
        while remaining > 0:
            chunk = client_socket.recv(remaining)
            if not chunk:
                print("NO DATA!")
                return None
            data += chunk
            remaining -= len(chunk)
        print("The data is: " + str(data))
        if ret_type == "string":
            data = data.decode(self.format)
        print(data)
        return data
        #except:
            #print("Error with receiving msg")


if __name__ == "__main__":
    M = MainWindow()
    try:
        M.mainloop()  # keep the window displaying
    except KeyboardInterrupt:
        pass
