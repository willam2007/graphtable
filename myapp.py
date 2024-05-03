import tkinter as tk
from tkinter import messagebox

class AuthWindow:
    def __init__(self, root):
        self.root = root
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
        if username == "admin" and password == "1234":
            messagebox.showinfo("Login", "Successful!")
            self.root.destroy()
            MainWindow(tk.Tk())
        else:
            messagebox.showerror("Error", "Invalid username or password")

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("GraphTable")
        self.root.geometry("800x300")

        # во втором комите

if __name__ == "__main__":
    root = tk.Tk()
    auth = AuthWindow(root)
    root.mainloop()
