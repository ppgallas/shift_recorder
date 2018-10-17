import tkinter as tk
from tkinter import messagebox as ms
import sqlite3
import sys


with sqlite3.connect('quit.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL, password TEXT NOT NULL);')
db.commit()
db.close()



class Main:
    def __init__(self, master):
        # Window
        self.master = master
        # Some Usefull variables
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.n_username = tk.StringVar()
        self.n_password = tk.StringVar()
        # Create Widgets
        self.widgets()

    # Login Function
    def login(self):
        # Establish Connection
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        # Find user If there is any take proper action
        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user, [(self.username.get()), (self.password.get())])
        result = c.fetchall()
        if result:
            self.logf.pack_forget()
            self.head['text'] = self.username.get() + '\n Loged In'
            self.head['pady'] = 150
        else:
            ms.showerror('Oops!', 'Username Not Found.')

    def new_user(self):
        # Establish Connection
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        # Find Existing username if any take proper action
        find_user = ('SELECT * FROM user WHERE username = ?')
        c.execute(find_user, [(self.username.get())])
        if c.fetchall():
            ms.showerror('Error!', 'Username Taken Try a Diffrent One.')
        else:
            ms.showinfo('Success!', 'Account Created!')
            self.log()
        # Create New Account
        insert = 'INSERT INTO user(username,password) VALUES(?,?)'
        c.execute(insert, [(self.n_username.get()), (self.n_password.get())])
        db.commit()



    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
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
        tk.Label(self.crf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky='W')
        tk.Entry(self.crf, textvariable=self.n_password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        tk.Button(self.crf, text='Create Account', bd=3, font=('', 15), padx=5, pady=5, command=self.new_user).grid()
        tk.Button(self.crf, text='Go to Login', bd=3, font=('', 15), padx=5, pady=5, command=self.log).grid(row=2,
                                                                                                         column=1)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Login Form')
    Main(root)
    root.mainloop()