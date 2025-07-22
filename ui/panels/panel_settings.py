import tkinter as tk
from tkinter import messagebox
import json
from core.cipher import AESCipherPass

class SettingsPanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="white")
        self.app = app

        tk.Label(self, text="Finnhub API Key", bg="white").pack(pady=(20, 5))
        self.api_var = tk.StringVar()

        try:
            with open(self.app.accounts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}

        users = data.get("users", {})
        user_data = users.get(self.app.current_user_enc, {})
        enc_key = user_data.get("finnhub", "")
        key_plain = ""
        if enc_key and self.app.current_password:
            try:
                key_plain = AESCipherPass.decrypt(enc_key, self.app.current_password)
            except Exception:
                key_plain = ""
        self.api_var.set(key_plain)

        tk.Entry(self, textvariable=self.api_var).pack(fill="x", padx=10)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Cancel", command=self._cancel).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save", command=self._save).pack(side="left", padx=5)

    def _save(self):
        key = self.api_var.get().strip()
        try:
            with open(self.app.accounts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}

        users = data.get("users", {})
        user_data = users.get(self.app.current_user_enc, {})
        enc_key = ""
        if key:
            enc_key = AESCipherPass.encrypt(key, self.app.current_password or "")
        user_data["finnhub"] = enc_key
        users[self.app.current_user_enc] = user_data
        data["users"] = users
        with open(self.app.accounts_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Saved", "Settings saved")
        self.app.show_main()

    def _cancel(self):
        self.app.show_main()
