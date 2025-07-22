import tkinter as tk
from tkinter import messagebox
import configparser
from pathlib import Path


class LoginPanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="white")
        self.app = app

        tk.Label(self, text="Username", bg="white").pack(pady=(20, 5))
        self.username_var = tk.StringVar()
        tk.Entry(self, textvariable=self.username_var).pack()

        tk.Label(self, text="Password", bg="white").pack(pady=(10, 5))
        self.password_var = tk.StringVar()
        tk.Entry(self, textvariable=self.password_var, show="*").pack()

        tk.Button(self, text="Login", command=self._login).pack(pady=10)
        tk.Button(self, text="Create Account", command=self.app.show_create).pack()

    def _login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        config = configparser.ConfigParser()
        config.read(self.app.accounts_file)
        if config.has_option("users", username) and config["users"][username] == password:
            self.app.show_main()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")