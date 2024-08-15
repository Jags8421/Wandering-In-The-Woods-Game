from abc import ABC, abstractmethod

# Abstract class defining the interface for the Wandering Game itself.
class AbstractWanderingGame(ABC):
    
    # Abstract method for creating the game grid.
    @abstractmethod
    def create_grid(self):
        pass

    # Abstract method for displaying game statistics at the end of the game.
    @abstractmethod
    def show_statistics(self):
        pass

    # Abstract method for running the game loop.
    @abstractmethod
    def run_game(self):
        pass

# Abstract class defining the interface for the Wandering Game itself.
class AbstractGameLauncher(ABC):
    
    # Abstract Method to Launch the game for a specific level.
    @abstractmethod
    def launch_game(self):
        pass