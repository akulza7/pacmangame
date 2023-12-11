import pygame
import datetime
import random


class Ghost(pygame.sprite.Sprite):
    IMAGE = pygame.image.load('class_ghost/ghost_images.png')

    def __init__(self, position, crop_regions):
        super(Ghost, self).__init__()
        self.surfaces = {
            "left": self.IMAGE.subsurface(crop_regions["left"]),
            "right": self.IMAGE.subsurface(crop_regions["right"]),
            "up": self.IMAGE.subsurface(crop_regions["up"]),
            "down": self.IMAGE.subsurface(crop_regions["down"]),
            "scared": self.IMAGE.subsurface(crop_regions["scared"]),
            "semiscared": self.IMAGE.subsurface(crop_regions["semiscared"])
        }
        self.surface = None
        self.mask = None
        self.direction = None
        self.newdirection = None
        self.rect = pygame.Rect(position[0]*45, position[1]*45, 45, 45)
        self.scared = False
        self.invisible = False
        self.dissapear_time = None
        self.INITIALPOS = position

    def respawn(self):
        position = self.INITIALPOS
        self.rect = pygame.Rect(position[0]*45, position[1]*45, 45, 45)
        self.direction = "right"
        self.reset()
        self.change_sprite()
        self.mask = pygame.mask.from_surface(self.surface)

    def change_sprite(self, scaremode_seconds=None):
        if (self.scared == True):
            if scaremode_seconds < 6:
                self.surface = self.surfaces["scared"]
            else:
                self.surface = self.surfaces["semiscared"]
        else:
            self.surface = self.surfaces[self.direction]
        self.surface = pygame.transform.scale(self.surface, (45, 45))

    def draw(self, screen):
        if self.invisible == False:
            screen.blit(self.surface, self.rect)

    def collision_wall(self, direction, map):
        shift = {
            "left": [-1, 0],
            "right": [1, 0],
            "up": [0, -1],
            "down": [0, 1],
            "stand": [0, 0]
        }
        newRect = pygame.Rect(self.rect)
        newRect.x += shift[direction][0]*9
        newRect.y += shift[direction][1]*9
        for i in range(len(map)):
            for j in range(len(map[i])):
                if (map[i][j] == 1 and newRect.colliderect(pygame.Rect(45*j, 45*i, 45, 45))):
                    return 1
        return 0

    def reset(self):
        self.scared = False
        self.invisible = False

    def respawn_timer_logic(self, max_respawn_seconds=3):
        now = datetime.datetime.now()
        seconds = (now - self.dissapear_time).seconds
        if (seconds == max_respawn_seconds):
            self.respawn()

    def random_direction(self, directions):
        return directions[random.randint(0, len(directions)-1)]

    def eaten(self):
        self.dissapear_time = datetime.datetime.now()
        self.invisible = True

    def move(self):
        delta_x, delta_y = 0, 0
        if self.direction == "down":
            delta_y = 9
        elif self.direction == "up":
            delta_y = -9
        elif self.direction == "left":
            delta_x = -9
        elif self.direction == "right":
            delta_x = 9
        self.rect.x += delta_x
        self.rect.y += delta_y

    def dirchange_logic(self, map):
        y, x = self.rect.y//45, self.rect.x//45
        bools = {
            "right": map[y][x+1] in [0, 2, 3] and self.direction != "right",
            "left": map[y][x-1] in [0, 2, 3] and self.direction != "left",
            "up": map[y-1][x] in [0, 2, 3] and self.direction != "up",
            "down": map[y+1][x] in [0, 2, 3] and self.direction != "down"
        }
        available = [None, None, None, None]
        directions = ["right", "left", "up", "down"]
        for i in range(4):
            if bools[directions[i]]:
                available[i] = directions[i]
        if available[0] and self.direction == "left" and not self.collision_wall(self.direction, map):
            available[0] = None
        if available[1] and self.direction == "right" and not self.collision_wall(self.direction, map):
            available[1] = None
        if available[2] and self.direction == "down" and not self.collision_wall(self.direction, map):
            available[2] = None
        if available[3] and self.direction == "up" and not self.collision_wall(self.direction, map):
            available[3] = None
        self.newdirection = self.random_direction(available)

    def logic(self, scaremode_activated, scaremode_status, map, scaremode_seconds):
        if self.invisible == True:
            self.respawn_timer_logic()
        if scaremode_activated == True and self.scared == False:
            self.scared = True
        if scaremode_status == False and self.scared == True:
            self.scared = False
        else:
            if self.rect.x % 45 == 0 and self.rect.y % 45 == 0:
                if self.rect.y == 270 and self.rect.x == 450 and (self.direction == "left" or self.direction == "right"):
                    self.newdirection = "up"
                else:
                    self.dirchange_logic(map)
            if self.newdirection != self.direction and self.newdirection != None:
                if not self.collision_wall(self.newdirection, map):
                    self.direction = self.newdirection
            self.change_sprite(scaremode_seconds)
            if not self.collision_wall(self.direction, map):
                self.move()
            else:
                self.newdirection = self.random_direction(
                    ["left", "right", "up", "down"])
