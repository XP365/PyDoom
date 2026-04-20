import importlib
from ObjectManager import *
from PhysicsManager import physicsManager

class LevelManager:
    def __init__(self):
        self.current_level = "Level1"
        self._level_module = None

    def load_level(self, level_name: str):
        self.current_level = level_name
        module_name = "Levels." + self.current_level
        self._level_module = importlib.import_module(module_name)
        self._level_module.CreateObjects()

    def unload_level(self):
        del objectManager.objects[:]
        del physicsManager.colliders[:]

    def reload_level(self):
        self.unload_level()
        if self._level_module is None:
            self.load_level(self.current_level)
            return
        self._level_module = importlib.reload(self._level_module)
        self._level_module.CreateObjects()
        


levelManager = LevelManager()
