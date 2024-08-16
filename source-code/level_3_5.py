import tkinter as tk
from tkinter import messagebox
import random
from abstract_classes import AbstractWanderingGame, AbstractGameLauncher

class Player:
    def __init__(self, canvas, color, grid_size, start_position):
        # Creating Private Variables by adding double underscore at the beginning.
        self.__canvas = canvas  # Canvas where the player will be drawn
        self.__color = color    # Color of the player's avatar
        self.__grid_size = grid_size  # Size of the grid (width, height)
        self.__position = start_position  # Starting position of the player (x, y)
        self.__size = 50  # Size of each cell in the grid
        self.__avatar = self.create_avatar()  # Create the player's visual representation on the canvas

    def create_avatar(self):
        # Create an oval on the canvas to represent the player
        x, y = self.__position 
        return self.__canvas.create_oval(
            x * self.__size, y * self.__size,  # Top-left corner
            (x + 1) * self.__size, (y + 1) * self.__size,  # Bottom-right corner
            fill=self.__color,  # Fill color of the oval
            outline="black"  # Border color of the oval
        )

    def get_valid_moves(self):
        # Determine which moves are valid based on the player's position
        x, y = self.__position
        valid_moves = []

        if y > 0:  # Can move up if not on the top edge
            valid_moves.append('up')
        if y < self.__grid_size[1] - 1:  # Can move down if not on the bottom edge
            valid_moves.append('down')
        if x > 0:  # Can move left if not on the left edge
            valid_moves.append('left')
        if x < self.__grid_size[0] - 1:  # Can move right if not on the right edge
            valid_moves.append('right')

        return valid_moves

    def move(self):
        # Move the player in a random valid direction
        valid_moves = self.get_valid_moves()  # Get possible moves
        direction = random.choice(valid_moves)  # Choose a random direction
        x, y = self.__position

        # Update position based on the chosen direction
        if direction == 'up':
            y -= 1
        elif direction == 'down':
            y += 1
        elif direction == 'left':
            x -= 1
        elif direction == 'right':
            x += 1

        self.__position = (x, y)  # Update player's position
        # Update the player's visual representation on the canvas
        self.__canvas.coords(
            self.__avatar,
            x * self.__size, y * self.__size,  # Top-left corner of the updated position
            (x + 1) * self.__size, (y + 1) * self.__size  # Bottom-right corner of the updated position
        )
    
    def get_position(self):
        return self.__position
    
    def get_avatar(self):
        return self.__avatar

class WanderingGame(AbstractWanderingGame):
    def __init__(self, root, grid_size, players):
        self.__root = root  # Main window
        self.__grid_size = grid_size  # Size of the grid (width, height)
        self.__canvas = tk.Canvas(root, width=grid_size[0] * 50, height=grid_size[1] * 50)  # Drawing area
        self.__canvas.pack()
        self.__root.title('Wandering Game')  # Window title

        self.__root.resizable(False, False)  # Prevent resizing

        self.__initial_players = players  # Store initial player info
        self.__merge_count = 0  # Track number of merges
        self.__reset_game()  # Initialize the game
        self.__running = True

        self.__root.after(500, self.run_game)  # Start game loop

    def create_grid(self):
        # Draw grid on the canvas
        for i in range(self.__grid_size[0]):
            for j in range(self.__grid_size[1]):
                self.__canvas.create_rectangle(
                    i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, outline="black"
                )

    def __reset_game(self):
        self.__canvas.delete("all")  # Clear canvas
        self.create_grid()  # Redraw grid
        # Create players
        self.__players = [Player(self.__canvas, color, self.__grid_size, position) for position, color in self.__initial_players]
        self.__move_counts = []  # Initialize move counts list
        self.__total_moves = 0  # Initialize total moves counter

    def __check_if_together(self):
        # Check if all players are in the same position
        positions = [player.get_position() for player in self.__players]
        return len(set(positions)) != len(positions)

    def __update_statistics(self):
        # Add current move count to statistics and reset counter
        self.__move_counts.append(self.__total_moves)
        self.__total_moves = 0

    def show_statistics(self):
        # Calculate statistics
        longest_run = max(self.__move_counts) if self.__move_counts else 0
        shortest_run = min(self.__move_counts) if self.__move_counts else 0
        average_run = sum(self.__move_counts) / len(self.__move_counts) if self.__move_counts else 0

        # Create and show statistics window
        stats_window = tk.Toplevel(self.__root)
        stats_window.title("Game Statistics")

        heading = tk.Label(stats_window, text="Game Statistics", font=("Helvetica", 16, "bold"))
        heading.pack(pady=10)

        stats_text = (
            f"Total Moves: {sum(self.__move_counts)}\n"
            f"Longest Run Without Meeting: {longest_run}\n"
            f"Shortest Run: {shortest_run}\n"
            f"Average Run: {average_run:.2f}"
        )

        stats_label = tk.Label(stats_window, text=stats_text, font=("Helvetica", 14), justify=tk.LEFT)
        stats_label.pack(padx=20, pady=20)

        def on_close():
            # Handle window close event
            self.__stats_window.destroy()
            self.__close_game()

        self.__stats_window = stats_window
        stats_window.protocol("WM_DELETE_WINDOW", on_close)  # Close game when stats window closes

        # Add buttons
        replay_button = tk.Button(stats_window, text="Replay with Same Coordinates", command=self.__replay_game)
        replay_button.pack(pady=10)

        new_game_button = tk.Button(stats_window, text="Start New Game", command=self.__start_new_game)
        new_game_button.pack(pady=10)

        close_button = tk.Button(stats_window, text="Close Application", command=self.__close_application)
        close_button.pack(pady=10)

    def __close_application(self):
        # Close application and stats window if open
        if hasattr(self, 'stats_window') and self.__stats_window is not None:
            self.__stats_window.destroy()
        self.__close_game()

    def __close_game(self):
        self.__running = False  # Stop game loop
        self.__root.destroy()  # Close main window

    def run_game(self):
        if not self.__running:
            return

        # Move all players
        for player in self.__players:
            player.move()
        self.__total_moves += 1  # Increment move counter

        if self.__check_if_together():
            merged_position = None
            new_players = []
            positions = {}
            # Identify merged position and remaining players
            for player in self.__players:
                if player.get_position() in positions:
                    merged_position = player.get_position()
                else:
                    positions[player.get_position()] = player

            for player in self.__players:
                if player.get_position() == merged_position:
                    self.__canvas.delete(player.get_avatar())  # Remove merged player avatar
                else:
                    new_players.append(player)

            # Add new player with merge color
            if merged_position:
                colors = ["purple", "orange", "cyan"]  # Merge colors
                new_color = colors[self.__merge_count] if self.__merge_count < len(colors) else "black"
                new_players.append(Player(self.__canvas, new_color, self.__grid_size, merged_position))
                self.__merge_count += 1

            self.__players = new_players  # Update player list

            self.__update_statistics()  # Update stats

            if len(self.__players) == 1:
                # Game over
                self.__canvas.create_text(
                    self.__grid_size[0] * 25, self.__grid_size[1] * 25,
                    text="Game Over",
                    font=("Helvetica", 20, "bold"),
                    fill="black"
                )
                self.__root.after(500, self.show_statistics)  # Show stats after delay
            else:
                self.__root.after(500, self.run_game)  # Continue game loop
        else:
            self.__root.after(500, self.run_game)  # Continue game loop

    def __replay_game(self):
        self.__close_game()  # Close current game
        game_root = tk.Tk()  # Create new game window
        game_app = WanderingGame(game_root, self.__grid_size, self.__initial_players)
        game_root.mainloop()  # Start new game loop

    def __start_new_game(self):
        self.__close_game()  # Close current game
        new_game_root = tk.Tk()  # Create new start screen window
        new_game_app = StartScreen(new_game_root)
        new_game_root.mainloop()  # Start new game loop


class StartScreen:
    def __init__(self, root):
        self.__root = root
        self.__root.title("3-5 Level")  # Set window title
        self.__root.resizable(False, False)  # Prevent window resizing
        self.__setup_ui()  # Initialize UI components

    def __setup_ui(self):
        self.rows, self.cols, self.num_players = 0, 0, 0  # Initialize variables
        self.coordinates = []  # List to store player coordinates

        # Frame for input fields
        self.input_frame = tk.Frame(self.__root)
        self.input_frame.pack(pady=10)

        # Row input
        self.row_label = tk.Label(self.input_frame, text="Enter Number of Rows:")
        self.row_label.pack(side=tk.LEFT, padx=(10, 5))
        self.rows_entry = tk.Entry(self.input_frame, width=10)
        self.rows_entry.pack(side=tk.LEFT, padx=(0, 15))

        # Column input
        self.col_label = tk.Label(self.input_frame, text="Enter Number of Columns:")
        self.col_label.pack(side=tk.LEFT, padx=(10, 5))
        self.cols_entry = tk.Entry(self.input_frame, width=10)
        self.cols_entry.pack(side=tk.LEFT, padx=(0, 15))

        # Number of players input
        self.__players_label = tk.Label(self.input_frame, text="Enter Number of Players:")
        self.__players_label.pack(side=tk.LEFT, padx=(10, 5))
        self.__players_entry = tk.Entry(self.input_frame, width=10)
        self.__players_entry.pack(side=tk.LEFT, padx=(0, 15))

        # Button to proceed to coordinate entry
        self.start_button = tk.Button(self.__root, text="Next", command=self.__get_coordinates)
        self.start_button.pack(pady=20)
        self.__root.bind('<Return>', lambda event, button=self.start_button: button.invoke())

    def __get_coordinates(self):
        try:
            # Get and validate user inputs
            try:
                self.rows = int(self.rows_entry.get())
            except ValueError:
                raise ValueError("Only Numbers are allowed as an Input for rows.")
            try:
                self.cols = int(self.cols_entry.get())
            except ValueError:
                raise ValueError("Only Numbers are allowed as an Input for columns.")
            try:
                self.num_players = int(self.__players_entry.get())
            except ValueError:
                raise ValueError("Only Numbers are allowed as an Input for number of players.")
            
            if not (2 <= self.num_players <= 4):
                raise ValueError("Number of players must be between 2 and 4.")
            if self.rows < 2 or self.rows > 15:
                raise ValueError("Number of rows in the grid must be at least 2 and at most 15")
            if self.cols < 2 or self.cols > 15:
                raise ValueError("Number of columns in the grid must be at least 2 and must be less than 15.")
            if self.num_players >= self.rows * self.cols:
                raise ValueError("More players than available grid spaces.")

            self.coordinates = []  # Reset coordinates
            self.__root.destroy()  # Close the current window

            # Create new window for player coordinates
            self.coord_window = tk.Tk()
            self.coord_window.resizable(False, False)
            self.coord_window.title("Enter Player Coordinates")

            self.__colors = ["red", "blue", "green", "yellow"]  # Define player colors

            # Create input fields for player coordinates
            for i in range(self.num_players):
                self.__add_coordinate_input(i + 1, self.__colors[i])

            # Button to start the game
            self.finish_button = tk.Button(self.coord_window, text="Start Game", command=self.__start_game)
            self.finish_button.pack(pady=20)
            self.coord_window.mainloop()

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))  # Show error message for invalid inputs

    def __add_coordinate_input(self, player_number, color):
        frame = tk.Frame(self.coord_window)
        frame.pack(pady=10, anchor=tk.W)

        # Input fields for player's coordinates
        label = tk.Label(frame, text=f"Player {player_number} Coordinates (x, y):")
        label.pack(side=tk.LEFT, padx=(10, 5))

        x_entry = tk.Entry(frame, width=5)
        x_entry.pack(side=tk.LEFT, padx=(0, 5))

        y_entry = tk.Entry(frame, width=5)
        y_entry.pack(side=tk.LEFT, padx=(0, 15))

        color_label = tk.Label(frame, text=f"Color: {color}")
        color_label.pack(side=tk.RIGHT, padx=(10, 10))

        self.coordinates.append((x_entry, y_entry, color))  # Store coordinate inputs

    def __start_game(self):
        try:
            player_positions = []
            for i, (x_entry, y_entry, color) in enumerate(self.coordinates):
                y = int(x_entry.get()) - 1  # Swap x and y for internal coordinate system
                x = int(y_entry.get()) - 1  # Swap x and y for internal coordinate system

                # Validate coordinates
                if not (0 <= x < self.cols and 0 <= y < self.rows):
                    raise ValueError(f"Coordinates for player {i + 1} are out of bounds.")
                if (x, y) in [pos for pos, _ in player_positions]:
                    raise ValueError(f"Coordinates for player {i + 1} overlap with another player.")

                player_positions.append(((x, y), color))

            self.coord_window.destroy()  # Close the coordinate entry window

            # Start the game with the grid size and player positions
            game_root = tk.Tk()
            game_app = WanderingGame(game_root, (self.cols, self.rows), player_positions)
            game_root.mainloop()

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))  # Show error message for invalid inputs

class WanderingGame3to5Launcher(AbstractGameLauncher):
    # Method to launch the game.
    def launch_game(self):
        root = tk.Tk()
        app = StartScreen(root)
        root.mainloop()

# Check if this script is run directly and then start the main function.
if __name__ == "__main__":
    game_launcher = WanderingGame3to5Launcher()
    game_launcher.launch_game()