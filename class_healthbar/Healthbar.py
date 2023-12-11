import pygame


class Healthbar():
    image = pygame.transform.scale(pygame.image.load(
        'class_healthbar/heart.png'), (45, 45))

    def __init__(self):
        self.health = None
        self.rects = []

    def reset(self):
        self.rects = [
            pygame.Rect(890, 0, 45, 45),
            pygame.Rect(845, 0, 45, 45),
            pygame.Rect(800, 0, 45, 45)
        ]

    def decrease(self):
        self.rects.pop()

    def draw(self, screen):
        for rect in self.rects:
            screen.blit(self.image, rect)
