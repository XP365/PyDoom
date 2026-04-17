import Levels
import importlib

class LevelManager:
    def __init__(self):
        self.current_level = "Level1"

    def load_level(self, level_data):
        importlib.import_module("Levels." + self.current_level)
        


levelManager = LevelManager()