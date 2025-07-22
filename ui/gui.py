import tkinter as tk
from tkinter import ttk
from ui.panels.panel_main import MainPanel
from ui.panels.panel_settings import SettingsPanel
from core.utils import bootcheck

class TickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticker")
        self.root.geometry("640x480")
        self.root.minsize(640, 480)
        self.root.configure(bg="white")

        bootcheck()
        self._create_notebook()

    def _create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.main_panel = MainPanel(self.notebook)
        self.settings_panel = SettingsPanel(self.notebook)
        self.notebook.add(self.main_panel, text="Main")
        self.notebook.add(self.settings_panel, text="Settings")
        self.notebook.pack(fill="both", expand=True)

def launch_gui():
    root = tk.Tk()
    app = TickerApp(root)
    root.mainloop()