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
        self.geometry("1200x500")
        self.title('Registration')
        self.format = 'utf-8'
        self.resizable(width=False, height=False)

        # ====================BG and Icon======================
        # self.icon = PhotoImage(file="../Photos/SAL_icon.png")
        # self.iconphoto(False, self.icon)
        self.canvas = Canvas(self, width=1200, height=500, bg='#AC94F4')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.LblFont = font.Font(family='Comic Sans MS', weight="bold")
        self.img = Image.open("../Photos/Anya_Security.jpg")
        self.resize = self.img.resize((175, 175), Image.Resampling.LANCZOS)
        self.secure_img = ImageTk.PhotoImage(self.resize)
        self.canvas.create_image(750, 180, image=self.secure_img, anchor=NW)

        self.create_gui()

    def create_gui(self):
        # ====================Labels & Entries======================
        self.canvas.create_oval(930, 230, 1130, 370, fill="white", outline="black", width=5)
        self.canvas.create_text(950, 300, text="Your Information\n Is Secured :)", font=self.LblFont, anchor=W)

        self.canvas.create_text(150, 30, text="Email:", font=self.LblFont, anchor=W)
        self.EntEmail = Entry(self, font=self.LblFont)
        self.canvas.create_window(400, 30, window=self.EntEmail)

        self.canvas.create_text(150, 80, text="Password:", font=self.LblFont, anchor=W)
        self.EntPass = Entry(self, show='●', font=self.LblFont)
        self.canvas.create_window(400, 80, window=self.EntPass)

        self.canvas.create_text(150, 130, text="Confirm Password:", font=self.LblFont, anchor=W)
        self.EntConfirmPass = Entry(self, show='●', font=self.LblFont)
        self.canvas.create_window(400, 130, window=self.EntConfirmPass)

        self.canvas.create_text(150, 180, text="Username:", font=self.LblFont, anchor=W)
        self.EntUsername = Entry(self, font=self.LblFont)
        self.canvas.create_window(400, 180, window=self.EntUsername)

        self.SucReg = StringVar()
        self.SucReg.set("Please Enter Information To Register")
        self.SucRegLbl = Label(self, textvariable=self.SucReg, font=self.LblFont, background="yellow", width=40,
                               height=5)
        self.canvas.create_window(850, 90, window=self.SucRegLbl)

        # ====================Buttons======================
        self.button_reg = Button(self, text="Register", command=self.handle_add_user, font=self.LblFont, background="green")
        self.canvas.create_window(200, 250, window=self.button_reg)

        self.btn_close = Button(self, text="Previous Window", command=self.close, background="red", font=self.LblFont)
        self.canvas.create_window(350, 250, window=self.btn_close)

        self.ShowIcon = Image.open('../photos/Show.png')
        self.ShowIconResize = self.ShowIcon.resize((27, 28), Image.Resampling.LANCZOS)
        self.ShowEye = ImageTk.PhotoImage(self.ShowIconResize)
        self.HideIcon = Image.open('../photos/Hide.png')
        self.HideIconResize = self.HideIcon.resize((27, 28), Image.Resampling.LANCZOS)
        self.HideEye = ImageTk.PhotoImage(self.HideIconResize)
        self.ShowHidePass = Button(self, image=self.ShowEye, command=self.toggle_pswrd, font=self.LblFont)
        self.canvas.create_window(535, 80, window=self.ShowHidePass)

        self.ShowHideConfirmPass = Button(self, image=self.ShowEye, command=self.toggle_confirm_pswrd, font=self.LblFont)
        self.canvas.create_window(535, 130, window=self.ShowHideConfirmPass)

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

    def toggle_confirm_pswrd(self):
        try:
            if self.EntConfirmPass.cget('show') == '':
                self.EntConfirmPass.config(show='●')
                self.ShowHideConfirmPass.config(image=self.ShowEye)
            else:
                self.EntConfirmPass.config(show='')
                self.ShowHideConfirmPass.config(image=self.HideEye)
        except:
            print("failed to show/hide")
            return False

    def handle_add_user(self):
        email = self.EntEmail.get()
        username = self.EntUsername.get()
        password = self.EntPass.get()
        confirm_password = self.EntConfirmPass.get()

        if not email or not username or not password or not confirm_password:
            self.SucReg.set("Please enter all the required information")
        elif len(username) > 9:
            self.SucReg.set("Username length must be less than or equal to 9 characters")
        elif password != confirm_password:
            self.SucReg.set("Passwords do not match")
        else:
            self.client_handler = threading.Thread(target=self.register_user, args=())
            self.client_handler.daemon = True
            self.client_handler.start()

    def register_user(self):
        try:
            print("register")
            arr = ["register", self.EntEmail.get(), self.EntUsername.get(), self.EntPass.get()]
            str_insert = ",".join(arr)
            print(str_insert)
            self.parent.send_msg(str_insert, self.parent.client_socket, "encrypted")
            data = self.parent.recv_msg(self.parent.client_socket)
            if data == "Successfully registered!":
                self.SucReg.set(data)
                self.EntEmail.delete(0, END)
                self.EntPass.delete(0, END)
                self.EntConfirmPass.delete(0, END)
                self.EntUsername.delete(0, END)
            else:
                self.SucReg.set(data)
            print(data)
        except:
            self.SucReg.set("Failed Register")

    def close(self):
        self.parent.deiconify()
        self.destroy()
