import sys
import math
import pygame
from Camera import camera
from Time import time
from MusicManager import musicManager
from LevelManager import levelManager
from ObjectManager import *
from TextureManager import textures

# Adjust these to your liking
mouse_sensitivity = 0.15

class PlayerController:

    def __init__(self):
        #Player Properties
        self.can_move = True
        self.can_shoot = True


        self.moveSpeedForward = 0
        self.moveSpeedSideways = 0

        self.maxMoveSpeed = 5.0
        self.moveSpeedInc = 6
        self.moveSpeedDecay = 5

        gun_frames = [f"shotgun_frame{i}" for i in range(5)]


    def SetupPlayer(self):
        #Setup UI
        ui_tex = textures.GetTexture("UI_Main")

        self.MainUI = create_ui_rect((-1,-1,0), (1,-0.6,0), ui_tex, uv_mode="stretch", tile_u=8.0, tile_v=8.0)
        self.Gun = create_ui_rect((-0.5,-0.5,0), (0.5,0.5,0), ui_tex, uv_mode="stretch", tile_u=8.0, tile_v=8.0)
        self.GunFrame = 0


    def ShootWeapon(self):
        """Handle shooting logic, including raycasting and hit detection. Returns false if shooting was disabled, otherwise returns the result of the raycast (hit object or None)."""
        if self.can_shoot == False:
            return False
        
        # Implement shooting logic here
        hitObject = physicsManager.Raycast((camera.camera_pos_2d[0] + 1, camera.camera_pos_2d[1] + 1), camera.forward_vector)
        return hitObject
    
    def MovePlayer(self, dt):
        """Move the player based on input and delta time. Returns false if movement was disabled, otherwise returns true."""
        if self.can_move == False:
            self.moveSpeedForward = max(0, min(self.moveSpeedForward - self.moveSpeedInc, self.maxMoveSpeed))
            return False
        
        
        keys = pygame.key.get_pressed()

        angle = math.radians(camera.rotationY)
        
        # Forward Vector
        forward_x = math.sin(angle)
        forward_z = -math.cos(angle)

        camera.forward_vector = (forward_x, forward_z) # type: ignore

        # Right Vector (Strafe)
        right_x = math.cos(angle)
        right_z = math.sin(angle)
        
        accel = self.moveSpeedInc * dt
        friction = self.moveSpeedDecay * dt
        if keys[pygame.K_w]: self.moveSpeedForward += accel
        if keys[pygame.K_s]: self.moveSpeedForward -= accel

        if (keys[pygame.K_s] or keys[pygame.K_w]) == False: 
            if self.moveSpeedForward > 0:
                self.moveSpeedForward = max(0, self.moveSpeedForward - friction)
            elif self.moveSpeedForward < 0:
                self.moveSpeedForward = min(0, self.moveSpeedForward + friction)


        if keys[pygame.K_d]: self.moveSpeedSideways += accel
        if keys[pygame.K_a]: self.moveSpeedSideways -= accel

        if (keys[pygame.K_d] or keys[pygame.K_a]) == False:
            if self.moveSpeedSideways > 0:
                self.moveSpeedSideways = max(0, self.moveSpeedSideways - friction)
            elif self.moveSpeedSideways < 0:
                self.moveSpeedSideways = min(0, self.moveSpeedSideways + friction)


        self.moveSpeedForward = max(-self.maxMoveSpeed, min(self.moveSpeedForward, self.maxMoveSpeed))
        self.moveSpeedSideways = max(-self.maxMoveSpeed, min(self.moveSpeedSideways, self.maxMoveSpeed))

        camera.x += (forward_x * self.moveSpeedForward + right_x * self.moveSpeedSideways) * dt
        camera.z += (forward_z * self.moveSpeedForward + right_z * self.moveSpeedSideways) * dt


playerController = PlayerController()



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
            self._relative_ok = bool(pygame.mouse.set_relative(True)) # type: ignore
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
        

        playerController.MovePlayer(dt)


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
