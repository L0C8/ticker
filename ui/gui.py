import tkinter as tk
from ui.panels.panel_main import MainPanel
from core.utils import bootcheck

class TickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticker")
        self.root.geometry("640x480")
        self.root.minsize(640, 480)
        self.root.configure(bg="white")

        bootcheck()
        self._load_main_panel()

    def _load_main_panel(self):
        self.panel = MainPanel(self.root)
        self.panel.pack(fill="both", expand=True)

def launch_gui():
    root = tk.Tk()
    app = TickerApp(root)
    root.mainloop()