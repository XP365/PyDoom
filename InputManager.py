import sys
import math
import pygame
from Camera import camera
from Time import time

# Adjust these to your liking
mouse_sensitivity = 0.15
moveSpeed = 5.0


class InputManager:
    def __init__(self):
        pygame.init()
        # 1. Hide the mouse and lock it to the center of the window
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    @staticmethod
    def pollInput():
        dt = time.getDeltaTime()
        keys = pygame.key.get_pressed()

        # --- Close Game ---
        if keys[pygame.K_ESCAPE]:
            print("\nUser Closed the Game")
            sys.exit()


        # --- MOUSE LOOK ---
        # get_rel returns (delta_x, delta_y) since the last call
        mouse_dx, mouse_dy = pygame.mouse.get_rel()

        # Update horizontal rotation (Y-axis)
        camera.rotationY += mouse_dx * mouse_sensitivity

        # Update vertical rotation (X-axis)
        camera.rotationX += mouse_dy * mouse_sensitivity

        # Clamp vertical look so you can't flip upside down
        if camera.rotationX > 90: camera.rotationX = 90
        if camera.rotationX < -90: camera.rotationX = -90

        # --- MOVEMENT  ---
        angle = math.radians(camera.rotationY)

        # Forward Vector
        forward_x = math.sin(angle)
        forward_z = -math.cos(angle)

        # Right Vector (Strafe)
        right_x = math.cos(angle)
        right_z = math.sin(angle)

        if keys[pygame.K_w]:
            camera.x += forward_x * moveSpeed * dt
            camera.z += forward_z * moveSpeed * dt
        if keys[pygame.K_s]:
            camera.x -= forward_x * moveSpeed * dt
            camera.z -= forward_z * moveSpeed * dt
        if keys[pygame.K_a]:
            camera.x -= right_x * moveSpeed * dt
            camera.z -= right_z * moveSpeed * dt
        if keys[pygame.K_d]:
            camera.x += right_x * moveSpeed * dt
            camera.z += right_z * moveSpeed * dt


inputManager = InputManager()
