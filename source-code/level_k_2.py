import tkinter as tk
from tkinter import messagebox
import random
import pygame
import pyttsx3  # Import for text-to-speech functionality
from abstract_classes import AbstractWanderingGame, AbstractGameLauncher

class Player:
    def __init__(self, canvas, color, grid_size, start_position):
        # Creating Private variables by adding double underscore, else they can be accessed by outside functions.
        self.__canvas = canvas
        self.__color = color
        self.__grid_size = grid_size
        self.__position = start_position
        self.size = 50  # Size of each cell on the grid
        self.__avatar = self.create_avatar()  # Create player avatar

    def create_avatar(self):
        x, y = self.__position
        # Draw an oval (player) at the starting position
        return self.__canvas.create_oval(
            x * self.size, y * self.size, 
            (x + 1) * self.size, (y + 1) * self.size, 
            fill=self.__color, outline="black"
        )

    def get_valid_moves(self):
        x, y = self.__position
        valid_moves = []
        # Check available moves based on current position
        if y > 0:  # Up
            valid_moves.append('up')
        if y < self.__grid_size[1] - 1:  # Down
            valid_moves.append('down')
        if x > 0:  # Left
            valid_moves.append('left')
        if x < self.__grid_size[0] - 1:  # Right
            valid_moves.append('right')

        return valid_moves

    def move(self):
        valid_moves = self.get_valid_moves()
        direction = random.choice(valid_moves)  # Choose a random valid move
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

        self.__position = (x, y)
        # Move avatar to the new position on the canvas
        self.__canvas.coords(
            self.__avatar, 
            x * self.size, y * self.size, 
            (x + 1) * self.size, (y + 1) * self.size
        )
    
    def get_position(self):
        return self.__position

    def change_color(self, new_color):
        self.__color = new_color  # Update player's color
        self.__canvas.itemconfig(self.__avatar, fill=new_color)  # Change avatar color on canvas

class WanderingGameKto2(AbstractWanderingGame):
    def __init__(self, root):
        pygame.mixer.init()  # Initialize pygame for sound
        pygame.mixer.music.load("happy-and-joyful-children.wav")  # Load background music
        
        self.__root = root
        self.__root.title("Wandering Game K-2")
        grid_size = random.randint(3, 7) # Randomly select the size of the grid.
        self.__grid_size = (grid_size, grid_size)  # Ensure square grid
        self.__cell_size = 50  # Size of each grid cell in pixels
        self.__canvas = tk.Canvas(root, width=grid_size * self.__cell_size, height=grid_size * self.__cell_size, bg="white")
        self.__canvas.pack()

        self.__root.resizable(False, False)  # Prevent window resizing

        self.create_grid()  # Draw the grid
        # Initialize two players at opposite corners
        self.__players = [
            Player(self.__canvas, "red", self.__grid_size, start_position=(0, 0)),
            Player(self.__canvas, "blue", self.__grid_size, start_position=(grid_size - 1, grid_size - 1))
        ]

        self.__move_count = 0  # Track the number of moves
        self.run_game()  # Start the game loop

        pygame.mixer.music.play(loops=-1)  # Play background music in a loop

        self.__text_to_speech_engine = pyttsx3.init()  # Initialize text-to-speech engine

    def create_grid(self):
        # Draw vertical lines to form the grid
        for i in range(self.__grid_size[0] + 1):
            self.__canvas.create_line(
                i * self.__cell_size, 0, 
                i * self.__cell_size, self.__grid_size[1] * self.__cell_size,
                fill="black"
            )
        # Draw horizontal lines to form the grid
        for j in range(self.__grid_size[1] + 1):
            self.__canvas.create_line(
                0, j * self.__cell_size, 
                self.__grid_size[0] * self.__cell_size, j * self.__cell_size,
                fill="black"
            )

    def __check_if_together(self):
        # Check if both players are at the same position
        return self.__players[0].get_position() == self.__players[1].get_position()

    def run_game(self):
        # Schedule the first move after an initial delay
        self.__root.after(600, self.__move_players)

    def __move_players(self):
        self.__move_count += 1  # Increment move count
        for player in self.__players:
            player.move()  # Move each player
        if self.__check_if_together():
            self.__update_colors()  # Change colors if players meet
            self.__canvas.create_text(
                    self.__grid_size[0] * 25, self.__grid_size[1] * 25,
                    text="Game Over",
                    font=("Helvetica", 20, "bold"),
                    fill="black"
                )
            
            self.__root.after(500, self.show_statistics)  # Show game statistics
        else:
            self.__root.after(500, self.__move_players)  # Continue moving players

    def __update_colors(self):
        # Change both players' color to purple when they meet
        self.__players[0].change_color("purple")
        self.__players[1].change_color("purple")

    def show_statistics(self):
        pygame.mixer.music.stop()  # Stop background music

        # Create a new window for game statistics
        stats_window = tk.Toplevel(self.__root)
        stats_window.title("Game Statistics")
        stats_window.resizable(False, False)

        # Display the game result
        stats_label = f"Number of moves to meet: {self.__move_count}"
        tk.Label(stats_window, text="Hurray! Players have met!", font=("Helvetica", 18)).pack(pady=10, padx=(20, 20))  # Added padding
        tk.Label(stats_window, text=stats_label, font=("Helvetica", 18)).pack(pady=10, padx=(20, 20))  # Added padding

        # Restart or quit game options
        def restart_game():
            stats_window.destroy()
            self.__root.destroy()
            start_root = tk.Tk()
            WanderingGameKto2(start_root)
            start_root.mainloop()

        def quit_game():
            stats_window.destroy()
            self.__root.destroy()

        button_frame = tk.Frame(stats_window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Restart Game", command=restart_game).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Quit Game", command=quit_game).pack(side=tk.LEFT, padx=5)

        def close_all():
            # Safely close all windows
            if stats_window.winfo_exists():
                stats_window.destroy()
            if self.__root.winfo_exists():
                self.__root.destroy()
            self.__cleanup_engine()

        self.__root.after(100, self.__announce_success)  # Announce success after brief delay

        stats_window.protocol("WM_DELETE_WINDOW", close_all)
        self.__root.protocol("WM_DELETE_WINDOW", close_all)

    def __cleanup_engine(self):
        # Stop and clean up the text-to-speech engine
        if self.__text_to_speech_engine:
            self.__text_to_speech_engine.stop()
            del self.__text_to_speech_engine
        
    def __announce_success(self):
        # Announce game success using text-to-speech
        self.__text_to_speech_engine.say(f"Hurray! Players have met")
        self.__text_to_speech_engine.say(f"Number of moves to meet: {self.__move_count}.")
        self.__text_to_speech_engine.runAndWait()

class WanderingGameKto2Launcher(AbstractGameLauncher):
    
    # Method to launch the game.
    def launch_game(self):
        root = tk.Tk()
        app = WanderingGameKto2(root)
        root.mainloop()

# Check if this script is run directly and then start the main function.
if __name__ == "__main__":
    game_launcher = WanderingGameKto2Launcher()
    game_launcher.launch_game()
