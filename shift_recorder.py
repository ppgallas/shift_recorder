import tkinter as tk
from tkinter import messagebox as ms
import xlsxwriter as xwr
import sqlite3 as lite
import hashlib as hsh
import datetime


def encrypt_password(password):
    return hsh.sha1(password.encode('UTF-8')).hexdigest()


class MainWindow:

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

        try:
            conn1 = lite.connect('shifts.db')
            c1 = conn1.cursor()
            name_select = '''SELECT * FROM shifts WHERE name = ? AND surname = ?;'''
            db_to_xls = c1.execute(name_select, [self.name.get(), self.surname.get()])

            # Create an new Excel file and add a worksheet
            wb = xwr.Workbook('moje_zmiany.xlsx')
            ws = wb.add_worksheet()

            # Add a bold format to use to highlight cells
            bold = wb.add_format({'bold': True})

            # write some text with formatting in bold for columns
            ws.write('A1', 'Imię', bold)
            ws.write('B1', 'Nazwisko', bold)
            ws.write('C1', 'Data', bold)

            # Write the content of db to xlsx worksheet
            for i, row in enumerate(db_to_xls):
                for j, value in enumerate(row):
                    ws.write(i + 1, j, value)

            # close the handler
            wb.close()

        except lite.Error as e:
            conn1.rollback()
            print("An error occurred : ", e.args[0])
        finally:
            conn1.close()

    # TODO every time after generating - drop table before next month
    def register_day(self):

        date = str(datetime.date.today())

        try:
            conn2 = lite.connect('shifts.db')
            c2 = conn2.cursor()
            c2.execute('''CREATE TABLE IF NOT EXISTS shifts (name TEXT, surname TEXT, date TEXT,
                            FOREIGN KEY (name) REFERENCES user(name),
                            FOREIGN KEY (surname) REFERENCES user(surname));''')
            saving_date = '''INSERT INTO shifts (name, surname, date) VALUES (?, ?, ?)'''
            c2.execute(saving_date, [self.name.get(), self.surname.get(), date])
            conn2.commit()
            c2.close()
        except lite.Error as e:
            conn2.rollback()
            print("An error occured :", e.args[0])
        finally:
            conn2.close()

        self.generate_report()

        ms.showinfo('Zapis zmiany', 'Data zapisana')
        self.master.destroy()

    # Login Function
    def client_login(self):

        try:
            # Establish Connection
            conn3 = lite.connect('shifts.db')
            c3 = conn3.cursor()

            # Find user If there is any take proper action
            find_user = 'SELECT * FROM user WHERE username = ? and password = ?'
            c3.execute(find_user, [self.username.get(), encrypt_password(self.password.get())])
            result = c3.fetchall()

            if result:
                self.name.set(result[0][1])
                self.surname.set(result[0][2])
                [x.destroy() for x in self.master.slaves()]
                label1 = tk.Label(self.master.geometry('250x125'), text='Is your shift today ' + self.username.get()+'?')
                ok_button = tk.Button(self.master, text='OK', command=self.register_day)
                label1.pack(), ok_button.pack()
            else:
                ms.showerror('Oops!', 'Username not found.')
        except lite.Error as e:
            conn3.rollback()
            print("An error occurred : ", e.args[0])
        finally:
            conn3.close()

    def add_new_user(self):
        try:
            # Establish Connection
            conn4 = lite.connect('shifts.db')
            c4 = conn4.cursor()

            # Find Existing username if any take proper action
            find_user = '''SELECT DISTINCT username, name, surname FROM user WHERE username = ? and name = ? 
                            and surname = ? '''
            c4.execute(find_user, [self.n_username.get(), self.name.get(), self.surname.get()])
            if c4.fetchall():
                ms.showerror('Error!', 'Username taken try a different one, please.')
            else:
                ms.showinfo('Success!', 'Account created!')
                self.log()

                # defined a function for encrypting password
                conn4.create_function('encrypt', 1, encrypt_password)

                # Create New Account
                insert = '''INSERT INTO user (username, name, surname, password) VALUES(?, ?, ?, encrypt(?))'''
                c4.execute(insert, [self.n_username.get(), self.name.get(), self.surname.get(), self.n_password.get()])
                conn4.commit()
        except lite.Error as e:
            conn4.rollback()
            print("An error occurred : ", e.args[0])
        finally:
            conn4.close()

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
        tk.Button(self.logf, text=' Login ', bd=3, font=('', 15), padx=5, pady=5, command=self.client_login).grid()
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
        tk.Button(self.crf, text='Create Account', bd=3, font=('', 15), padx=5, pady=5,
                  command=self.add_new_user).grid(row=4, column=1)
        tk.Button(self.crf, text='Back', bd=3, font=('', 15), padx=5, pady=5, command=self.log).grid(row=4,
                                                                                                            column=0)


if __name__ == '__main__':

    try:
        conn0 = lite.connect('shifts.db')
        c0 = conn0.cursor()

        # CHANGE USERNAME FOR PRIMARY KEY
        c0.execute('''CREATE TABLE IF NOT EXISTS user(username TEXT NOT NULL, name TEXT NOT NULL, surname TEXT NOT NULL, 
                            password TEXT NOT NULL, employee_id INTEGER PRIMARY KEY);''')
        conn0.commit()
    except lite.Error as e:
        conn0.rollback()
        print("An error occurred : ", e.args[0])
    finally:
        conn0.close()

    mycolor = '#%02x%02x%02x' % (0, 173, 239)

    root = tk.Tk()
    root.title('Login form - Shift recorder')
    MainWindow(root)
    root.mainloop()
