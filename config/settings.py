# config/settings.py - configuration settings for chess app

class GameInfo:
    def __init__(self):
        self.WIDTH = 512
        self.HEIGHT = 512
        self.DIMENSION = 8
        self.SQ_SIZE = self.HEIGHT // self.DIMENSION
        self.MAX_FPS = 20

game_info = GameInfo()