# HomeOS

A simple, Python-based simulated operating system created with the Tkinter library. This project serves as a fun and educational demonstration of application management, user interfaces, and basic command-line functionality within a single Python environment.

## Features

- **Login and Account Creation:** A functional login screen allows users to create a new account or log in with a pre-defined user.
- **Modern Desktop UI:** A clean, modern desktop with draggable icons and a dynamic taskbar.
- **Simulated Terminal:** A Linux-like terminal with a realistic prompt, tab completion, command history, and a variety of simulated commands (`ls`, `cd`, `mkdir`, `touch`, `ping`, etc.).
- **Pydocs Word Processor:** A simple word processor that supports basic text formatting (bold and italic) and file operations (open, save, save as).
- **Snake Game:** A classic Snake game with a high score leaderboard.
- **Simulated Web Browser:** A basic browser that fetches and displays the raw HTML content of a URL.

## Getting Started

To run this project, you will need to have Python installed on your system.

### 1. Clone the Repository

First, clone this repository to your local machine using Git:
git clone https://github.com/nbs12215/HomeOS.git

 ### 2. Install Dependencies
This project requires the `requests` library. You can install it using `pip`, the Python package installer, with the following command:
pip install requests

### 3. Run the Application

The application's entry point is the `login.py` file. To start the HomeOS, run the following command in your terminal:
python login.py

### User Accounts and Data Persistence

- The application comes with a default user:
  - **Username:** `admin`
  - **Password:** `password123`
- You can create new accounts from the login screen.
- **Important Note:** All user accounts and their data (including high scores and files created in the terminal) are stored in your computer's RAM. This means that any new accounts or changes you make will be deleted when you close the program.

### Application Details

- **Pydocs:** The word processor allows you to save and open `.txt` files.
- **Snake Game:** Your high scores are saved to a `highscores.txt` file in the project directory, so they will be saved when the program is closed.
- **Web Browser:** The browser is a simulated tool. It fetches and displays the plain text HTML of a website, but it cannot render the full page with CSS, JavaScript, or images.

## Project Structure

- `login.py`: The entry point for the application, handling login and user account creation.
- `home.py`: The main HomeOS application, managing the desktop, taskbar, and all other applications.
- `terminal.py`: The code for the simulated terminal.
- `pydocs.py`: The code for the Pydocs word processor.
- `snake.py`: The code for the classic Snake game.
- `browser.py`: The code for the simulated web browser.

Feel free to explore the code, modify it, and add your own applications!



