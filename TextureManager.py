import os

from OpenGL.GL import *
import pygame

class Textures:
    def __init__(self):
        self.textures = {}

    def load_texture(self,path: str) -> int:
        surface = pygame.image.load(path).convert_alpha()

        image_data = pygame.image.tostring(surface, "RGBA", False)
        width, height = surface.get_size()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            image_data,
        )

        glBindTexture(GL_TEXTURE_2D, 0)
        return texture_id


    def AddPreloadedTexture(self, path, alias):
        self.textures[alias] = self.load_texture(path)

    def GetTexture(self, alias):
        if alias not in self.textures:
            print("ALERT: TEXTURE {alias} NOT REGISTERED")
            exit(-1)
        return self.textures[alias]

    def PreloadTextures(self):
        self.AddPreloadedTexture(os.path.join("Assets", "Textures", "WallTemp.png"), "Wall")
        self.AddPreloadedTexture(os.path.join("Assets", "Textures", "hud.png"), "UI_Main")
        self.AddPreloadedTexture(os.path.join("Assets", "Textures", "RedSkyWRock.png"), "Red_Wall")

        for i in range(8):
            self.AddPreloadedTexture(os.path.join("Assets", "Textures", "Weapons", "Shotgun", f"shotgun_frame{i}.png"), f"shotgun_frame{i}")




textures = Textures()
