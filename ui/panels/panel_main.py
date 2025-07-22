import tkinter as tk

class MainPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        label = tk.Label(self, text="Main", font=("Arial", 18), bg="white")
        label.pack(expand=True)