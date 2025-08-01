import tkinter as tk
from tkinter import messagebox
import hashlib
from home import HomeOS


class LoginApp(tk.Tk):
    """
    Main application window for the login and account creation screens.
    """

    def __init__(self):
        super().__init__()
        self.title("HomeOS Login")
        self.geometry("400x500")
        self.configure(bg="#2c3e50")

        # In-memory user database to store credentials
        self.user_database = {}

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.login_screen = LoginScreen(
            self.container, self.show_create_account, self.on_login_success, self.user_database)
        self.create_account_screen = CreateAccountScreen(
            self.container, self.show_login_screen, self.user_database)

        self.login_screen.pack(fill="both", expand=True)

    def show_login_screen(self):
        """Displays the login screen and hides the create account screen."""
        self.create_account_screen.pack_forget()
        self.login_screen.pack(fill="both", expand=True)
        self.login_screen.username_entry.focus_set()

    def show_create_account(self):
        """Displays the create account screen and hides the login screen."""
        self.login_screen.pack_forget()
        self.create_account_screen.pack(fill="both", expand=True)
        self.create_account_screen.username_entry.focus_set()

    def on_login_success(self, username):
        """Called upon successful login to close this window and launch the OS."""
        self.destroy()
        # Launch the main HomeOS application with the logged-in username
        home_app = HomeOS(username=username)
        home_app.title(f"HomeOS - Logged in as {username}")
        home_app.mainloop()


class LoginScreen(tk.Frame):
    """
    Login screen with username and password fields.
    """

    def __init__(self, master, show_create_account_callback, on_login_success_callback, user_database):
        super().__init__(master, bg="#2c3e50")
        self.show_create_account_callback = show_create_account_callback
        self.on_login_success_callback = on_login_success_callback
        self.user_database = user_database

        self.login_frame = tk.Frame(
            self, bg="#34495e", padx=40, pady=40, borderwidth=2, relief="groove")
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(self.login_frame, text="HomeOS Login", font=(
            "Helvetica", 24, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=(0, 20))
        tk.Label(self.login_frame, text="Username:",
                 fg="#ecf0f1", bg="#34495e").pack(pady=5)
        self.username_entry = tk.Entry(
            self.login_frame, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)
        # Default user for quick testing
        self.username_entry.insert(0, "admin")

        tk.Label(self.login_frame, text="Password:",
                 fg="#ecf0f1", bg="#34495e").pack(pady=5)
        self.password_entry = tk.Entry(
            self.login_frame, show="*", font=("Helvetica", 12))
        self.password_entry.pack(pady=5)
        # Default password for quick testing
        self.password_entry.insert(0, "password123")

        self.message_label = tk.Label(
            self.login_frame, text="", fg="#e74c3c", bg="#34495e")
        self.message_label.pack(pady=(5, 10))

        tk.Button(self.login_frame, text="Login", command=self.check_login, font=("Helvetica", 12, "bold"), bg="#27ae60",
                  fg="#ffffff", activebackground="#2ecc71", activeforeground="#ffffff", relief="raised", cursor="hand2").pack(pady=(10, 5))
        tk.Button(self.login_frame, text="Create Account", command=self.show_create_account_callback, font=("Helvetica", 10),
                  bg="#3498db", fg="#ffffff", activebackground="#2980b9", activeforeground="#ffffff", relief="flat", cursor="hand2").pack()

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.message_label.config(
                text="Please enter a username and password.")
            return

        if username in self.user_database:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if self.user_database[username] == hashed_password:
                self.on_login_success_callback(username)
            else:
                self.message_label.config(text="Invalid username or password.")
        else:
            self.message_label.config(text="Invalid username or password.")


class CreateAccountScreen(tk.Frame):
    """
    Screen for creating a new user account.
    """

    def __init__(self, master, show_login_screen_callback, user_database):
        super().__init__(master, bg="#2c3e50")
        self.show_login_screen_callback = show_login_screen_callback
        self.user_database = user_database

        self.create_frame = tk.Frame(
            self, bg="#34495e", padx=40, pady=40, borderwidth=2, relief="groove")
        self.create_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(self.create_frame, text="Create New Account", font=(
            "Helvetica", 20, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=(0, 10))
        tk.Label(self.create_frame, text="Username:",
                 fg="#ecf0f1", bg="#34495e").pack(pady=5)
        self.username_entry = tk.Entry(
            self.create_frame, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.create_frame, text="Password (min 8 chars):",
                 fg="#ecf0f1", bg="#34495e").pack(pady=5)
        self.password_entry = tk.Entry(
            self.create_frame, show="*", font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        self.message_label = tk.Label(
            self.create_frame, text="", fg="#e74c3c", bg="#34495e")
        self.message_label.pack(pady=(5, 10))

        tk.Button(self.create_frame, text="Create Account", command=self.create_account, font=("Helvetica", 12, "bold"), bg="#27ae60",
                  fg="#ffffff", activebackground="#2ecc71", activeforeground="#ffffff", relief="raised", cursor="hand2").pack(pady=(10, 5))
        tk.Button(self.create_frame, text="Back to Login", command=self.show_login_screen_callback, font=("Helvetica", 10),
                  bg="#3498db", fg="#ffffff", activebackground="#2980b9", activeforeground="#ffffff", relief="flat", cursor="hand2").pack()

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.message_label.config(text="Please fill in all fields.")
            return

        if len(password) < 8:
            self.message_label.config(
                text="Password must be at least 8 characters long.")
            return

        if username in self.user_database:
            self.message_label.config(text="Username already exists.")
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.user_database[username] = hashed_password
            messagebox.showinfo(
                "Success", "Account created successfully! Please log in.")
            self.show_login_screen_callback()


if __name__ == "__main__":
    app = LoginApp()
    # Pre-populate a test user for convenience
    test_user_hash = hashlib.sha256("password123".encode()).hexdigest()
    app.user_database["admin"] = test_user_hash
    app.mainloop()
