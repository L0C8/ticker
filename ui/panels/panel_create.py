import tkinter as tk
from tkinter import messagebox
import json

from core.cipher import AESCipherPass, hash_text


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
        try:
            with open(self.app.accounts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}

        users = data.get("users", {})
        for enc_user in users.keys():
            try:
                dec_user = AESCipherPass.decrypt(enc_user, "default")
            except Exception:
                continue
            if dec_user == username:
                messagebox.showerror("Error", "Username already exists")
                return

        enc_user = AESCipherPass.encrypt(username, "default")
        ciphered_pw = AESCipherPass.encrypt(pw1, "default")
        hashed_pw = hash_text(ciphered_pw)
        enc_pw = AESCipherPass.encrypt(hashed_pw, pw1)
        users[enc_user] = {"password": enc_pw, "finnhub": ""}
        data["users"] = users

        with open(self.app.accounts_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Success", "Account created")
        self.app.show_login()