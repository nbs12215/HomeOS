import tkinter as tk
from tkinter import messagebox
import requests


class BrowserApp(tk.Frame):
    """
    A simple web browser application.
    """

    def __init__(self, master, on_close):
        super().__init__(master, bg="#303030")
        self.on_close = on_close

        # --- UI Elements ---
        self.url_frame = tk.Frame(self, bg="#424242", padx=5, pady=5)
        self.url_frame.pack(fill="x")

        self.url_entry = tk.Entry(
            self.url_frame,
            font=("Helvetica", 12),
            bg="#212121",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.url_entry.pack(side="left", fill="x", expand=True)
        self.url_entry.insert(0, "https://www.google.com")

        self.go_button = tk.Button(
            self.url_frame,
            text="Go",
            command=self.fetch_url,
            font=("Helvetica", 12),
            bg="#27ae60",
            fg="#ffffff"
        )
        self.go_button.pack(side="left", padx=5)

        self.browser_frame = tk.Frame(self, bg="#1e1e1e", padx=10, pady=10)
        self.browser_frame.pack(fill="both", expand=True)

        self.text_display = tk.Text(
            self.browser_frame,
            bg="#1e1e1e",
            fg="#d4d4d4",
            font=("Consolas", 12),
            wrap="word"
        )
        self.text_display.pack(fill="both", expand=True)

        self.exit_button = tk.Button(
            self,
            text="Exit Browser",
            command=self.on_close,
            font=("Helvetica", 12),
            bg="#e74c3c",
            fg="#ffffff",
            relief="raised",
            cursor="hand2"
        )
        self.exit_button.pack(pady=10)

    def fetch_url(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Clear previous content and display new content
            self.text_display.delete("1.0", tk.END)
            self.text_display.insert("1.0", response.text)
        except requests.exceptions.RequestException as e:
            self.text_display.delete("1.0", tk.END)
            self.text_display.insert(
                "1.0", f"Error: Could not retrieve content from {url}\n\n{e}")


if __name__ == '__main__':
    # This block is for testing BrowserApp as a standalone application
    root = tk.Tk()
    root.geometry("800x600")

    def close_app():
        root.destroy()
    app = BrowserApp(root, on_close=close_app)
    app.pack(fill="both", expand=True)
    root.mainloop()
