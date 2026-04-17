import pygame
from pygame.locals import *

from InputManager import inputManager
from MusicManager import musicManager
from ObjectManager import *
from Time import *
from Renderer import renderer, choose_video_driver, load_texture
from TextureManager import *
from PhysicsManager import *
from Camera import *


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
        # Save position before movement
        old_pos = (camera.x, camera.z)
        
        renderer.stepRenderer()

        # Check if the new position causes a collision
        _, has_collision = physicsManager.CheckCollisions((camera.x, camera.z))
        
        # If collision detected, revert to the old position
        if has_collision:
            camera.x, camera.z = old_pos


#Start of game logic behavior
def Start():
    textures.PreloadTextures()
    musicManager.PreloadMusic()

    #Get texture refs
    WallTex = textures.GetTexture("Wall")
    ui_tex = textures.GetTexture("UI_Main")

    create_ui_rect((-1,-1,0), (1,-0.6,0), ui_tex, uv_mode="stretch", tile_u=8.0, tile_v=8.0)

    create_wall((0, 0, 0), (7, 5, 0), WallTex, tile_u=0.2, tile_v=0.2)
    create_wall((5, 0, 5), (5, 5, 10), WallTex, tile_u=0.2, tile_v=0.2)

    #floors
    floor_width = 10
    create_floor((-floor_width, 0, -floor_width), (floor_width, 0, floor_width), WallTex, tile_u=0.2, tile_v=0.2)


if __name__ == "__main__":
    main()
