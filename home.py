import tkinter as tk
from tkinter import messagebox
from terminal import TerminalApp
from pydocs import PydocsApp
from snake import SnakeGame
from browser import BrowserApp


class Desktop(tk.Frame):
    """
    The main desktop area where application icons would reside.
    """

    def __init__(self, master, launch_app_callback, username):
        super().__init__(master, bg="#212121")  # Dark background
        self.launch_app_callback = launch_app_callback
        self.username = username

        # A frame to hold desktop icons
        self.icons_frame = tk.Frame(self, bg="#212121")
        self.icons_frame.pack(fill="both", expand=True)

        # Desktop icon for Terminal
        self.terminal_icon = self._create_icon(
            self.icons_frame,
            "Terminal",
            "",  # Unicode for terminal icon
            lambda: self.launch_app_callback("terminal")
        )
        self.terminal_icon.place(x=20, y=20)

        # Desktop icon for Pydocs
        self.pydocs_icon = self._create_icon(
            self.icons_frame,
            "Pydocs",
            "✎",  # A new Unicode character for a better icon
            lambda: self.launch_app_callback("pydocs")
        )
        self.pydocs_icon.place(x=20, y=100)

        # Desktop icon for Snake Game
        self.snake_icon = self._create_icon(
            self.icons_frame,
            "Snake",
            "",  # Unicode for a game controller
            lambda: self.launch_app_callback("snake")
        )
        self.snake_icon.place(x=20, y=180)

        # Desktop icon for Web Browser
        self.browser_icon = self._create_icon(
            self.icons_frame,
            "Browser",
            "🌐",  # A new Unicode character for a better browser icon
            lambda: self.launch_app_callback("browser")
        )
        self.browser_icon.place(x=20, y=260)

    def _create_icon(self, parent, text, icon_char, command):
        """Helper method to create a button that looks like a desktop icon."""
        frame = tk.Frame(parent, bg="#212121")  # Dark background
        icon_font = "FontAwesome" if "FontAwesome" in tk.font.families() else "Arial"

        icon_label = tk.Label(
            frame,
            text=icon_char,
            font=(icon_font, 36),
            fg="#90caf9",  # Light blue accent color
            bg="#212121",
            cursor="hand2"
        )
        icon_label.pack()
        label = tk.Label(frame, text=text, fg="#ffffff",
                         bg="#212121", font=("Helvetica", 10))
        label.pack()

        # Make the icon clickable and draggable
        frame.icon_command = command
        frame.bind("<Button-1>", self._start_drag)
        frame.bind("<B1-Motion>", self._drag_motion)
        frame.bind("<ButtonRelease-1>", self._stop_drag)
        icon_label.bind("<Button-1>", self._start_drag)
        icon_label.bind("<B1-Motion>", self._drag_motion)
        icon_label.bind("<ButtonRelease-1>", self._stop_drag)
        label.bind("<Button-1>", self._start_drag)
        label.bind("<B1-Motion>", self._drag_motion)
        label.bind("<ButtonRelease-1>", self._stop_drag)

        return frame

    def _start_drag(self, event):
        # Set a flag to check if the user is dragging
        event.widget.master.drag_start_x = event.x
        event.widget.master.drag_start_y = event.y
        event.widget.master.is_dragging = False

    def _drag_motion(self, event):
        # Check if the drag distance is significant enough to be a drag
        frame = event.widget.master
        if abs(event.x - frame.drag_start_x) > 5 or abs(event.y - frame.drag_start_y) > 5:
            frame.is_dragging = True
            x, y = frame.winfo_x(), frame.winfo_y()
            frame.place(x=x + event.x - frame.drag_start_x,
                        y=y + event.y - frame.drag_start_y)

    def _stop_drag(self, event):
        frame = event.widget.master
        if not frame.is_dragging:
            # If not dragging, execute the command
            frame.icon_command()
        frame.is_dragging = False


class Taskbar(tk.Frame):
    """
    The persistent taskbar at the bottom of the screen.
    It now includes a start button and dynamic app buttons.
    """

    def __init__(self, master, start_menu_callback):
        super().__init__(master, bg="#212121", height=40)  # Dark background
        self.pack_propagate(False)
        self.buttons = {}
        self.start_menu_callback = start_menu_callback

        # Start button
        self.start_button = tk.Button(
            self,
            text="Start",
            command=start_menu_callback,
            font=("Helvetica", 12, "bold"),
            bg="#424242",  # Darker accent
            fg="#ffffff",
            activebackground="#616161",
            activeforeground="#ffffff",
            relief="raised",
            cursor="hand2"
        ).pack(side="left", padx=10, pady=5)

    def add_app_button(self, app_name, command):
        """Adds a new button to the taskbar for an open application."""
        if app_name not in self.buttons:
            button = tk.Button(
                self,
                text=app_name,
                command=command,
                font=("Helvetica", 12),
                bg="#424242",
                fg="#ffffff",
                activebackground="#616161",
                activeforeground="#ffffff",
                relief="raised",
                cursor="hand2"
            )
            button.pack(side="left", padx=5, pady=5)
            self.buttons[app_name] = button

    def remove_app_button(self, app_name):
        """Removes an app button from the taskbar."""
        if app_name in self.buttons:
            self.buttons[app_name].destroy()
            del self.buttons[app_name]


class HomeOS(tk.Tk):
    """
    The main application class that manages the different screens.
    """

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"HomeOS - Logged in as {self.username}")
        self.geometry("1024x768")
        self.configure(bg="#212121")  # Dark background

        self.apps = {}
        self.current_frame = None

        # Create the main content area and taskbar
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.taskbar = Taskbar(self, self.show_start_menu)
        self.taskbar.pack(side="bottom", fill="x")

        # Create all frames/screens
        self.desktop_screen = Desktop(
            self.container, self.show_app, self.username)
        self.start_menu_frame = tk.Frame(
            self.container, bg="#303030", width=200)  # Slightly lighter dark gray
        self.start_menu_frame.pack_propagate(False)

        # Initialize applications but don't display them yet
        self.terminal_app = TerminalApp(self.container, lambda: self.close_app(
            "terminal"), self.username, self.show_app)
        self.pydocs_app = PydocsApp(self.container, lambda: self.close_app(
            "pydocs"), self.change_desktop_color)
        self.snake_app = SnakeGame(
            self.container, lambda: self.close_app("snake"))
        self.browser_app = BrowserApp(
            self.container, lambda: self.close_app("browser"))

        # A dictionary to hold all available apps for easier management
        self.available_apps = {
            "terminal": self.terminal_app,
            "pydocs": self.pydocs_app,
            "snake": self.snake_app,
            "browser": self.browser_app
        }

        # Initially, show the desktop screen
        self.desktop_screen.pack(fill="both", expand=True)
        self.current_frame = self.desktop_screen
        self.taskbar.pack(side="bottom", fill="x")

        self.bind('<Escape>', self.quit_app)

    def change_desktop_color(self, color_code):
        """Changes the background color of the desktop and container frames."""
        self.desktop_screen.config(bg=color_code)
        self.container.config(bg=color_code)

    def show_desktop(self):
        """Displays the main desktop, called from the taskbar."""
        if self.current_frame:
            self.current_frame.pack_forget()
        self.desktop_screen.pack(fill="both", expand=True)
        self.current_frame = self.desktop_screen
        self.taskbar.pack(side="bottom", fill="x")

    def show_start_menu(self):
        """Toggles the start menu on and off."""
        if self.start_menu_frame.winfo_ismapped():
            self.start_menu_frame.pack_forget()
        else:
            self.start_menu_frame.pack(side="left", fill="y", anchor="sw")
            self._populate_start_menu()

    def _populate_start_menu(self):
        """
        Creates buttons in the start menu for each available application.
        This is a simple version, for more apps you might want to use a loop.
        """
        for widget in self.start_menu_frame.winfo_children():
            widget.destroy()

        # Terminal app button
        tk.Button(
            self.start_menu_frame,
            text="Terminal",
            command=lambda: self.show_app("terminal"),
            font=("Helvetica", 12),
            bg="#424242",
            fg="#ffffff",
            activebackground="#616161",
            activeforeground="#ffffff",
            relief="flat"
        ).pack(fill="x", padx=5, pady=2)

        # Pydocs app button
        tk.Button(
            self.start_menu_frame,
            text="Pydocs",
            command=lambda: self.show_app("pydocs"),
            font=("Helvetica", 12),
            bg="#424242",
            fg="#ffffff",
            activebackground="#616161",
            activeforeground="#ffffff",
            relief="flat"
        ).pack(fill="x", padx=5, pady=2)

        # Snake game button
        tk.Button(
            self.start_menu_frame,
            text="Snake",
            command=lambda: self.show_app("snake"),
            font=("Helvetica", 12),
            bg="#424242",
            fg="#ffffff",
            activebackground="#616161",
            activeforeground="#ffffff",
            relief="flat"
        ).pack(fill="x", padx=5, pady=2)

        # Browser app button
        tk.Button(
            self.start_menu_frame,
            text="Browser",
            command=lambda: self.show_app("browser"),
            font=("Helvetica", 12),
            bg="#424242",
            fg="#ffffff",
            activebackground="#616161",
            activeforeground="#ffffff",
            relief="flat"
        ).pack(fill="x", padx=5, pady=2)

    def show_app(self, app_name):
        """Switches the view to the specified application."""
        self.start_menu_frame.pack_forget()  # Close the start menu if open
        if self.current_frame:
            self.current_frame.pack_forget()

        app_frame = self.available_apps.get(app_name)

        if app_frame:
            app_frame.pack(fill="both", expand=True)
            self.current_frame = app_frame
            if app_name == "terminal":
                self.terminal_app._refocus_input()
            self.taskbar.add_app_button(
                app_name, lambda: self.show_app(app_name))

    def close_app(self, app_name):
        """Closes an application and returns to the desktop."""
        app_frame = self.available_apps.get(app_name)
        if app_frame:
            app_frame.pack_forget()
            self.taskbar.remove_app_button(app_name)
        self.show_desktop()

    def quit_app(self, event=None):
        """Method to quit the application."""
        self.destroy()


if __name__ == "__main__":
    # This block is no longer needed since login.py will launch HomeOS
    # However, for testing purposes, you could launch with a default user:
    # app = HomeOS(username="test_user")
    # app.mainloop()
    pass
