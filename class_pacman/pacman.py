import pygame


class Pacman(pygame.sprite.Sprite):
    IMAGES = {
        "up": [
            pygame.image.load(
                "class_pacman/images/pacman_leftup_opened.png"),
            pygame.image.load(
                "class_pacman/images/pacman_leftup_half.png"),
            pygame.image.load(
                "class_pacman/images/pacman_leftup_quarter.png"),
            pygame.image.load(
                "class_pacman/images/pacman_leftup_closed.png"),
            pygame.image.load(
                "class_pacman/images/pacman_rightup_opened.png"),
            pygame.image.load(
                "class_pacman/images/pacman_rightup_half.png"),
            pygame.image.load(
                "class_pacman/images/pacman_rightup_quarter.png"),
            pygame.image.load(
                "class_pacman/images/pacman_rightup_closed.png")
        ],
        "down": [
            pygame.image.load(
                "class_pacman/images/pacman_leftdown_opened.png"),
            pygame.image.load(
                "class_pacman/images/pacman_leftdown_half.png"),
            pygame.image.load(
                "class_pacman/images/pacman_leftdown_quarter.png"),
            pygame.image.load(
                "class_pacman/images/pacman_leftdown_closed.png"),
            pygame.image.load(
                "class_pacman/images/pacman_rightdown_opened.png"),
            pygame.image.load(
                "class_pacman/images/pacman_rightdown_half.png"),
            pygame.image.load(
                "class_pacman/images/pacman_rightdown_quarter.png"),
            pygame.image.load(
                "class_pacman/images/pacman_rightdown_closed.png")
        ],
        "left": [
            pygame.image.load(
                "class_pacman/images/pacman_left_opened.png"),
            pygame.image.load("class_pacman/images/pacman_left_half.png"),
            pygame.image.load(
                "class_pacman/images/pacman_left_quarter.png"),
            pygame.image.load("class_pacman/images/pacman_left_closed.png")
        ],
        "right": [
            pygame.image.load(
                "class_pacman/images/pacman_right_opened.png"),
            pygame.image.load("class_pacman/images/pacman_right_half.png"),
            pygame.image.load(
                "class_pacman/images/pacman_right_quarter.png"),
            pygame.image.load(
                "class_pacman/images/pacman_right_closed.png")
        ]
    }

    def __init__(self, rarefaction_rate=2):
        self.health = None
        self.image = None
        self.mask = None
        self.direction = None
        self.rarefaction = 0
        self.rarefaction_rate = rarefaction_rate
        self.frames_order = None
        self.frame = None
        self.scaremode_eaten = None
        self.pos = None
        self.mapPos = None
        self.rect = None

    def set_health(self, number):
        self.health = number

    def get_health(self):
        return self.health

    def respawn(self, position, mapPos):
        self.pos = position
        self.mapPos = mapPos
        self.direction = "left"
        self.frame = 0
        self.frames_order = [3, 2, 1, 0, 1, 2]
        self.change_sprite(self.direction, self.frame)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 45, 45)
        self.mask = pygame.mask.from_surface(self.image)
        self.scaremode_eaten = 0
        self.rarefaction = 0

    def change_sprite(self, direction, frame):
        self.image = self.IMAGES[direction][frame]

    def collision_ghost(self, ghost):
        if ghost.invisible == False:
            if pygame.sprite.spritecollide(self, pygame.sprite.Group(ghost), False, pygame.sprite.collide_mask):
                if ghost.scared == False:
                    return 2
                else:
                    ghost.eaten()
                    return 1
            else:
                return 0

    def collision_corn(self, map):
        position = self.mapPos
        if map[position[1]][position[0]] == 2:
            map[position[1]][position[0]] = 0
            return 1, map
        elif map[position[1]][position[0]] == 3:
            map[position[1]][position[0]] = 0
            return 2, map
        else:
            return 0, map

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

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        if (self.direction == "left"):
            self.pos[0] -= 9

        if (self.direction == "right"):
            self.pos[0] += 9

        if (self.direction == "up"):
            self.pos[1] -= 9

        if (self.direction == "down"):
            self.pos[1] += 9

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if (self.pos[0] % 45 == 0):
            self.mapPos[0] = self.pos[0]//45
        if (self.pos[1] % 45 == 0):
            self.mapPos[1] = self.pos[1]//45

    def logic(self, map, ghosts, scaremode_status=False, direction=None):
        score = 0
        self.rarefaction = (self.rarefaction+1) % 2

        if (scaremode_status == False):
            self.scaremode_eaten = 0

        for ghost in ghosts:
            statement = self.collision_ghost(ghost)
            if (statement == 2):
                score = -100000
            elif (statement == 1):
                score = 200 * 2**self.scaremode_eaten
                self.scaremode_eaten += 1

        corn, map = self.collision_corn(map)
        scaremode = False
        if (corn == 2):
            score += 50
            scaremode = True
        if (corn == 1):
            score += 10

        if direction != self.direction and direction != None:
            if not self.collision_wall(direction, map):
                if self.direction == "right" and \
                        (direction == "up" or direction == "down"):
                    self.frames_order = [7, 6, 5, 4, 5, 6]
                else:
                    self.frames_order = [3, 2, 1, 0, 1, 2]
                self.direction = direction

        if not self.collision_wall(self.direction, map):
            if self.rarefaction % self.rarefaction_rate == 0:
                self.frame = (self.frame+1) % 6
            self.change_sprite(self.direction, self.frames_order[self.frame])
            self.move()

        return score, scaremode, map
