import json
from pathlib import Path
import tkinter as tk


class HelpPanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="white")
        self.app = app
        base_dir = Path(__file__).resolve().parent.parent.parent
        data_file = base_dir / "data" / "help.json"
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                self.help_data = json.load(f)
        except Exception:
            self.help_data = {}

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.listbox = tk.Listbox(container, exportselection=False)
        self.listbox.pack(side="left", fill="y")
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        self.text = tk.Text(container, state="disabled", wrap="word")
        self.text.pack(side="left", fill="both", expand=True, padx=(10, 0))

        for category in self.help_data.keys():
            self.listbox.insert(tk.END, category)

        if self.help_data:
            self.listbox.select_set(0)
            self._display_content(next(iter(self.help_data)))

    def _on_select(self, event=None):
        if not self.listbox.curselection():
            return
        idx = self.listbox.curselection()[0]
        category = self.listbox.get(idx)
        self._display_content(category)

    def _display_content(self, category: str):
        content = self.help_data.get(category, "")
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, content)
        self.text.configure(state="disabled")
