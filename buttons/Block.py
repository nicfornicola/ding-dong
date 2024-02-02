from pygame.locals import *

class Block:

    def __init__(self, rect, rectList):
        self.rect: Rect = rect
        self.rectList: list = rectList
        self.currentPaddingHeight = self.rect.y
        self.currentPaddingWidth = self.rect.x
        self.maxWidth = 0
        self.maxHeight = 0







