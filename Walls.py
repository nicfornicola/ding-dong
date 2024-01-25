import pygame


class Wall:

    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
