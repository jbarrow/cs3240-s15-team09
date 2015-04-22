# GUI for SecureWitness Desktop Application
from tkinter import *
import tkinter.messagebox as tm
from client import authenticate, get_reports, download_files, get

url = "http://secure-witness-9.herokuapp.com/"
token = ""

class SecureWitnessGUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Stack all of our frames on top of each other using a
        # tkFrame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginFrame, ReportsFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)

    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()

class LoginFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)

        self.user_label = Label(self, text="Username")
        self.pass_label = Label(self, text="Password")

        self.user_field = Entry(self)
        self.pass_field = Entry(self, show="*")

        self.user_label.grid(row=0, sticky=E)
        self.pass_label.grid(row=1, sticky=E)
        self.user_field.grid(row=0, column=1)
        self.pass_field.grid(row=1, column=1)

        self.submit = Button(self, text="Login", command = lambda: self._login(controller))
        self.submit.grid(columnspan=2)

        self.pack()

    def _login(self, controller):
        username = self.user_field.get()
        password = self.pass_field.get()

        if username == "" or password == "":
            tm.showerror("Login Error", "You must enter a username and password.")
        else:
            try:
                token = authenticate(username, password)
                tm.showinfo("Congrats!", "Logged in!")
            except:
                tm.showerror("Login Error", "Username and password don't match")

        controller.show_frame(ReportsFrame)

class ReportsFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)

        self.pack()

class ReportFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)

        self.pack()

app = SecureWitnessGUI()
app.mainloop()
