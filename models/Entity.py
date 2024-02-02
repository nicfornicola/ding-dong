import pygame
from pygame.rect import Rect

from buttons.InfoBlock import InfoBlock


class Entity:

    def __init__(self, entityId, entityType, rect, coolDown):
        self.entityId = entityId
        self.entityType = entityType # good or bad
        self.rect: Rect = rect
        self.coolDown = coolDown
        self.isSelected = False
        self.lastAction = pygame.time.get_ticks()
        self.infoBlock = InfoBlock(None, None)
        self.bones = 5

    def getBaseStatsList(self):
        return [self.getEntityId(), self.getRect(), self.getCoolDown(), self.getBones()]

    def setSellBlock(self, sellBlock):
        self.infoBlock.sellBlock = sellBlock

    def setStatBlock(self, block):
        self.infoBlock.statBlock = block

    def canDoAction(self):
        # fire gun, only if cooldown has been 0.3 seconds since last
        return pygame.time.get_ticks() - self.lastAction >= self.coolDown

    def setRect(self, rect):
        self.rect = rect

    def getEntityId(self):
        return "Id: " + str(self.entityId)

    def getEntityType(self):
        return "Type: " + str(self.entityType)

    def getBones(self):
        return "Bones: " + str(self.bones)

    def getRect(self):
        if self.rect:
            return "Rect: X " + str(self.rect.x) + ", Y " + str(self.rect.y)
        else:
            return "Rect: X -, Y -"


    def getFullRect(self):
        return self.getRect() + ", W " + str(self.rect.width) + ", H " + str(self.rect.height)

    def getCoolDown(self):
        if self.entityType == "good":
            return "Fire Rate: " + str(self.coolDown)
        elif self.entityType == "bad":
            return "Speed: " + str(self.coolDown)

    def getLastAction(self):
        return "lastAction: " + str(self.entityId)

    def __eq__(self, other):
        return self.entityId == other.entityId
