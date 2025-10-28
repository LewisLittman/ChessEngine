# engines/base_engine.py - defines the base class for chess engines

class BaseEngine:
    def __init__(self, player_colour):
        self.player_colour = player_colour # w or b

    def select_move(self, valid_moves, game_state):
        raise NotImplementedError("This method should be overridden by subclasses.")
