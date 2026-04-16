import os

import pygame


class MusicManager:
    def __init__(self, MusicVolume, SFXVolume, VoiceVolume):
        self.preloadedAudio = {}

        self.MusicVolume = MusicVolume
        self.SFXVolume = SFXVolume
        self.VoiceVolume = VoiceVolume

        pygame.mixer.init()

        path = os.path.join("Assets", "Audio", "Music", "MainTheme.mp3")
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(MusicVolume)

    def AddPreloadedMusic(self, path, alias):
        try:
            self.preloadedAudio[alias] = pygame.mixer.Sound(path)
        except FileNotFoundError:
            print(f"Unable to load audio file: {path}")
        except (KeyError, AttributeError):
            print(f"Unable to register audio file: {path}")

    def PreloadMusic(self):
            self.AddPreloadedMusic(os.path.join("Assets", "Audio", "SFX", "shotgun.mp3"), "Shotgun Sound")


    def PlaySound(self, alias):
        if alias in self.preloadedAudio:
            sound = self.preloadedAudio[alias]

            # Set the volume
            sound.set_volume(self.SFXVolume)
            sound.play()
        else:
            print(f"Alias '{alias}' not found in preloaded audio.")




musicManager = MusicManager(0.3, 1, 1)
