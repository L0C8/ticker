import tkinter as tk
from tkinter import ttk
from pathlib import Path

# runtime utils
from core.utils import bootcheck

# ui panels 
from ui.panels.panel_main import MainPanel
from ui.panels.panel_settings import SettingsPanel
from ui.panels.panel_login import LoginPanel
from ui.panels.panel_create import CreatePanel

class TickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticker")
        self.root.geometry("640x480")
        self.root.minsize(640, 480)
        self.root.configure(bg="white")

        bootcheck()
        self.base_dir = Path(__file__).resolve().parent.parent
        self.accounts_file = self.base_dir / "data" / "accounts.ini"

        self.container = tk.Frame(self.root, bg="white")
        self.container.pack(fill="both", expand=True)

        self.show_login()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_container()
        panel = LoginPanel(self.container, self)
        panel.pack(fill="both", expand=True)

    def show_create(self):
        self.clear_container()
        panel = CreatePanel(self.container, self)
        panel.pack(fill="both", expand=True)

    def show_main(self):
        self.clear_container()
        notebook = ttk.Notebook(self.container)
        main_panel = MainPanel(notebook)
        settings_panel = SettingsPanel(notebook)
        notebook.add(main_panel, text="Main")
        notebook.add(settings_panel, text="Settings")
        notebook.pack(fill="both", expand=True)

def launch_gui():
    root = tk.Tk()
    app = TickerApp(root)
    root.mainloop()