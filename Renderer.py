import pygame
import numpy as np
import ObjectManager
import Camera
from GameManager import gameManager
from Time import Time


class Renderer:

    def __init__(self, width, height):
        pygame.init()
        display_info = pygame.display.Info()
        self.width = display_info.current_w
        self.height = display_info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption("Pyoom")
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos((self.width // 2, self.height // 2))
        self.clock = pygame.time.Clock()
        self.running = True
        self.deltaTime = 0

        self.camera_matrix = np.array(
            [[800, 0, self.width / 2],
            [0, 800, self.height / 2],
            [0, 0, 1]], dtype=np.float32)
        self.focal_length_x = float(self.camera_matrix[0, 0])
        self.focal_length_y = float(self.camera_matrix[1, 1])
        self.center_x = float(self.camera_matrix[0, 2])
        self.center_y = float(self.camera_matrix[1, 2])
        self.near_plane = 0.1
        Time.deltaTime = 1.0 / gameManager.frameCap

    def beginFrame(self):
        Time.deltaTime = self.clock.tick(gameManager.frameCap) / 1000.0
        if pygame.mouse.get_focused():
            pygame.event.set_grab(True)
            pygame.mouse.set_visible(False)

    def stepRenderer(self):
        # flip() the display to put the image on screen
        pygame.display.flip()

    def drawAllObjects(self):
        for currentObject in ObjectManager.objectManager.currentObjects:
            if isinstance(currentObject, ObjectManager.Square):
                camera_points = [
                    Camera.camera.world_to_camera(currentObject.topLeftVec),
                    Camera.camera.world_to_camera(currentObject.topRightVec),
                    Camera.camera.world_to_camera(currentObject.BottomRightVec),
                    Camera.camera.world_to_camera(currentObject.BottomLeftVec),
                ]

                if any(point.z <= self.near_plane for point in camera_points):
                    continue

                pygame_points = []
                for point in camera_points:
                    screen_x = (self.focal_length_x * point.x / point.z) + self.center_x
                    screen_y = (self.focal_length_y * point.y / point.z) + self.center_y
                    pygame_points.append((int(screen_x), int(screen_y)))

                pygame.draw.polygon(self.screen, currentObject.color, pygame_points, 0)
