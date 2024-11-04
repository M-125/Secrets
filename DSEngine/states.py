from enum import Enum

# Define the Game States Enum
class GameStateEnum(Enum):
    MAIN_MENU = "MainMenu"
    GAMEPLAY = "Gameplay"
    GAME_OVER = "GameOver"

# Define the Base State Class
class GameState:
    def __init__(self, window):
        self.window = window

    def enter(self):
        """Called when entering the state"""
        pass

    def exit(self):
        """Called when exiting the state"""
        pass

    def update(self):
        """Called every frame to update the state"""
        pass

    def render(self):
        """Called to render the state"""
        pass

    def handle_event(self, event):
        """Handle events specific to the state"""
        pass

class StateManager:
    def __init__(self):
        self.states = []

    def push_state(self, state):
        """Push a new state onto the stack"""
        if self.states:
            self.states[-1].exit()  # Call exit on the current state
        self.states.append(state)
        state.enter()  # Call enter on the new state

    def pop_state(self):
        """Pop the current state off the stack"""
        if self.states:
            state = self.states.pop()
            state.exit()  # Call exit on the current state
            if self.states:
                self.states[-1].enter()  # Call enter on the new current state

    def update(self, delta_time):
        """Update the current state"""
        if self.states:
            self.states[-1].update(delta_time)

    def render(self, surface):
        """Render the current state"""
        if self.states:
            self.states[-1].render(surface)

    def handle_event(self, event):
        """Handle events for the current state"""
        if self.states:
            self.states[-1].handle_event(event)
