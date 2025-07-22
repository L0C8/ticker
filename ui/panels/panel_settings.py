import tkinter as tk

class SettingsPanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="white")
        self.app = app
        tk.Label(self, text="Settings", bg="white").pack(pady=(20, 10))
        tk.Button(self, text="Back", command=self._back).pack()

    def _back(self):
        self.app.show_main()
