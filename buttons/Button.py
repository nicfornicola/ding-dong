import pygame
from pygame.locals import *

class Button:

    def __init__(self, buttonId, buttonType, img, rect):
        self.buttonId = buttonId
        self.buttonType = buttonType
        self.rect: Rect = rect
        self.show = True
        self.img = img




