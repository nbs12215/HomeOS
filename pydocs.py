import tkinter as tk
from tkinter import messagebox, filedialog, font, colorchooser, ttk


class PydocsApp(tk.Frame):
    """
    A simple Microsoft Word-like text editor application.
    Features a menubar, toolbar, and main text area with scrollbars.
    """

    def __init__(self, master, on_close, change_desktop_color_callback):
        super().__init__(master)
        self.on_close = on_close
        self.change_desktop_color_callback = change_desktop_color_callback
        self.current_file = None

        # --- Main Frame and Widgets ---
        self.main_frame = tk.Frame(self, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True)

        # Main Text Editing Area
        self.text_area_frame = tk.Frame(self.main_frame)
        self.text_area_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar for the text area
        self.scrollbar = tk.Scrollbar(self.text_area_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(
            self.text_area_frame,
            wrap="word",  # Wraps text at word boundaries
            font=("Arial", 12),
            undo=True,
            yscrollcommand=self.scrollbar.set
        )
        self.text_area.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.text_area.yview)

        # --- Menubar ---
        self.menubar = tk.Menu(self.master.winfo_toplevel())
        self.master.winfo_toplevel().config(menu=self.menubar)

        # File Menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open...", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(
            label="Save As...", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_close)

        # Edit Menu (Placeholders for future functionality)
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(
            label="Undo", command=self.text_area.edit_undo)
        self.edit_menu.add_command(
            label="Redo", command=self.text_area.edit_redo)

        # Settings Menu
        self.settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(
            label="Background Color", command=self.change_background_color)

        # --- Toolbar with Formatting Buttons ---
        self.toolbar = tk.Frame(
            self.main_frame, bg="#e0e0e0", relief="flat", bd=1)
        self.toolbar.pack(fill="x", padx=10, pady=(0, 5))

        # Font Selection Combobox
        self.font_families = sorted(font.families())
        self.font_selection = ttk.Combobox(
            self.toolbar, values=self.font_families, state="readonly", width=15)
        self.font_selection.set("Arial")
        self.font_selection.bind(
            "<<ComboboxSelected>>", self.change_font_family)
        self.font_selection.pack(side="left", padx=5)

        # Bold button
        self.bold_button = tk.Button(
            self.toolbar,
            text="B",
            font=("Arial", 10, "bold"),
            command=self.apply_bold,
            relief="raised",
            padx=5,
            pady=2
        )
        self.bold_button.pack(side="left", padx=2)

        # Italic button
        self.italic_button = tk.Button(
            self.toolbar,
            text="I",
            font=("Arial", 10, "italic"),
            command=self.apply_italic,
            relief="raised",
            padx=5,
            pady=2
        )
        self.italic_button.pack(side="left", padx=2)

        # Initial font setup
        self.text_area.tag_configure("bold", font=(
            self.font_selection.get(), 12, "bold"))
        self.text_area.tag_configure("italic", font=(
            self.font_selection.get(), 12, "italic"))

    # --- File Operations ---

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.current_file = None
        self.master.winfo_toplevel().title("Pydocs - Untitled")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", file.read())
                self.current_file = file_path
                self.master.winfo_toplevel().title(f"Pydocs - {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w") as file:
                    file.write(self.text_area.get("1.0", tk.END))
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get("1.0", tk.END))
                self.current_file = file_path
                self.master.winfo_toplevel().title(f"Pydocs - {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    # --- Formatting Functions ---
    def apply_bold(self):
        try:
            current_tags = self.text_area.tag_names("sel.first")
            if "bold" in current_tags:
                self.text_area.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text_area.tag_add("bold", "sel.first", "sel.last")
        except tk.TclError:
            pass  # No text selected

    def apply_italic(self):
        try:
            current_tags = self.text_area.tag_names("sel.first")
            if "italic" in current_tags:
                self.text_area.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text_area.tag_add("italic", "sel.first", "sel.last")
        except tk.TclError:
            pass  # No text selected

    def change_font_family(self, event):
        new_font_family = self.font_selection.get()
        current_font = font.Font(self.text_area, self.text_area.cget("font"))
        current_font.configure(family=new_font_family)
        self.text_area.config(font=current_font)

        # Update bold and italic tags to use the new font family
        self.text_area.tag_configure("bold", font=(
            new_font_family, current_font.cget("size"), "bold"))
        self.text_area.tag_configure("italic", font=(
            new_font_family, current_font.cget("size"), "italic"))

    def change_background_color(self):
        """Opens a color picker and changes the background color of the desktop."""
        color_code = colorchooser.askcolor(
            title="Choose a new desktop color")[1]
        if color_code:
            self.change_desktop_color_callback(color_code)


if __name__ == '__main__':
    # This block is for testing PydocsApp as a standalone application
    root = tk.Tk()

    def close_app():
        root.destroy()
    app = PydocsApp(root, on_close=close_app,
                    change_desktop_color_callback=lambda c: root.config(bg=c))
    app.pack(fill="both", expand=True)
    root.mainloop()
