import os
import sys
from math import tan, radians

from OpenGL.GL import *
from pygame.locals import *
import pygame

import InputManager

inputManager = InputManager.inputManager

WINDOW_SIZE = (1920, 1080)
WINDOW_TITLE = "PyDoom"
FRAMERATE_CAP = 240
BACKGROUND = (0.455, 0.204, 0.922, 1.0)

def load_texture(path: str) -> int:
    surface = pygame.image.load(path).convert_alpha()
    image_data = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

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


vertexes = [
    (-0.5, -0.5, 0.0), 
    ( 0.5, -0.5, 0.0), 
    ( 0.5,  0.5, 0.0), 
    (-0.5,  0.5, 0.0),
]

texcoords = [
    (0, 0),
    (1, 0),
    (1, 1),
    (0, 1)
]

def triangle(texture_id: int):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for index, vertex in enumerate(vertexes):
        glTexCoord2f(texcoords[index][0], texcoords[index][1])
        glVertex3fv(vertex)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)




def choose_video_driver() -> None:
    if os.environ.get("SDL_VIDEODRIVER"):
        return

    if os.environ.get("DISPLAY"):
        os.environ["SDL_VIDEODRIVER"] = "x11"
        return

    if os.environ.get("WAYLAND_DISPLAY"):
        os.environ["SDL_VIDEODRIVER"] = "wayland"


def set_perspective(fov_degrees: float, aspect_ratio: float, near: float, far: float) -> None:
    top = near * tan(radians(fov_degrees) / 2)
    bottom = -top
    right = top * aspect_ratio
    left = -right

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(left, right, bottom, top, near, far)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main() -> None:
    angle = 0

    choose_video_driver()
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)
    pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF | OPENGL)

    texture_path = os.path.join("Assets", "Textures", "test.jpg")
    texture_id = load_texture(texture_path)
    glEnable(GL_TEXTURE_2D)

    set_perspective(45, WINDOW_SIZE[0] / WINDOW_SIZE[1], 0.1, 1000)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)

    glClearColor(*BACKGROUND)

    clock = pygame.time.Clock()
    running = True

    while True:
        dt_ms = clock.tick(FRAMERATE_CAP)
        dt = dt_ms / 1000.0
        angle += 90.0 * dt

        #Check if the user Xed out of the window
        for event in pygame.event.get():
            if event.type == QUIT:
                print("\nUser Closed Window")
                sys.exit(0)

        #Wipe and clear previous frame
        glClearColor(*BACKGROUND)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #Get user input before rendering frame
        inputManager.pollInput()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)
        glRotatef(angle, 0, 1, 0)
        triangle(texture_id)


        pygame.display.flip()   #Same as glfwSwapBuffers

    pygame.quit()


if __name__ == "__main__":
    main()
