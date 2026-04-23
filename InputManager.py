import sys
import math
import pygame
from Camera import camera
from Time import time
from MusicManager import musicManager
from LevelManager import levelManager

# Adjust these to your liking
mouse_sensitivity = 0.15
moveSpeed = 5.0


class InputManager:
    def __init__(self):
        self._center = None
        self._relative_ok = False
        self._keys_down = None
        self._keys_down_prev = None

    def init(self, window_size: tuple[int, int]) -> None:
        # Must be called after the window exists (after pygame.display.set_mode).
        w, h = window_size
        self._center = (w // 2, h // 2)

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        # Preferred: relative mouse mode keeps motion working without warping the cursor.
        try:
            self._relative_ok = bool(pygame.mouse.set_relative(True))
        except Exception:
            self._relative_ok = False

        if not self._relative_ok:
            pygame.mouse.set_pos(self._center)

        # Flush any accumulated movement from initialization.
        pygame.mouse.get_rel()

    def is_key_pressed(self, key: int) -> bool:
        """True only on the frame the key transitions up->down."""
        keys = self._keys_down if self._keys_down is not None else pygame.key.get_pressed()
        prev_keys = self._keys_down_prev

        if key >= len(keys):
            return False
        is_currently_pressed = bool(keys[key])
        was_pressed_last_frame = bool(prev_keys[key]) if prev_keys is not None and key < len(prev_keys) else False
        return is_currently_pressed and not was_pressed_last_frame

    def pollInput(self):
        dt = time.getDeltaTime()
        self._keys_down_prev = self._keys_down
        keys = pygame.key.get_pressed()
        self._keys_down = keys

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

        camera.forward_vector = (forward_x, forward_z)

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


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    musicManager.PlaySound("Shotgun Sound")

                if event.button == pygame.BUTTON_RIGHT:
                    levelManager.reload_level()


        # Fallback: keep the cursor centered if relative mode isn't available.
        if (not self._relative_ok) and (self._center is not None):
            pygame.mouse.set_pos(self._center)
            pygame.mouse.get_rel()  # Flush any warp-induced delta.


inputManager = InputManager()
