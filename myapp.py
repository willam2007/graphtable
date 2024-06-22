import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Text
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="127.0.0.1",
                user="Admin",
                password="Willam2003",
                database="auth_db"
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            messagebox.showerror("Датабейз Error", f"Error connecting to MySQL: {e}")

    def __del__(self):
        if self.conn.is_connected():
            self.conn.close()

    def authenticate(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()

class AuthWindow:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Authorization")
        self.root.geometry("300x150")
        
        self.label_username = tk.Label(root, text="Username:")
        self.label_password = tk.Label(root, text="Password:")
        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")
        self.btn_login = tk.Button(root, text="Login", command=self.login)
        
        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.btn_login.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user = self.db.authenticate(username, password)
        if user:
            messagebox.showinfo("Login", "Successful!")
            self.root.destroy()
            MainWindow(tk.Tk())
        else:
            messagebox.showerror("Error", "Invalid username or password")

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Window")
        self.root.geometry("800x600")

        self.label_x = tk.Label(root, text="X (через запятую):")
        self.entry_x = tk.Entry(root)
        self.label_y = tk.Label(root, text="Y (через запятую):")
        self.entry_y = tk.Entry(root)

        self.btn_plot = tk.Button(root, text="Plot", command=self.plot_graph)
        self.btn_plot_table = tk.Button(root, text="Plot from Table", command=self.plot_from_table)
        self.btn_reminder = tk.Button(root, text="Памятка", command=self.show_reminder)
        
        self.label_x.pack()
        self.entry_x.pack()
        self.label_y.pack()
        self.entry_y.pack()
        self.btn_plot.pack()
        self.btn_plot_table.pack()
        self.btn_reminder.pack()

        self.figure = plt.Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
    #Строим график через 'интерфейс' данные
    def plot_graph(self):
        try:
            x_values = list(map(float, self.entry_x.get().split(',')))
            y_values = list(map(float, self.entry_y.get().split(',')))
        except ValueError:
            messagebox.showerror("Error", "Пожалуйста, введите действительные цифры через запятую")
            return
        
        if len(x_values) != len(y_values):
            messagebox.showerror("Error", "Количество значений X и Y должно быть одинаковым")
            return
        
        sorted_pairs = sorted(zip(x_values, y_values))
        x_values, y_values = zip(*sorted_pairs)
        
        self.ax.clear()
        self.ax.plot(x_values, y_values, marker='o')
        self.ax.set_title('Graph')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.canvas.draw()
    #Строим график через таблицу(принцип тот же)
    def plot_from_table(self):
        try:
            df = pd.read_excel('table.xlsx')
            x_values = df['X'].tolist()
            y_values = df['Y'].tolist()
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")
            return
        
        if len(x_values) != len(y_values):
            messagebox.showerror("Error", "Количество значений X и Y должно быть одинаковым")
            return
        
        sorted_pairs = sorted(zip(x_values, y_values))
        x_values, y_values = zip(*sorted_pairs)
        
        self.ax.clear()
        self.ax.plot(x_values, y_values, marker='o')
        self.ax.set_title('Graph')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
    
        self.canvas.draw()
    #Памятка
    def show_reminder(self):
        reminder_window = Toplevel(self.root)
        reminder_window.title("Памятка")
        reminder_window.geometry("300x200")
        
        reminder_text = (
            "Эта программа позволяет строить графики по данным X и Y.\n"
            "1. Введите данные X и Y через запятую в соответствующие поля.\n"
            "2. Нажмите кнопку 'Plot', чтобы построить график по введенным данным.\n"
            "3. Вы можете также использовать кнопку 'Plot from Table', чтобы построить график по данным из файла table.xlsx.\n"
            "4. Убедитесь, что файл table.xlsx находится в корне проекта и содержит столбцы X и Y.\n"
            
        )
        
        text_widget = tk.Text(reminder_window, wrap=tk.WORD, height=10, width=40)
        text_widget.pack(padx=20, pady=20)
        text_widget.insert(tk.END, reminder_text)
        text_widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    db = Database()
    root = tk.Tk()
    auth = AuthWindow(root, db)
    root.mainloop()
