import pygame
class Time:
    def __init__(self):
        self.dt = 0
        self.FRAMERATE_CAP = None
        self.clock = None

    def initTime(self, FRAMERATE_CAP):
        self.clock = pygame.time.Clock()

        self.FRAMERATE_CAP = FRAMERATE_CAP

    def updateDeltaTime(self):
        dt_ms = self.clock.tick(self.FRAMERATE_CAP)
        self.dt = dt_ms / 1000.0

    def getDeltaTime(self):
        return self.dt

time = Time()