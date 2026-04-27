#add the local path to the library search dir
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

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
from LevelManager import *
from OpenGL.GL import *

IS_MULTISAMPLING_ENABLED = True

def main() -> None:

    #compatability fix
    choose_video_driver()

    #pygame setup
    pygame.init()
    pygame.display.set_caption(renderer.WINDOW_TITLE)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
    pygame.display.set_mode(renderer.WINDOW_SIZE, DOUBLEBUF | OPENGL)

    icon = pygame.image.load(os.path.join("Assets", "Icons", "windowicon.png")).convert_alpha()
    pygame.display.set_icon(icon)

    # Sync renderer sizing/aspect ratio to the actual surface.
    renderer.WINDOW_SIZE = pygame.display.get_surface().get_size()
    inputManager.init(renderer.WINDOW_SIZE)

    # OpenGL setup must happen after the OpenGL context exists (after set_mode).
    renderer.initRenderer()

    #Easy toggle for performance reason
    if IS_MULTISAMPLING_ENABLED:

        glEnable(GL_MULTISAMPLE)

    #msc setup
    time.initTime(renderer.FRAMERATE_CAP)

    Start()

    while True:
        # Save position before movement
        old_pos = (camera.x, camera.z)
        
        renderer.stepRenderer()

        # Check if the new position causes a collision, allow sliding
        adjusted_pos, has_collision = physicsManager.CheckCollisions((camera.x, camera.z), old_pos)
        
        # Apply the adjusted position (either reverted or slid)
        camera.x, camera.z = adjusted_pos
        camera.camera_pos_2d = adjusted_pos

        Update()


#Start of game logic behavior
def Start():
    textures.PreloadTextures()
    musicManager.PreloadMusic()

    musicManager.PlayMusic("Main Theme")

    #Get texture refs
    WallTex = textures.GetTexture("Wall")
    ui_tex = textures.GetTexture("UI_Main")

    create_ui_rect((-1,-1,0), (1,-0.6,0), ui_tex, uv_mode="stretch", tile_u=8.0, tile_v=8.0)


    levelManager.load_level("Level1")

def Update():
    physicsManager.Raycast((camera.camera_pos_2d[0] + 1, camera.camera_pos_2d[1] + 1), camera.forward_vector)



if __name__ == "__main__":
    main()
