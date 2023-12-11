import pygame

class Area:
    def __init__(self):
        self.map = None

    def check_corns(self):
        for row in self.map:
            if 2 in row or 3 in row:
                return False
        return True

    def updateMap(self, map):
        self.map = map

    def draw(self, screen):
        for i in range(20):
            for j in range(21):
                if self.map[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 255),
                                     [j*45, i*45, 45, 45])
                elif self.map[i][j] == 2:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     [j*45, i*45, 45, 45])
                    pygame.draw.circle(screen, (255, 168, 175),
                                       [j*45+23, i*45+23], 4.5, 0)

                elif self.map[i][j] == 3:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     [j*45, i*45, 45, 45])
                    pygame.draw.circle(screen, (255, 168, 175),
                                       [j*45+23, i*45+23], 13, 0)
                else:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     [j*45, i*45, 45, 45])
