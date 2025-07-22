import tkinter as tk
from tkinter import messagebox
from core.utils import create_account


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

        success, msg = create_account(username, pw1, pw2, self.app.accounts_file)
        if success:
            messagebox.showinfo("Success", msg)
            self.app.show_login()
        else:
            messagebox.showerror("Error", msg)
