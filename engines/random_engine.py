# engines/random_engine.py - defines a random move selection engine

import random
from engines.base_engine import BaseEngine

class RandomEngine(BaseEngine):
    def select_move(self, valid_moves, game_state):
        return random.choice(valid_moves)

        # need to also implement promotion logic as well either here or in run_game.py
        