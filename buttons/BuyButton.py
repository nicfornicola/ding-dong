import pygame

from buttons.Button import Button
from models.GoodGuy import GoodGuy


class BuyButton(Button):
    def __init__(self, buttonFunction, towerType, rect, img):
        super().__init__(buttonFunction, rect, img)
        self.goodGuy = GoodGuy(towerType)
        self.buttonImgList = img

    def __str__(self) -> str:
        return super().__str__() + " " + str(self.goodGuy)

