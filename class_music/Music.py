import pygame

class Music():
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('class_music/soundtrack.ogg')

    def play(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

