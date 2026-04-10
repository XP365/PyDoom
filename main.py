import os
import sys
import pygame

from math import tan, radians
from OpenGL.GL import *
from pygame.locals import *

from InputManager import inputManager
from Time import time
from Camera import camera

WINDOW_SIZE = (1920, 1080)
WINDOW_TITLE = "PyDoom"
FRAMERATE_CAP = 240
BACKGROUND = (0.455, 0.204, 0.922, 1.0)

def load_texture(path: str) -> int:
    surface = pygame.image.load(path).convert_alpha()

    image_data = pygame.image.tostring(surface, "RGBA", False)
    width, height = surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

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

from OpenGL.GL import *


def draw_textured_quad(texture_id: int, topLeftPos: tuple = (-0.5, 0.5, 0.0),
                       bottomRightPos: tuple = (0.5, -0.5, 0.0)) -> None:
    # Assuming standard 2D quad (topLeft, topRight, bottomRight, bottomLeft)
    # Using the provided positions to define the corners
    x1, y1, z1 = topLeftPos
    x2, y2, z2 = bottomRightPos

    vertexes = [
        (x1, y2, z1),  # Bottom Left (Using x from top, y from bottom for standard rect)
        (x2, y2, z2),  # Bottom Right
        (x2, y1, z2),  # Top Right
        (x1, y1, z1),  # Top Left
    ]

    # Calculate world-space dimensions of the quad
    quad_width = abs(x2 - x1)
    quad_height = abs(y2 - y1)

    # Div by a scaler
    repeat_u = quad_width / (1/5)
    repeat_v = quad_height / (1/5)

    # Normalized texture coordinates (U, V)
    # 0,0 is bottom-left, 1,1 is top-right


    texcoords = [
        (0.0, 0.0),
        (repeat_u, 0.0),
        (repeat_u, repeat_v),
        (0.0, repeat_v),
    ]

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

    #compatability fix
    choose_video_driver()

    #pygame setup
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)
    pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF | OPENGL)

    #msc setup
    time.initTime(FRAMERATE_CAP)

    #temp texture
    texture_path = os.path.join("Assets", "Textures", "test.jpg")
    texture_id = load_texture(texture_path)
    glEnable(GL_TEXTURE_2D)

    #setup camera and initial position
    set_perspective(45, WINDOW_SIZE[0] / WINDOW_SIZE[1], 0.1, 1000)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(0, 0, 0, 0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    #setup face culling
    glCullFace(GL_BACK)
    glFrontFace(GL_CW)

    glClearColor(*BACKGROUND)


    running = True

    while True:
        time.updateDeltaTime()
        dt = time.getDeltaTime()

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

        # 3. Apply rotations
        glRotatef(camera.rotationX, 1, 0, 0)
        glRotatef(camera.rotationY, 0, 1, 0)
        glRotatef(camera.rotationZ, 0, 0, 1)

        glTranslatef(-camera.x, camera.y, -camera.z - 5.0)



        draw_textured_quad(texture_id, (-0.5,-0.5,0), (0.5,0.5,0))

        pygame.display.flip()   #Same as glfwSwapBuffers


if __name__ == "__main__":
    main()
