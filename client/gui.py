# GUI for SecureWitness Desktop Application
from tkinter import *
import tkinter.messagebox as tm
from client import authenticate, get_reports, download_files, get

url = "http://localhost:8000/"
token, username = "", ""
reports = []

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
        for F in (LoginFrame, ReportsFrame, ReportFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)

    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()

    def set_credentials(self, username, token):
        self.username = username
        self.token = token

    def render_reports(self, reports):
        frame = self.frames[ReportsFrame]
        frame._render_reports(reports)

    def render_report(self, report):
        frame = self.frames[ReportFrame]
        frame._render_report(report, self.username, self.token)

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
        logged_in = False

        if username == "" or password == "":
            tm.showerror("Login Error", "You must enter a username and password.")
        else:
            try:
                token = authenticate(username, password)
                #tm.showinfo("Congrats!", "Logged in!")
                controller.set_credentials(username, token)
                logged_in = True
            except:
                tm.showerror("Login Error", "Username and password don't match")

        if logged_in:
            reports = get_reports(username, token)
            controller.render_reports(reports)
            controller.show_frame(ReportsFrame)


class ReportsFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.list = Listbox(self, selectmode=SINGLE)
        self.list.grid(row=0, pady=10)

        self.view = Button(self, text="View Selected Report", command = lambda: self._render_report(controller))
        self.view.grid(row=1)

        self.current = None

        #self.pack()

    def _render_reports(self, reports):
        self.reports = reports
        for i, report in enumerate(reports):
            self.list.insert(END, str(i+1) + ". " + report['fields']['short_description'])

    def _render_report(self, controller):
        title = self.list.get(self.list.curselection())
        i = int(title[0])
        report = self.reports[i-1]
        controller.render_report(report)
        controller.show_frame(ReportFrame)

class ReportFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)

        self.title_var = StringVar()
        self.desc_var = StringVar()
        self.loc_var = StringVar()

        self.title_var.set('')
        self.desc_var.set('')
        self.loc_var.set('')

        self.title = Label(self, textvariable=self.title_var, wraplength=200)
        self.title.grid(row=0, columnspan=2)

        self.desc = Label(self, textvariable=self.desc_var, wraplength=200)
        self.desc.grid(row=1, columnspan=2)

        self.loc = Label(self, textvariable=self.loc_var, wraplength=200)
        self.loc.grid(row=2, columnspan=2)

        self.back = Button(self, text="Back to Reports", command = lambda: controller.show_frame(ReportsFrame))
        self.back.grid(row=3, column=0)

        self.download = Button(self, text="Download All Files")
        self.download.grid(row=3, column=1)
        #self.pack()

    def _render_report(self, report, username, token):
        self.title_var.set(report['fields']['short_description'])
        self.desc_var.set(report['fields']['detailed_description'])
        self.loc_var.set("Location: " + report['fields']['location'])

        self.download.configure(command = lambda: download_files(username, token, report['pk']))

        self.report = report

app = SecureWitnessGUI()
app.mainloop()
