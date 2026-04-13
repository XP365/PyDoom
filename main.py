import os

import pygame

from pygame.locals import *

from InputManager import inputManager
from ObjectManager import *
from Time import time
from Renderer import renderer, choose_video_driver, load_texture


def main() -> None:

    #compatability fix
    choose_video_driver()

    #pygame setup
    pygame.init()
    pygame.display.set_caption(renderer.WINDOW_TITLE)
    pygame.display.set_mode(renderer.WINDOW_SIZE, DOUBLEBUF | OPENGL)
    # Sync renderer sizing/aspect ratio to the actual surface.
    renderer.WINDOW_SIZE = pygame.display.get_surface().get_size()
    inputManager.init(renderer.WINDOW_SIZE)

    # OpenGL setup must happen after the OpenGL context exists (after set_mode).
    renderer.initRenderer()

    #msc setup
    time.initTime(renderer.FRAMERATE_CAP)

    Start()

    while True:
        renderer.stepRenderer()

#Start of game logic behavior
def Start():
    texture_path = os.path.join("Assets", "Textures", "WallTemp.png")
    texture_id = load_texture(texture_path)

    texture_path = os.path.join("Assets", "Textures", "hud.png")
    ui_tex = load_texture(texture_path)

    create_ui_rect((-1,-1,0), (1,-0.6,0), ui_tex, uv_mode="stretch", tile_u=8.0, tile_v=8.0)

    create_wall((0, 0, 0), (7, 5, 0), texture_id, tile_u=0.2, tile_v=0.2)
    create_wall((5, 0, 5), (5, 5, 10), texture_id)



if __name__ == "__main__":
    main()
