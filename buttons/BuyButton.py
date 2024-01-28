from pygame import Rect

from models.GoodGuy import GoodGuy
from buttons.Button import Button


class BuyButton(Button):
    def __init__(self, buttonFunction, towerType, rect, img):
        super().__init__(buttonFunction, rect, img)
        self.goodGuy = GoodGuy(towerType)

    def __str__(self) -> str:
        return super.__str__(self) + str(self.goodGuy)

