import tkinter as tk
from tkinter import font, ttk
import datetime


class TerminalApp(tk.Frame):
    """
    A more advanced terminal emulator for our simulated HomeOS,
    with a Linux-like feel and improved functionality.
    """

    def __init__(self, master, on_close, username, launch_app_callback):
        """
        Initializes the terminal frame.

        Args:
            master (tk.Tk): The parent widget.
            on_close (callable): A function to call when the terminal is closed.
            username (str): The logged-in username.
            launch_app_callback (callable): A function to call to launch other applications.
        """
        # Define a consistent color scheme for better aesthetics
        self.bg_color = "#1e1e1e"  # Deep charcoal background
        self.fg_color = "#d4d4d4"  # Light gray text for readability
        self.cursor_color = "#00ff00"  # Classic green cursor
        self.input_fg_color = "#00ff00"  # A very bright green for the user's typing
        self.prompt_fg = "#50fa7b"  # A bright green for the prompt

        super().__init__(master, bg=self.bg_color)
        self.on_close = on_close
        self.launch_app_callback = launch_app_callback

        self.user = username
        self.hostname = "homeos"

        # Mock file system for the `ls` and `cd` commands.
        self.file_system = {
            "root": {"dirs": ["home", "bin", "etc", "var"], "files": []},
            "home": {"dirs": ["user", "guest"], "files": ["profile.txt"]},
            "bin": {"dirs": [], "files": ["echo", "clear", "ls", "help", "exit", "date", "sysinfo", "mkdir", "touch", "whoami"]},
            "etc": {"dirs": [], "files": ["passwd", "hosts"]},
            "var": {"dirs": [], "files": ["log.txt"]},
            "user": {"dirs": ["documents", "downloads"], "files": ["welcome.txt"]},
            "guest": {"dirs": [], "files": []},
            "documents": {"dirs": [], "files": ["my_document.txt"]},
            "downloads": {"dirs": [], "files": []}
        }
        self.current_directory = "home"
        self.home_directory = "home"
        self.command_history = []
        self.history_index = -1

        # Use a monospace font for a classic terminal look
        self.terminal_font = font.Font(family="Consolas", size=12)

        # Create the main text display area for the terminal output
        self.text_area = tk.Text(
            self,
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.cursor_color,
            font=self.terminal_font,
            state="disabled",
            relief="flat",
            wrap="word",
            padx=10,
            pady=10
        )
        self.text_area.pack(expand=True, fill="both")

        # --- BUG FIX: Bind a mouse click event to always set focus to the input area. ---
        self.text_area.bind('<Button-1>', self._refocus_input)

        # Create a frame for the input area
        self.input_frame = tk.Frame(self, bg=self.bg_color)
        self.input_frame.pack(fill="x", padx=10, pady=(0, 0))

        # A label to act as the persistent command prompt
        self.prompt_label = tk.Label(
            self.input_frame,
            text=self._get_prompt(),
            bg=self.bg_color,
            fg=self.prompt_fg,
            font=self.terminal_font
        )
        self.prompt_label.pack(side="left")

        # Create the input entry field where the user types
        self.input_area = tk.Entry(
            self.input_frame,
            bg=self.bg_color,
            fg=self.input_fg_color,
            font=self.terminal_font,
            insertbackground=self.cursor_color,
            relief="flat",
            borderwidth=0
        )
        self.input_area.pack(side="left", expand=True, fill="x")
        self.input_area.focus_set()

        # Bind the Enter key to the command handler
        self.input_area.bind('<Return>', self.handle_command)
        self.input_area.bind('<Tab>', self._tab_completion)
        self.input_area.bind('<Up>', self._history_up)
        self.input_area.bind('<Down>', self._history_down)

        # Dictionary of command handlers for a clean and scalable approach
        self.commands = {
            "clear": self._cmd_clear,
            "help": self._cmd_help,
            "echo": self._cmd_echo,
            "ls": self._cmd_ls,
            "cd": self._cmd_cd,
            "date": self._cmd_date,
            "sysinfo": self._cmd_sysinfo,
            "mkdir": self._cmd_mkdir,
            "touch": self._cmd_touch,
            "whoami": self._cmd_whoami,
            "pydocs": self._cmd_pydocs,
            "snake": self._cmd_snake,
            "rm": self._cmd_rm,
            "rmdir": self._cmd_rmdir,
            "ping": self._cmd_ping,
            "ifconfig": self._cmd_ifconfig,
            "exit": self._cmd_exit
        }

        # Print a welcome message
        self.print_output(
            f"Welcome to HomeOS Terminal. Type 'help' for a list of commands.")
        self.print_output("")

    def _get_prompt(self):
        """Constructs the bash-style prompt string."""
        path = f"/~{self.current_directory}" if self.current_directory != self.home_directory else "~"
        return f"{self.user}@{self.hostname}:{path}$ "

    def _refocus_input(self, event=None):
        """
        Sets the focus back to the input area.
        Called on mouse click and whenever the terminal is shown.
        """
        self.input_area.focus_set()

    def print_output(self, text):
        """
        Writes text to the terminal display.
        """
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, f"\n{text}")
        self.text_area.see(tk.END)
        self.text_area.config(state="disabled")

    def handle_command(self, event):
        """
        Processes the command entered by the user.
        """
        command_line = self.input_area.get().strip()

        if command_line:
            self.command_history.append(command_line)
            self.history_index = len(self.command_history)

        self.input_area.delete(0, tk.END)

        if not command_line:
            return

        parts = command_line.split()
        command = parts[0]
        args = parts[1:]

        # Display the prompt and the command that was just run
        prompt_text = f"{self.user}@{self.hostname}:/~{self.current_directory}$ {command_line}"
        self.print_output(f"\033[92m{prompt_text}\033[0m")
        self.text_area.tag_config('prompt', foreground=self.prompt_fg)

        # Execute the command using the dictionary-based handler
        handler = self.commands.get(command)
        if handler:
            handler(args)
        else:
            self.print_output(f"bash: {command}: command not found")

        self.print_output("")  # Add a blank line for readability

    # --- New Functionality ---
    def _tab_completion(self, event):
        """
        Handles tab completion for commands and file paths.
        """
        current_text = self.input_area.get()
        if not current_text:
            return

        words = current_text.split()
        if len(words) <= 1:
            # Command completion
            partial_command = words[0] if words else ""
            matches = [
                cmd for cmd in self.commands if cmd.startswith(partial_command)]
            if len(matches) == 1:
                self.input_area.delete(0, tk.END)
                self.input_area.insert(0, matches[0] + " ")
            elif len(matches) > 1:
                self.print_output(" ".join(matches))
        else:
            # File path completion
            partial_path = words[-1]
            path_parts = partial_path.split('/')

            # Simplified path resolution for demonstration
            current_content = self.file_system.get(
                self.current_directory, {"dirs": [], "files": []})
            possible_matches = current_content["dirs"] + \
                current_content["files"]

            matches = [
                item for item in possible_matches if item.startswith(partial_path)]
            if len(matches) == 1:
                self.input_area.delete(
                    len(current_text) - len(partial_path), tk.END)
                self.input_area.insert(tk.END, matches[0])
            elif len(matches) > 1:
                self.print_output(" ".join(matches))
        return "break"  # Prevents Tkinter from inserting a tab character

    def _history_up(self, event):
        """Navigates up in the command history."""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.input_area.delete(0, tk.END)
            self.input_area.insert(0, self.command_history[self.history_index])
        return "break"  # Prevents the cursor from moving

    def _history_down(self, event):
        """Navigates down in the command history."""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_area.delete(0, tk.END)
            self.input_area.insert(0, self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index += 1
            self.input_area.delete(0, tk.END)
        return "break"  # Prevents the cursor from moving

    # --- Command Handler Methods ---

    def _cmd_clear(self, args):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state="disabled")

    def _cmd_help(self, args):
        if not args:
            self.print_output(
                "Available commands:\n"
                "  - help [command] Shows specific help for a command\n"
                "  - clear          Clears the terminal screen\n"
                "  - echo [text]    Prints the text back to the terminal\n"
                "  - ls             Lists the contents of the current directory\n"
                "  - cd [dir]       Changes the current directory\n"
                "  - date           Displays the current date and time\n"
                "  - sysinfo        Displays mock system information\n"
                "  - mkdir [dir]    Creates a new directory\n"
                "  - touch [file]   Creates a new file\n"
                "  - rm [file]      Removes a file\n"
                "  - rmdir [dir]    Removes an empty directory\n"
                "  - whoami         Displays the current username\n"
                "  - pydocs         Launches the Pydocs application\n"
                "  - snake          Launches the Snake game\n"
                "  - ping [ip/host] Simulates a network ping\n"
                "  - ifconfig       Displays mock network configuration\n"
                "  - exit           Closes the terminal application"
            )
        else:
            command = args[0]
            if command == "help":
                self.print_output(
                    "Usage: help [command]\nShows specific information for a given command.")
            elif command == "clear":
                self.print_output(
                    "Usage: clear\nClears all text from the terminal screen.")
            elif command == "echo":
                self.print_output(
                    "Usage: echo [text]\nPrints a line of text to the terminal.")
            elif command == "ls":
                self.print_output(
                    "Usage: ls\nLists files and directories in the current directory.")
            elif command == "cd":
                self.print_output(
                    "Usage: cd [directory]\nChanges the current directory. 'cd ..' moves to the parent directory. 'cd' with no arguments returns to the home directory.")
            elif command == "date":
                self.print_output(
                    "Usage: date\nDisplays the current date and time.")
            elif command == "sysinfo":
                self.print_output(
                    "Usage: sysinfo\nDisplays mock system information about the OS.")
            elif command == "mkdir":
                self.print_output(
                    "Usage: mkdir [directory]\nCreates a new directory with the given name.")
            elif command == "touch":
                self.print_output(
                    "Usage: touch [file]\nCreates a new, empty file with the given name.")
            elif command == "rm":
                self.print_output(
                    "Usage: rm [file]\nRemoves a file. Does not work on directories.")
            elif command == "rmdir":
                self.print_output(
                    "Usage: rmdir [directory]\nRemoves an empty directory.")
            elif command == "whoami":
                self.print_output(
                    "Usage: whoami\nDisplays the name of the current user.")
            elif command == "pydocs":
                self.print_output(
                    "Usage: pydocs\nLaunches the Pydocs word processor application.")
            elif command == "snake":
                self.print_output(
                    "Usage: snake\nLaunches the classic Snake game.")
            elif command == "ping":
                self.print_output(
                    "Usage: ping [ip/host]\nSimulates sending data packets to a network host.")
            elif command == "ifconfig":
                self.print_output(
                    "Usage: ifconfig\nDisplays a mock network configuration for the system.")
            elif command == "exit":
                self.print_output(
                    "Usage: exit\nCloses the terminal application and returns to the desktop.")
            else:
                self.print_output(f"Help: No help topic for '{command}'")

    def _cmd_echo(self, args):
        self.print_output(" ".join(args))

    def _cmd_ls(self, args):
        if self.current_directory in self.file_system:
            dirs = self.file_system[self.current_directory]["dirs"]
            files = self.file_system[self.current_directory]["files"]

            if dirs or files:
                output = " ".join(f"\033[94m{d}\033[0m" for d in sorted(
                    dirs)) + " " + " ".join(sorted(files))
                self.print_output(output)
            else:
                self.print_output("")
        else:
            self.print_output("Error: Directory not found")

    def _cmd_cd(self, args):
        if not args or args[0] == "~":
            self.current_directory = self.home_directory
            self.prompt_label.config(text=self._get_prompt())
            return

        new_dir = args[0]
        current_content = self.file_system.get(
            self.current_directory, {"dirs": []})

        if new_dir in current_content["dirs"]:
            self.current_directory = new_dir
        elif new_dir == "..":
            if self.current_directory != "root":
                parent_found = False
                for parent, content in self.file_system.items():
                    if self.current_directory in content["dirs"]:
                        self.current_directory = parent
                        parent_found = True
                        break
                if not parent_found:
                    self.print_output("Error: Could not find parent directory")
        else:
            self.print_output(f"Error: Directory not found '{new_dir}'")

        self.prompt_label.config(text=self._get_prompt())

    def _cmd_date(self, args):
        now = datetime.datetime.now()
        self.print_output(now.strftime("%A, %B %d, %Y %H:%M:%S"))

    def _cmd_sysinfo(self, args):
        self.print_output("HomeOS (Python Terminal) v1.0.0")
        self.print_output("OS Name: Python-based Simulated Environment")
        self.print_output("Kernel: 5.15.0-76-generic (simulated)")
        self.print_output(
            f"Uptime: {datetime.timedelta(seconds=tk.Tcl().eval('info tclversion'))}")

    def _cmd_mkdir(self, args):
        if not args:
            self.print_output("Error: Please specify a directory name.")
            return

        new_dir_name = args[0]
        if new_dir_name in self.file_system.get(self.current_directory, {"dirs": [], "files": []})["dirs"] or \
           new_dir_name in self.file_system.get(self.current_directory, {"dirs": [], "files": []})["files"]:
            self.print_output(
                f"Error: Directory or file '{new_dir_name}' already exists.")
        else:
            self.file_system[self.current_directory]["dirs"].append(
                new_dir_name)
            self.file_system[new_dir_name] = {"dirs": [], "files": []}
            self.print_output(f"Directory '{new_dir_name}' created.")

    def _cmd_touch(self, args):
        if not args:
            self.print_output("Error: Please specify a file name.")
            return

        new_file_name = args[0]
        if new_file_name in self.file_system.get(self.current_directory, {"dirs": [], "files": []})["dirs"] or \
           new_file_name in self.file_system.get(self.current_directory, {"dirs": [], "files": []})["files"]:
            self.print_output(
                f"Error: File or directory '{new_file_name}' already exists.")
        else:
            self.file_system[self.current_directory]["files"].append(
                new_file_name)
            self.print_output(f"File '{new_file_name}' created.")

    def _cmd_rm(self, args):
        if not args:
            self.print_output("Error: Please specify a file name.")
            return

        file_to_remove = args[0]
        if file_to_remove in self.file_system.get(self.current_directory, {"files": []})["files"]:
            self.file_system[self.current_directory]["files"].remove(
                file_to_remove)
            self.print_output(f"File '{file_to_remove}' removed.")
        else:
            self.print_output(
                f"Error: File '{file_to_remove}' not found or is a directory.")

    def _cmd_rmdir(self, args):
        if not args:
            self.print_output("Error: Please specify a directory name.")
            return

        dir_to_remove = args[0]
        if dir_to_remove in self.file_system.get(self.current_directory, {"dirs": []})["dirs"]:
            if self.file_system.get(dir_to_remove, {"dirs": [], "files": []})["dirs"] or \
               self.file_system.get(dir_to_remove, {"dirs": [], "files": []})["files"]:
                self.print_output(
                    f"Error: Directory '{dir_to_remove}' is not empty.")
            else:
                self.file_system[self.current_directory]["dirs"].remove(
                    dir_to_remove)
                del self.file_system[dir_to_remove]
                self.print_output(f"Directory '{dir_to_remove}' removed.")
        else:
            self.print_output(
                f"Error: Directory '{dir_to_remove}' not found or is a file.")

    def _cmd_whoami(self, args):
        self.print_output(self.user)

    def _cmd_pydocs(self, args):
        self.launch_app_callback("pydocs")

    def _cmd_snake(self, args):
        self.launch_app_callback("snake")

    def _cmd_ping(self, args):
        if not args:
            self.print_output(
                "Usage: ping [ip/host]\nSimulates sending data packets to a network host.")
            return

        host = args[0]
        self.print_output(f"PING {host} ({host}): 56 data bytes")
        for i in range(4):
            self.print_output(
                f"64 bytes from {host}: icmp_seq={i+1} ttl=64 time={random.randint(10, 50)} ms")

    def _cmd_ifconfig(self, args):
        self.print_output(
            "eth0: flags=209<UP,BROADCAST,MULTICAST>  mtu 1500\n"
            "        inet 192.168.1.10  netmask 255.255.255.0  broadcast 192.168.1.255\n"
            "        ether 00:11:22:33:44:55  txqueuelen 1000  (Ethernet)\n"
            "lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536\n"
            "        inet 127.0.0.1  netmask 255.0.0.0\n"
        )

    def _cmd_exit(self, args):
        self.on_close()
