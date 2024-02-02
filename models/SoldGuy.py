from pygame import Rect

from models.GoodGuy import GoodGuy


class SoldGuy(GoodGuy):
    def __init__(self, goodGuy):
        super().__init__(goodGuy.towerType, goodGuy.entityId, goodGuy.color, goodGuy.rect, fullCopy=False)
        self.sellSpot: Rect = goodGuy.rect.copy()
        self.shadow: Rect = goodGuy.rect.copy()
        self.shadowHeight = 0
        self.frameCounter = 0
        self.path = []
        self.index = 0
        self.landed = False
        self.inflateShadow()

    def inflateShadow(self):
        self.shadow.inflate_ip(1,1)


