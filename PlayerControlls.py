from GameManager import gameManager
from Camera import camera
from Vectors import Vector3
from Time import Time
import pygame

class PlayerController:
    def __init__(self):
        self.move_speed = 120.0
        self.turn_speed = 2.2
        self.mouse_sensitivity = 0.003

    def pollInput(self):
        move_speed_factor = self.move_speed * Time.deltaTime
        turn_speed_factor = self.turn_speed * Time.deltaTime

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameManager.gameShutdown(0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            gameManager.gameShutdown(0)

        surface = pygame.display.get_surface()
        if surface is not None and pygame.mouse.get_focused():
            center_x = surface.get_width() // 2
            center_y = surface.get_height() // 2
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_delta_x = mouse_x - center_x
            mouse_delta_y = mouse_y - center_y

            camera.rotateCamera(
                Vector3(
                    -mouse_delta_y * self.mouse_sensitivity,
                    mouse_delta_x * self.mouse_sensitivity,
                    0,
                )
            )
            pygame.mouse.set_pos((center_x, center_y))

        if keys[pygame.K_w]:
            self._move(camera.get_forward_vector(), move_speed_factor)
        if keys[pygame.K_s]:
            self._move(camera.get_forward_vector(), -move_speed_factor)
        if keys[pygame.K_a]:
            self._move(camera.get_right_vector(), -move_speed_factor)
        if keys[pygame.K_d]:
            self._move(camera.get_right_vector(), move_speed_factor)
        if keys[pygame.K_SPACE]:
            self._move(camera.get_up_vector(), move_speed_factor)
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self._move(camera.get_up_vector(), -move_speed_factor)

        if keys[pygame.K_LEFT]:
            camera.rotateCamera(Vector3(0, -turn_speed_factor, 0))
        if keys[pygame.K_RIGHT]:
            camera.rotateCamera(Vector3(0, turn_speed_factor, 0))
        if keys[pygame.K_UP]:
            camera.rotateCamera(Vector3(-turn_speed_factor, 0, 0))
        if keys[pygame.K_DOWN]:
            camera.rotateCamera(Vector3(turn_speed_factor, 0, 0))
        if keys[pygame.K_q]:
            camera.rotateCamera(Vector3(0, 0, -turn_speed_factor))
        if keys[pygame.K_e]:
            camera.rotateCamera(Vector3(0, 0, turn_speed_factor))

    def _move(self, direction, speed):
        camera.moveCamera(Vector3(direction.x * speed, direction.y * speed, direction.z * speed))

playerController = PlayerController()
