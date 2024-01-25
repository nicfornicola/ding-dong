from pygame import Rect

from models.GoodGuy import GoodGuy
from buttons.Button import Button


class BuyButton(Button):
    def __init__(self, buttonId, buttonType, towerType, img, rect):
        super().__init__(buttonId, buttonType, img, rect)
        self.goodGuy = GoodGuy(-1, "good", towerType, None, 20, 500)

