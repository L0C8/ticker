import tkinter as tk
import threading
from core.services import get_ticker_data

class MainPanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="white")
        self.app = app
        
        search_frame = tk.Frame(self, bg="white")
        search_frame.pack(fill="x", anchor="nw", padx=10, pady=10)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<Return>", self._on_search)

        self.search_button = tk.Button(search_frame, text="Search", command=self._on_search)
        self.search_button.pack(side="left", padx=(5, 0))

        self.save_button = tk.Button(search_frame, text="Save", command=self._save_text, state="disabled")
        self.save_button.pack(side="left", padx=(5, 0))

        self.output_text = tk.Text(self, state="disabled", wrap="word")
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.search_thread = None
        self.loading = False
        self.dot_count = 0

    def _on_search(self, event=None):
        if self.search_thread and self.search_thread.is_alive():
            return

        query = self.search_var.get().strip()
        if not query:
            self.save_button.configure(state="disabled")
            return

        tickers = [t.strip() for t in query.replace(",", " ").split() if t.strip()]
        self.search_button.configure(state="disabled")
        self.save_button.configure(state="disabled")

        self.loading = True
        self.dot_count = 0
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self._animate_loading()

        self.search_thread = threading.Thread(
            target=self._perform_search, args=(tickers,), daemon=True
        )
        self.search_thread.start()

    def _perform_search(self, tickers: list[str]):
        results = []
        for idx, ticker in enumerate(tickers):
            data = get_ticker_data(ticker)
            lines = []
            if isinstance(data, dict):
                if "error" in data:
                    lines.append(data["error"])
                else:
                    for key, val in data.items():
                        if isinstance(val, dict):
                            lines.append(f"{key}:")
                            for k2, v2 in val.items():
                                lines.append(f"  {k2}: {v2}")
                        else:
                            lines.append(f"{key}: {val}")
            if idx < len(tickers) - 1:
                lines.append("-" * 40)
            results.append("\n".join(lines))

        final_text = "\n".join(results)
        self.after(0, lambda: self._display_result(final_text))

    def _display_result(self, text: str):
        self.loading = False
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state="disabled")
        if text.strip():
            self.save_button.configure(state="normal")
        self.search_button.configure(state="normal")

    def _animate_loading(self):
        if not self.loading:
            return
        dots = "." * (self.dot_count % 4)
        text = "Loading" + dots
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state="disabled")
        self.dot_count = (self.dot_count + 1) % 4
        self.after(500, self._animate_loading)

    def _save_text(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if not text:
            return
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)

