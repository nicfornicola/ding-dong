import pygame
from pygame.rect import Rect


class Entity:

    def __init__(self, entityId, entityType, rect, coolDown):
        self.entityId = entityId
        self.entityType = entityType
        self.rect: Rect = rect
        self.coolDown = coolDown
        self.lastAction = pygame.time.get_ticks()

    def canDoAction(self):
        # fire gun, only if cooldown has been 0.3 seconds since last
        return pygame.time.get_ticks() - self.lastAction >= self.coolDown

    def setRect(self, rect):
        self.rect = rect

    def getEntityId(self):
        return "Id: " + str(self.entityId)

    def getEntityType(self):
        return "Type: " + str(self.entityType)

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
