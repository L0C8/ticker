import tkinter as tk

class MainPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        
        search_frame = tk.Frame(self, bg="white")
        search_frame.pack(fill="x", anchor="nw", padx=10, pady=10)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<Return>", self._on_search)

        search_button = tk.Button(search_frame, text="Search", command=self._on_search)
        search_button.pack(side="left", padx=(5, 0))

        self.save_button = tk.Button(search_frame, text="Save", command=self._save_text, state="disabled")
        self.save_button.pack(side="left", padx=(5, 0))

        self.output_text = tk.Text(self, state="disabled", wrap="word")
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _on_search(self, event=None):
        query = self.search_var.get().strip()
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        if query:
            self.output_text.insert(tk.END, "temp")
            self.save_button.configure(state="normal")
        else:
            self.save_button.configure(state="disabled")
        self.output_text.configure(state="disabled")

    def _save_text(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if not text:
            return
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)