import tkinter as tk
from tkinter import messagebox as ms
from xlsxwriter.workbook import Workbook
import sqlite3
import datetime

with sqlite3.connect('shifts.db') as db:
    c = db.cursor()

#CHANGE USERNAME FOR PRIMARY KEY
c.execute("CREATE TABLE IF NOT EXISTS user(username TEXT NOT NULL, name TEXT NOT NULL, surname TEXT NOT NULL, password TEXT NOT NULL, employee_id INTEGER PRIMARY KEY);")
db.commit()
db.close()


mycolor = '#%02x%02x%02x' % (0, 173, 239)


class Main:

    def __init__(self, master):
        # Window
        self.master = master
        # Some useful variables
        self.username = tk.StringVar()
        self.name = tk.StringVar()
        self.surname = tk.StringVar()
        self.password = tk.StringVar()
        self.n_username = tk.StringVar()
        self.n_password = tk.StringVar()
        # Create Widgets
        self.widgets()

    def generate_report(self):

        with sqlite3.connect('shifts.db') as db:
            c = db.cursor()
        name_select = ("SELECT * FROM shifts WHERE name = ? AND surname = ?;")
        db_to_xls = c.execute(name_select, [(self.name.get()), (self.surname.get())])

        wb = Workbook('moje_zmiany.xlsx')
        ws = wb.add_worksheet()
        bold = wb.add_format({'bold':True})
        ws.write('A1', 'Imię', bold)
        ws.write('B1', 'Nazwisko', bold)
        ws.write('C1', 'Data', bold)

        for i, row in enumerate(db_to_xls):
            for j, value in enumerate(row):
                ws.write(i+1, j, value)

        wb.close()

        # TODO every time after generating - drop table before next month

    def register_day(self):

        date = str(datetime.date.today())

        with sqlite3.connect('shifts.db') as db:
            c = db.cursor()

            c.execute("""CREATE TABLE IF NOT EXISTS shifts
            (name TEXT,
            surname TEXT,
            date TEXT,
            FOREIGN KEY (name) REFERENCES user(name),
            FOREIGN KEY (surname) REFERENCES user(surname));""")


            saving_date = ("""INSERT INTO shifts (name, surname, date) VALUES (?, ?, ?)""")
            c.execute(saving_date, ((self.name.get()), (self.surname.get()), date))

        db.commit()
        c.close()
        db.close()
        self.generate_report()

        ms.showinfo('Zapis zmiany', 'Data zapisana')
        self.master.destroy()

    # Login Function
    def login(self):
        # Establish Connection
        with sqlite3.connect('my.db') as db:
            c = db.cursor()

        # Find user If there is any take proper action
        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user, [(self.username.get()), (self.password.get())])
        result = c.fetchall()
        if result:
            self.name.set(result[0][1])
            self.surname.set(result[0][2])
            [x.destroy() for x in self.master.slaves()]
            temp1 = tk.Label(self.master.geometry('250x125'), text='Czy dziś jest twoja zmiana ' + self.username.get() + '?')
            temp2 = tk.Button(self.master, text='OK', command= self.register_day)
            temp1.pack(), temp2.pack()
        else:
            ms.showerror('Oops!', 'Username Not Found.')

    def new_user(self):
        # Establish Connection
        with sqlite3.connect('shifts.db') as db:
            c = db.cursor()

        # Find Existing username if any take proper action
        find_user = ("SELECT DISTINCT username, name, surname FROM user WHERE username = ? and name = ? and surname = ? ")
        c.execute(find_user, [(self.n_username.get()), (self.name.get()), (self.surname.get())])
        if c.fetchall():
            ms.showerror('Error!', 'Username Taken Try a Diffrent One.')
        else:
            ms.showinfo('Success!', 'Account Created!')
            self.log()
        # Create New Account
            insert = ("INSERT INTO user (username, name, surname, password) VALUES(?, ?, ?, ?)")
            c.execute(insert, [(self.n_username.get()), (self.name.get()), (self.surname.get()), (self.n_password.get())])
            db.commit()

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
        self.name.set('')
        self.surname.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()

    # Draw Widgets
    def widgets(self):
        self.head = tk.Label(self.master, text='LOGIN', font=('', 35), pady=10)
        self.head.pack()
        self.logf = tk.Frame(self.master, padx=10, pady=10)
        tk.Label(self.logf, text='Username: ', font=('', 20), pady=5, padx=5).grid(sticky='W')
        tk.Entry(self.logf, textvariable=self.username, bd=5, font=('', 15)).grid(row=0, column=1)
        tk.Label(self.logf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky='W')
        tk.Entry(self.logf, textvariable=self.password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        tk.Button(self.logf, text=' Login ', bd=3, font=('', 15), padx=5, pady=5, command=self.login).grid()
        tk.Button(self.logf, text=' Create Account ', bd=3, font=('', 15), padx=5, pady=5, command=self.cr).grid(row=2,
                                                                                                              column=1)
        self.logf.pack()

        self.crf = tk.Frame(self.master, padx=10, pady=10)
        tk.Label(self.crf, text='Username: ', font=('', 20), pady=5, padx=5).grid(sticky='W')
        tk.Entry(self.crf, textvariable=self.n_username, bd=5, font=('', 15)).grid(row=0, column=1)
        tk.Label(self.crf, text='Name: ', font=('', 20), pady=5, padx=5).grid(sticky='W')
        tk.Entry(self.crf, textvariable=self.name, bd=5, font=('', 15)).grid(row=1, column=1)
        tk.Label(self.crf, text='Surname: ', font=('', 20), pady=5, padx=5).grid(sticky='W')
        tk.Entry(self.crf, textvariable=self.surname, bd=5, font=('', 15)).grid(row=2, column=1)
        tk.Label(self.crf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky='W')
        tk.Entry(self.crf, textvariable=self.n_password, bd=5, font=('', 15), show='*').grid(row=3, column=1)
        tk.Button(self.crf, text='Create Account', bd=3, font=('', 15), padx=5, pady=5, command=self.new_user).grid()
        tk.Button(self.crf, text='Go to Login', bd=3, font=('', 15), padx=5, pady=5, command=self.log).grid(row=4,
                                                                                                         column=1)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Login Form')
    Main(root)
    root.mainloop()

