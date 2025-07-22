import tkinter as tk
from tkinter import messagebox
import configparser


class CreatePanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="white")
        self.app = app

        tk.Label(self, text="New Username", bg="white").pack(pady=(20, 5))
        self.username_var = tk.StringVar()
        tk.Entry(self, textvariable=self.username_var).pack()

        tk.Label(self, text="Password", bg="white").pack(pady=(10, 5))
        self.password_var = tk.StringVar()
        tk.Entry(self, textvariable=self.password_var, show="*").pack()

        tk.Label(self, text="Confirm Password", bg="white").pack(pady=(10, 5))
        self.confirm_var = tk.StringVar()
        tk.Entry(self, textvariable=self.confirm_var, show="*").pack()

        tk.Button(self, text="Create", command=self._create_account).pack(pady=10)
        tk.Button(self, text="Back", command=self.app.show_login).pack()

    def _create_account(self):
        username = self.username_var.get().strip()
        pw1 = self.password_var.get().strip()
        pw2 = self.confirm_var.get().strip()
        if not username or not pw1:
            messagebox.showerror("Error", "Username and password required")
            return
        if pw1 != pw2:
            messagebox.showerror("Error", "Passwords do not match")
            return
        config = configparser.ConfigParser()
        config.read(self.app.accounts_file)
        if config.has_option("users", username):
            messagebox.showerror("Error", "Username already exists")
            return
        if "users" not in config:
            config["users"] = {}
        config["users"][username] = pw1
        with open(self.app.accounts_file, "w", encoding="utf-8") as f:
            config.write(f)
        messagebox.showinfo("Success", "Account created")
        self.app.show_login()