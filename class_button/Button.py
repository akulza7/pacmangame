import pygame
from class_button.button import Button as InternalButton
pygame.font.init()


class Button():

    BUTTON_STYLE = {
        "hover_color": pygame.Color('blue'),
        "clicked_color": pygame.Color('green'),
        "clicked_font_color": pygame.Color('black'),
        "hover_font_color": pygame.Color('orange'),
        "font": pygame.font.Font(None, 40),
        "font_color": pygame.Color("black")
    }

    def __init__(self, x, y, width, height, title, action):
        self.internal_button = InternalButton(
            pygame.Rect(x, y, width, height),
            pygame.Color('gray'), action,
            **self.BUTTON_STYLE,
            text=title)

    def event(self, event):
        self.internal_button.check_event(event)

    def draw(self, screen):
        self.internal_button.update(screen)
