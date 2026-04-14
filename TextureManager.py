import os

from Renderer import load_texture

class Textures:
    def __init__(self):
        self.textures = {}

    def PreloadTextures(self):
        for i in range(len(self.textures)):
            load_texture(list(self.textures.values())[i])

    def AddPreloadedTexture(self, path, alias):
        self.textures[alias] = load_texture(path)

    def GetTexture(self, alias):
        return self.textures[alias]

    def PreloadTextures(self):
        self.AddPreloadedTexture(os.path.join("Assets", "Textures", "WallTemp.png"), "Wall")
        self.AddPreloadedTexture(os.path.join("Assets", "Textures", "hud.png"), "UI_Main")

textures = Textures()