import tkinter as tk
import random
import os


class SnakeGame(tk.Frame):
    """
    A classic Snake game application built with Tkinter.
    """

    def __init__(self, master, on_close):
        super().__init__(master)
        self.on_close = on_close

        # --- Game Constants ---
        self.WIDTH = 600
        self.HEIGHT = 400
        self.GRID_SIZE = 20
        self.BG_COLOR = "#212121"
        self.SNAKE_COLOR = "#2ecc71"
        self.FOOD_COLOR = "#e74c3c"
        self.SCORE_COLOR = "#ecf0f1"
        self.GAME_OVER_COLOR = "#e74c3c"
        self.MENU_BG = "#303030"
        self.BUTTON_COLOR = "#424242"
        self.BUTTON_FG = "#ffffff"
        self.HIGHSCORE_FILE = "highscores.txt"

        # --- Game State ---
        self.snake = []
        self.direction = "Right"
        self.food_pos = None
        self.score = 0
        self.running = False
        self.highscores = []

        # Load high scores from file
        self._load_highscores()

        # --- UI Elements ---
        self.canvas = tk.Canvas(
            self,
            bg=self.BG_COLOR,
            width=self.WIDTH,
            height=self.HEIGHT,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.menu_frame = tk.Frame(self.canvas, bg=self.MENU_BG)
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create a container for buttons to avoid conflicts with the main canvas
        self.button_frame = tk.Frame(self, bg=self.BG_COLOR)
        self.button_frame.pack(pady=10)

        self.score_label = tk.Label(
            self.button_frame,
            text="Score: 0",
            font=("Helvetica", 16, "bold"),
            bg=self.BG_COLOR,
            fg=self.SCORE_COLOR
        )
        self.score_label.pack(side="left", padx=20)

        self.exit_button = tk.Button(
            self.button_frame,
            text="Exit Game",
            command=self._exit_game_and_close,
            font=("Helvetica", 12),
            bg=self.BUTTON_COLOR,
            fg=self.BUTTON_FG,
            relief="raised",
            cursor="hand2"
        )
        self.exit_button.pack(side="right", padx=20)

        # --- Event Bindings ---
        # The key bindings are now on the frame itself
        self.bind_all("<Left>", self._change_direction)
        self.bind_all("<Right>", self._change_direction)
        self.bind_all("<Up>", self._change_direction)
        self.bind_all("<Down>", self._change_direction)

        self._show_start_menu()

    def _load_highscores(self):
        """Loads high scores from a text file."""
        if os.path.exists(self.HIGHSCORE_FILE):
            with open(self.HIGHSCORE_FILE, "r") as f:
                self.highscores = [int(line.strip()) for line in f.readlines()]
        else:
            self.highscores = [0] * 5  # Initialize with 5 zero scores

    def _save_highscores(self):
        """Saves high scores to a text file."""
        with open(self.HIGHSCORE_FILE, "w") as f:
            for score in self.highscores:
                f.write(str(score) + "\n")

    def _show_start_menu(self):
        """Displays the main menu screen."""
        self.canvas.delete("all")
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome text
        tk.Label(self.menu_frame, text="Snake Game", font=(
            "Helvetica", 24, "bold"), bg=self.MENU_BG, fg=self.SCORE_COLOR).pack(pady=10)

        # High scores leaderboard
        tk.Label(self.menu_frame, text="High Scores", font=(
            "Helvetica", 16, "bold"), bg=self.MENU_BG, fg=self.SCORE_COLOR).pack(pady=(20, 5))
        for i, score in enumerate(sorted(self.highscores, reverse=True)[:5]):
            tk.Label(self.menu_frame, text=f"{i+1}. {score}", font=(
                "Helvetica", 12), bg=self.MENU_BG, fg=self.SCORE_COLOR).pack()

        # Start button
        tk.Button(self.menu_frame, text="Start Game", command=self._start_game, font=("Helvetica", 12,
                  "bold"), bg=self.BUTTON_COLOR, fg=self.BUTTON_FG, relief="raised", cursor="hand2").pack(pady=20)

    def _start_game(self):
        """Resets the game state and starts the game loop."""
        self.menu_frame.place_forget()
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food_pos = self._create_food()
        self.score = 0
        self.running = True
        self.score_label.config(text=f"Score: {self.score}")
        self._game_loop()

    def _create_food(self):
        """Generates a random position for the food."""
        x = random.randint(
            0, (self.WIDTH // self.GRID_SIZE) - 1) * self.GRID_SIZE
        y = random.randint(
            0, (self.HEIGHT // self.GRID_SIZE) - 1) * self.GRID_SIZE
        return (x, y)

    def _change_direction(self, event):
        """Changes the direction of the snake based on key press."""
        if not self.running:
            return

        if event.keysym == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif event.keysym == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym == "Right" and self.direction != "Left":
            self.direction = "Right"

    def _move_snake(self):
        """Moves the snake forward by one grid unit."""
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            new_head = (head_x, head_y - self.GRID_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + self.GRID_SIZE)
        elif self.direction == "Left":
            new_head = (head_x - self.GRID_SIZE, head_y)
        elif self.direction == "Right":
            new_head = (head_x + self.GRID_SIZE, head_y)

        self.snake.insert(0, new_head)

    def _check_collision(self):
        """Checks if the snake has collided with walls or itself."""
        head_x, head_y = self.snake[0]

        # Wall collision
        if (head_x < 0 or head_x >= self.WIDTH or
                head_y < 0 or head_y >= self.HEIGHT):
            return True

        # Self collision
        if self.snake[0] in self.snake[1:]:
            return True

        return False

    def _game_over(self):
        """Displays the game over message and checks for a new high score."""
        self.running = False
        self.canvas.delete("all")

        # Check for new high score
        self.highscores.append(self.score)
        self.highscores.sort(reverse=True)
        self.highscores = self.highscores[:5]  # Keep top 5 scores
        self._save_highscores()

        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(self.menu_frame, text="Game Over", font=(
            "Helvetica", 24, "bold"), bg=self.MENU_BG, fg=self.GAME_OVER_COLOR).pack(pady=10)
        tk.Label(self.menu_frame, text=f"Your Score: {self.score}", font=(
            "Helvetica", 16), bg=self.MENU_BG, fg=self.SCORE_COLOR).pack(pady=5)

        # Display high scores
        tk.Label(self.menu_frame, text="High Scores", font=(
            "Helvetica", 14, "bold"), bg=self.MENU_BG, fg=self.SCORE_COLOR).pack(pady=(10, 5))
        for i, score in enumerate(self.highscores):
            tk.Label(self.menu_frame, text=f"{i+1}. {score}", font=(
                "Helvetica", 12), bg=self.MENU_BG, fg=self.SCORE_COLOR).pack()

        tk.Button(self.menu_frame, text="Play Again", command=self._start_game, font=("Helvetica", 12, "bold"),
                  bg=self.BUTTON_COLOR, fg=self.BUTTON_FG, relief="raised", cursor="hand2").pack(pady=(20, 10))

    def _game_loop(self):
        """The main game loop that updates the game state and display."""
        if not self.running:
            return

        if self._check_collision():
            self._game_over()
            return

        if self.snake[0] == self.food_pos:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.food_pos = self._create_food()
        else:
            self.snake.pop()

        self._move_snake()
        self.canvas.delete("all")

        # Draw snake
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y, x + self.GRID_SIZE, y + self.GRID_SIZE,
                fill=self.SNAKE_COLOR, outline=self.BG_COLOR
            )

        # Draw food
        self.canvas.create_oval(
            self.food_pos[0], self.food_pos[1],
            self.food_pos[0] +
            self.GRID_SIZE, self.food_pos[1] + self.GRID_SIZE,
            fill=self.FOOD_COLOR, outline=self.BG_COLOR
        )

        self.master.after(100, self._game_loop)

    def _exit_game_and_close(self):
        """Stops the game loop and closes the game frame."""
        self.running = False
        self.on_close()


if __name__ == "__main__":
    # This block is for running the game as a standalone app for testing.
    root = tk.Tk()
    root.resizable(False, False)

    def close_game():
        root.destroy()
    game = SnakeGame(root, on_close=close_game)
    game.pack(fill="both", expand=True)
    root.mainloop()
