import pygame


class Text:
    def __init__(self, position, text, size, color, width=0, height=0):
        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont('Courier New', self.size, True, False)
        self.rect = pygame.rect.Rect(position[0], position[1], width, height)
        self.texture = None

    def render(self):
        self.texture = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.texture, self.rect)


class RecalculableText(Text):
    def __init__(self, position, text, size, color, width=0, height=0):
        super().__init__(position, text, size, color, width, height)
        self.text_format = self.text

    def recreate_text(self, *args, **kwargs):
        self.text = self.text_format.format(*args, **kwargs)
        self.render()
