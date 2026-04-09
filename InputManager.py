import pygame
import sys


class InputManager:
    def __init__(self):
        pygame.init()

    def pollInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            print("\nUser Quit")
            sys.exit(0)

inputManager = InputManager()