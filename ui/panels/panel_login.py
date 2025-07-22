import tkinter as tk
from tkinter import messagebox
import configparser
import json
from pathlib import Path
from core.cipher import AESCipherPass, hash_text


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
        if not username or not password:
            messagebox.showerror("Login Failed", "Invalid username or password")
            return

        try:
            with open(self.app.accounts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}

        users = data.get("users", {})
        hashed_input = hash_text(password)

        for enc_user, info in users.items():
            try:
                dec_user = AESCipherPass.decrypt(enc_user, "default")
            except Exception:
                continue
            if dec_user == username:
                stored_enc = info.get("password", "")
                try:
                    stored_hash = AESCipherPass.decrypt(stored_enc, password)
                except Exception:
                    break
                if stored_hash == hashed_input:
                    self.app.show_main()
                    return
                break

        messagebox.showerror("Login Failed", "Invalid username or password")