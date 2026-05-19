import sys
import math
import NetworkManager
import numpy as np
import pygame
import threading
import time
from Camera import camera
from DoomTime import doomTime
from MusicManager import musicManager
from LevelManager import levelManager
from ObjectManager import *
from TextureManager import textures
from NetworkManager import *


# Adjust these to your liking
mouse_sensitivity = 0.15

class PlayerController:

    def __init__(self):
        #Player Properties
        self.can_move = True
        self.can_shoot = True

        self.HP = 100
        self.Armor = 0


        self.moveSpeedForward = 0
        self.moveSpeedSideways = 0

        self.maxMoveSpeed = 7
        self.moveSpeedInc = 8
        self.moveSpeedDecay = 7

        self.lock = threading.Lock()

        gun_frames = [f"shotgun_frame{i}" for i in range(5)]


    def SetupPlayer(self):
        #Setup UI
        ui_tex = textures.GetTexture("UI_Main")
        gun_tex = textures.GetTexture("shotgun_frame0")
        face_tex = textures.GetTexture("Doomhead")

        self.MainUI = create_ui_rect((-1,-1,0), (1,-0.6,0), ui_tex, uv_mode="stretch")

        self.Gun = create_ui_rect((-0.7,-0.6,0), (0.3,0.4,0), gun_tex, uv_mode="stretch")
        self.GunFrame = 0


        self.Face = create_ui_rect((-0.03,-0.98,0), (-0.19,-0.64,0), face_tex, uv_mode="stretch")
        self.FaceFrame = 0

        number_position = (-0.725,-0.83,0)
        number_width = 0.1
        number_height = 0.2
        number_offset = (0.1,0,0)

        

        self.Health = []
        for i in range(3):
            scalar = np.sign(i)
            temp_number_offset = tuple(x * scalar for x in number_offset)

            number_position = tuple(x + y for x, y in zip(number_position, temp_number_offset))
            self.Health.append(create_ui_rect(number_position, (number_position[0] + number_width, number_position[1] + number_height, 0), textures.GetTexture(f"{i}"), uv_mode="stretch"))


    def ToggleCanShoot(self):
        with self.lock:
            self.can_shoot = not self.can_shoot

    def RemoveUiElement(self, obj):
        with self.lock:
            if obj in objectManager.uiObjects:
                objectManager.uiObjects.remove(obj)
            else: 
                print(f"{obj} not found in the following list: {objectManager.uiObjects}")
    
    def ShotgunAnimation(self):
        time.sleep(0.5)
        while True:
            self.GunFrame = Wraparound(self.GunFrame + 1, 0, 2)

            self.Gun.texture = textures.GetTexture(f"shotgun_frame{self.GunFrame}")
            if self.GunFrame != 0:
                time.sleep(0.3)
                continue
            else:
                return
        #Wraparound

    def ShootWeapon(self):
        """Handle shooting logic, including raycasting and hit detection. Returns false if shooting was disabled, otherwise returns the result of the raycast (hit object or None)."""
        if self.can_shoot == False:
            return False

        self.can_shoot = False
        musicManager.PlaySound("Shotgun Sound")

        fire_tex = textures.GetTexture("shotgun_fireframe0")
        self.GunFire = create_ui_rect((-0.022,-0.22,0), (0.168,0.05,0), fire_tex, uv_mode="stretch")
        self.GunFireFrame = 0

        #run shotgun animation on another thread
        thread = threading.Thread(target= self.ShotgunAnimation)
        thread.start()

        timer = threading.Timer(0.5, self.RemoveUiElement, args=(self.GunFire,))
        timer.start()
        timer = threading.Timer(1.0, self.ToggleCanShoot)
        timer.start()


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

    def UpdatePlayerInformation(self):
        digits = [int(d) for d in f"{self.HP:03d}"]
        for i in range(3):
            self.Health[i].texture = textures.GetTexture(f"{digits[i]}")

    def Anounce(self, text, text_position=(-0.5, -0.5, 0), text_width_and_height=(0.1, 0.1, 0), lifetime_seconds=2.0, newline_spacing=0.1):
        start_text_position = text_position
        """Puts a doom text anouncement in the center of the screen for a short time. Used for things like "You got the shotgun!" or "Enemy Hit!"."""
        text = text.lower()

        true_i = 0
        for i in range(len(text)):
            char = text[i]

            if char is "\n":
                text_position = (start_text_position[0], text_position[1] - newline_spacing, text_position[2])
                true_i = 0
                continue
                

            char_tex = textures.GetTexture(char)

            


            char_pos = tuple(x + y for x, y in zip(text_position, (text_width_and_height[0] * true_i, 0, 0)))
            text_inverse_pos = (char_pos[0] + text_width_and_height[0], char_pos[1] + text_width_and_height[1], char_pos[2] + text_width_and_height[2])
            
            char_obj = create_ui_rect(char_pos, text_inverse_pos, char_tex, uv_mode="stretch")
            timer = threading.Timer(lifetime_seconds, self.RemoveUiElement, args=(char_obj,))
            timer.start()

            true_i += 1
    


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
        dt = doomTime.getDeltaTime()
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
        #camera.rotationX += mouse_dy * mouse_sensitivity

        # Clamp vertical look so you can't flip upside down
        if camera.rotationX > 90: camera.rotationX = 90
        if camera.rotationX < -90: camera.rotationX = -90
        

        playerController.MovePlayer(dt)

        hitObject = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    hitObject = playerController.ShootWeapon()

                if event.button == pygame.BUTTON_RIGHT:
                    levelManager.reload_level()

        if hitObject is not None:
            if hitObject is enemyPlayer:
                print("Enemy hit!")
                NetworkManager.enemyHit = True
            else:
                print("Hit something else:", hitObject)

        # Fallback: keep the cursor centered if relative mode isn't available.
        if (not self._relative_ok) and (self._center is not None):
            pygame.mouse.set_pos(self._center)
            pygame.mouse.get_rel()  # Flush any warp-induced delta.

        playerController.UpdatePlayerInformation()


inputManager = InputManager()


def Wraparound(value, minval, maxval) -> int:
    if value > maxval:
        return minval
    elif value < maxval:
        return maxval
    else:
        return value