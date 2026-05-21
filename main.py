#add the local path to the library search dir
import subprocess
import sys
import os
import threading
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

import pygame
from pygame.locals import *
from time import time



from InputManager import inputManager, playerController
from MusicManager import musicManager
from ObjectManager import *
from DoomTime import *
from Renderer import renderer, choose_video_driver
from TextureManager import *
from PhysicsManager import *
from NetworkManager import *
import NetworkManager
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
    doomTime.initTime(renderer.FRAMERATE_CAP)

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

hasAnounced = False
def Start():
    textures.PreloadTextures()
    musicManager.PreloadMusic()

    threading.Thread(target=start_chat, daemon=True).start()

    musicManager.PlayMusic("Main Theme")

    playerController.SetupPlayer()

    levelManager.load_level("Level1")

    playerController.Anounce("Welcome to PyDoom!\nUse WASD to move\nmouse to look around and\nleft click to shoot.", lifetime_seconds=3, text_position=(-1, 0.5, 0))

def Update():
    global hasAnounced
    
    SendPacket(NetworkManager.sock, f"{camera.x},{camera.y},{camera.z},{camera.rotationX}, {camera.rotationY}, {NetworkManager.enemyHit},")
    NetworkManager.enemyHit = False

    if NetworkManager.sock is None:
        return

    if hasAnounced == False:
        hasAnounced = True
        playerController.Anounce("Enemy player has connected. begin!")
        if NetworkManager.isServer:
            camera.x = -18.5
            camera.z = -12.5
        else:
            camera.x = 13.5
            camera.z = 18.5
                
    



if __name__ == "__main__":
    main()