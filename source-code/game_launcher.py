import tkinter as tk
from tkinter import messagebox
from level_3_5 import WanderingGame3to5Launcher
from level_k_2 import WanderingGameKto2Launcher

class GameLauncher:
    def __init__(self):
        # Mapping display names to internal level identifiers
        self.__level_map = {
            "Kindergarten to Grade 2": "K-2",
            "Grade 3 to Grade 5": "3-5"
        }
        self.__level_to_game_launcher = {
            "K-2": WanderingGameKto2Launcher(),
            "3-5": WanderingGame3to5Launcher()
        }

    # Handle the selection of the game level.
    def handle_start_button_click(self, display_value, root):
        root.destroy()  # Close the selection window
        internal_value = self.__level_map[display_value]
        self.__level_to_game_launcher[internal_value].launch_game()

    # Display game rules in a message box.
    def show_rules(self):
        rules = (
            "Rules for Kindergarten Level (K-2):\n"
            "- The grid is always square.\n"
            "- Two players start in diagonally opposite corners.\n"
            "- Players wander randomly until they meet.\n\n"
            "Rules for 3-5 Level:\n"
            "- The grid can be rectangular.\n"
            "- Players can start anywhere on the grid.\n"
            "- The number of players can be between 2 and 4.\n"
            "- Players wander randomly until they all meet."
        )
        messagebox.showinfo("Game Rules", rules)

    # Main function to launch the game.
    def launch_game(self):
        # Initialize main window
        root = tk.Tk()
        root.title("Select Game Level")

        label = tk.Label(root, text="Select the game level:")
        label.pack(pady=10, padx=20)

        selected_value = tk.StringVar()
        display_names = list(self.__level_map.keys())
        selected_value.set(display_names[0])  # Set default option

        # Create dropdown menu with display names
        dropdown = tk.OptionMenu(root, selected_value, *display_names)
        dropdown.pack(pady=10) 

        # Create a frame to hold the buttons in a single row
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Button to start the selected game level
        select_button = tk.Button(button_frame, text="Start Game", command=lambda: self.handle_start_button_click(selected_value.get(), root))
        select_button.pack(side="left", padx=20)

        # Button to quit the game
        quit_game_button = tk.Button(button_frame, text="Quit Game", command=root.destroy)
        quit_game_button.pack(side="left", padx=20)

        # Label to show rules; clickable to display rules
        rules_label = tk.Label(root, text="Click here to view game rules", fg="blue", cursor="hand2")
        rules_label.pack(side="bottom", pady=10, padx=20) 
        rules_label.bind("<Button-1>", lambda e: self.show_rules())  # Bind click event to show rules

        root.mainloop()  # Run the main event loop

if __name__ == "__main__":
    game_launcher = GameLauncher()
    game_launcher.launch_game()
