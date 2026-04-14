import os
import sys
from math import tan, radians, sqrt

import pygame
from OpenGL.GL import *
from pygame import QUIT

from Camera import camera
from InputManager import inputManager
from Time import time
from ObjectManager import objectManager, Wall, Floor


def choose_video_driver() -> None:
    if os.environ.get("SDL_VIDEODRIVER"):
        return

    if os.environ.get("DISPLAY"):
        os.environ["SDL_VIDEODRIVER"] = "x11"
        return

    if os.environ.get("WAYLAND_DISPLAY"):
        os.environ["SDL_VIDEODRIVER"] = "wayland"


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


def draw_textured_quad(
    texture_id: int,
    topLeftPos: tuple = (-0.5, 0.5, 0.0),
    bottomRightPos: tuple = (0.5, -0.5, 0.0),
    *,
    uv_mode: str = "tile",   # "stretch" or "tile"
    tile_u: float = 5.0,     # repeats per world unit along U
    tile_v: float = 5.0,     # repeats per world unit along V
    u_offset: float = 0.0,
    v_offset: float = 0.0,
) -> None:
    if texture_id is None:
        raise RuntimeError(
            "texture_id is None. Call renderer.initRenderer() after creating the OpenGL context "
            "(pygame.display.set_mode(..., OPENGL)) before drawing."
        )
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

    if uv_mode == "stretch":
        texcoords = [
            (0.0 + u_offset, 0.0 + v_offset),
            (1.0 + u_offset, 0.0 + v_offset),
            (1.0 + u_offset, 1.0 + v_offset),
            (0.0 + u_offset, 1.0 + v_offset),
        ]
    else:
        # Tile: compute repeats from world-space size.
        # Use XZ distance for "width" so it works if Z changes; height comes from Y.
        dx = x2 - x1
        dz = z2 - z1
        quad_width = sqrt(dx * dx + dz * dz) if (dx != 0 or dz != 0) else abs(x2 - x1)
        quad_height = abs(y2 - y1)

        repeat_u = quad_width * tile_u
        repeat_v = quad_height * tile_v
        texcoords = [
            (0.0 + u_offset, 0.0 + v_offset),
            (repeat_u + u_offset, 0.0 + v_offset),
            (repeat_u + u_offset, repeat_v + v_offset),
            (0.0 + u_offset, repeat_v + v_offset),
        ]

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)

    for index, vertex in enumerate(vertexes):
        glTexCoord2f(texcoords[index][0], texcoords[index][1])
        glVertex3fv(vertex)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)

def draw_floor(
    texture_id: int,
    corner_a: tuple,
    corner_b: tuple,
    *,
    uv_mode: str = "tile",   # "stretch" or "tile"
    tile_u: float = 5.0,     # repeats per world unit along U (X)
    tile_v: float = 5.0,     # repeats per world unit along V (Z)
    u_offset: float = 0.0,
    v_offset: float = 0.0,
    double_sided: bool = True,
) -> None:
    """
    Draw a horizontal quad in the XZ plane (a floor/ceiling).

    corner_a/corner_b are opposite corners: (x, y, z). Y is taken from corner_a.
    """
    if texture_id is None:
        raise RuntimeError(
            "texture_id is None. Call renderer.initRenderer() after creating the OpenGL context "
            "(pygame.display.set_mode(..., OPENGL)) before drawing."
        )

    x1, y, z1 = corner_a
    x2, _, z2 = corner_b

    # Normalize so (x_min, z_min) .. (x_max, z_max)
    x_min, x_max = (x1, x2) if x1 <= x2 else (x2, x1)
    z_min, z_max = (z1, z2) if z1 <= z2 else (z2, z1)

    # Vertex order chosen for an upward-facing normal in a right-handed system.
    vertexes = [
        (x_min, y, z_max),
        (x_max, y, z_max),
        (x_max, y, z_min),
        (x_min, y, z_min),
    ]

    if uv_mode == "stretch":
        texcoords = [
            (0.0 + u_offset, 0.0 + v_offset),
            (1.0 + u_offset, 0.0 + v_offset),
            (1.0 + u_offset, 1.0 + v_offset),
            (0.0 + u_offset, 1.0 + v_offset),
        ]
    else:
        quad_width = abs(x_max - x_min)
        quad_depth = abs(z_max - z_min)
        repeat_u = quad_width * tile_u
        repeat_v = quad_depth * tile_v
        texcoords = [
            (0.0 + u_offset, 0.0 + v_offset),
            (repeat_u + u_offset, 0.0 + v_offset),
            (repeat_u + u_offset, repeat_v + v_offset),
            (0.0 + u_offset, repeat_v + v_offset),
        ]

    cull_enabled = glIsEnabled(GL_CULL_FACE)
    if double_sided and cull_enabled:
        glDisable(GL_CULL_FACE)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for index, vertex in enumerate(vertexes):
        glTexCoord2f(texcoords[index][0], texcoords[index][1])
        glVertex3fv(vertex)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)

    if double_sided and cull_enabled:
        glEnable(GL_CULL_FACE)


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


def set_ortho_ndc() -> None:
    # Simple UI projection: coordinates in [-1, 1] for both X and Y.
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


class Renderer:
    def __init__(self):
        self.texture_id = None
        self.WINDOW_SIZE = (1920, 1080)
        self.WINDOW_TITLE = "PyDoom"
        self.FRAMERATE_CAP = 240
        self.BACKGROUND = (0.455, 0.204, 0.922, 1.0)

    def initRenderer(self) -> None:
        glEnable(GL_TEXTURE_2D)
        glViewport(0, 0, self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])

        # setup camera and initial position
        set_perspective(45, self.WINDOW_SIZE[0] / self.WINDOW_SIZE[1], 0.1, 1000)
        glTranslatef(0.0, 0.0, -5)
        glRotatef(0, 0, 0, 0)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        # setup face culling
        glCullFace(GL_BACK)
        glFrontFace(GL_CW)

        glClearColor(*self.BACKGROUND)

    def toggle_fullscreen(self) -> None:
        # Best-effort: this usually preserves the OpenGL context, so textures stay valid.
        try:
            pygame.display.toggle_fullscreen()
        except Exception:
            return

        surface = pygame.display.get_surface()
        if surface is None:
            return

        self.WINDOW_SIZE = surface.get_size()
        glViewport(0, 0, self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
        set_perspective(45, self.WINDOW_SIZE[0] / self.WINDOW_SIZE[1], 0.1, 1000)
        inputManager.init(self.WINDOW_SIZE)

    def stepRenderer(self):
        time.updateDeltaTime()
        dt = time.getDeltaTime()

        # Check if the user Xed out of the window
        for event in pygame.event.get():
            if event.type == QUIT:
                print("\nUser Closed Window")
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                self.toggle_fullscreen()

        # Wipe and clear previous frame
        glClearColor(*self.BACKGROUND)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Get user input before rendering frame
        inputManager.pollInput()

        # --- World pass (3D) ---
        set_perspective(45, self.WINDOW_SIZE[0] / self.WINDOW_SIZE[1], 0.1, 1000)

        # Apply rotations
        glRotatef(camera.rotationX, 1, 0, 0)
        glRotatef(camera.rotationY, 0, 1, 0)
        glRotatef(camera.rotationZ, 0, 0, 1)

        glTranslatef(-camera.x, camera.y, -camera.z - 5.0)

        # draw world-space objects
        draw_object(objectManager.objects)

        # --- UI pass (2D, drawn last so it overlays the world) ---
        glClear(GL_DEPTH_BUFFER_BIT)
        depth_enabled = glIsEnabled(GL_DEPTH_TEST)
        cull_enabled = glIsEnabled(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        set_ortho_ndc()
        draw_object(objectManager.uiObjects)
        if cull_enabled:
            glEnable(GL_CULL_FACE)
        if depth_enabled:
            glEnable(GL_DEPTH_TEST)

        pygame.display.flip()  # Same as glfwSwapBuffers

def draw_object(object_array):
    for i in range(len(object_array)):
        current_object = object_array[i]
        if isinstance(current_object, Wall):
            draw_textured_quad(
                current_object.texture,
                current_object.top_left,
                current_object.bottom_right,
                uv_mode=getattr(current_object, "uv_mode", "tile"),
                tile_u=getattr(current_object, "tile_u", 5.0),
                tile_v=getattr(current_object, "tile_v", 5.0),
                u_offset=getattr(current_object, "u_offset", 0.0),
                v_offset=getattr(current_object, "v_offset", 0.0),
            )
        elif isinstance(current_object, Floor):
            draw_floor(
                current_object.texture,
                current_object.corner_a,
                current_object.corner_b,
                uv_mode=getattr(current_object, "uv_mode", "tile"),
                tile_u=getattr(current_object, "tile_u", 5.0),
                tile_v=getattr(current_object, "tile_v", 5.0),
                u_offset=getattr(current_object, "u_offset", 0.0),
                v_offset=getattr(current_object, "v_offset", 0.0),
                double_sided=True,
            )
        else:
            raise RuntimeError(f"Object {current_object} is not a valid game object. (Instance ID: {i})")

renderer = Renderer()
