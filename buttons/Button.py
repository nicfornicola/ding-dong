from pygame.locals import *

class Button:
    def __init__(self, buttonFunction, img, rect):
        self.buttonFunction = buttonFunction # buy, play,
        self.rect: Rect = rect
        self.img = img

    def __str__(self) -> str:
        return "buttonFunction: " + self.buttonFunction+\
               " rect: " + str(self.rect)+\
               " img: " + str(self.img)


