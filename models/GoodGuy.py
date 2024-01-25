import pygame

from models.Entity import Entity
from models.BadGuy import BadGuy
from util.Util import isInside, dis

class GoodGuy(Entity):
    def __init__(self, entityId, entityType, color, rect, rangeRad, coolDown, damage=None, targetingMethod=None):
        super().__init__(entityId, entityType, rect, coolDown)
        self.color = color
        self.items = []
        self.fireRate = 0
        self.damage = damage
        self.currentTarget = None
        self.targetingMethod = targetingMethod
        self.targetingMethods = ["First", "Last", "Strongest", "Closest"]
        self.rangeRad = rangeRad
        self.targetingMethodChanged = False
        self.inRangeList: list[BadGuy] = []

    def getInRangeList(self):
        strList = []
        for badGuy in self.inRangeList:
            strList.append(str(badGuy.entityId))
        return "In Range: " + str(strList)

    def getRangeRad(self):
        return "Range: " + str(self.rangeRad)

    def getItems(self):
        return "Items: " + str(self.items)

    def getFireRate(self):
        return "Fire Rate: " + str(self.fireRate)

    def getDamage(self):
        return "Damage: " + str(self.damage)

    def getCurrentTarget(self):
        if self.currentTarget is None:
            return "Current Target: None"
        return "Current Target: " + str(self.currentTarget.entityId)

    def getTargetingMethod(self):
        return "Targeting Method: " + str(self.targetingMethod)

    def setCurrentTarget(self, badGuy:BadGuy) -> None:
        self.currentTarget = badGuy

    def inRange(self, badGuy):

        return isInside(badGuy.rect.centerx, badGuy.rect.centery, self)

    def findClosestTarget(self, inRangeList: list[BadGuy]) -> BadGuy | None:
        newTarget = None
        for badGuy in inRangeList:
            if newTarget is None or dis(badGuy, self) < dis(newTarget, self):
                newTarget = badGuy

        return newTarget

    # sets the currentTarget from the list of badGuys
    def findTarget(self, pool):
        if not pool.anyAlive or self.currentTarget and not self.currentTarget.isAlive:
            self.currentTarget = None

        match self.targetingMethod:
            case "First":
                self.currentTarget = findFirstTarget(self.inRangeList)
            case "Last":
                self.currentTarget = findLastTarget(self.inRangeList)
            case "Strongest":
                self.currentTarget = findStrongestTarget(self.inRangeList)
            case "Closest":
                self.currentTarget = self.findClosestTarget(self.inRangeList)
            case _:
                print("bad targetingMethod")

    def shootTarget(self, pool) -> bool:
        # If we have a current target then shoot else do nothing
        if self.currentTarget:
            self.currentTarget.hp -= self.damage
            self.currentTarget.color = [rgb - self.damage for rgb in self.currentTarget.color]

            if self.currentTarget.hp <= 0:
                self.currentTarget.isAlive = False
                self.currentTarget.color = "red"
                pool.updateAllDead()
            else:
                for i in range(len(self.currentTarget.color)):
                    self.currentTarget.color[i] -= self.damage
                    if self.currentTarget.color[i] < 0:
                        self.currentTarget.color[i] = 0

            self.lastAction = pygame.time.get_ticks()
            return True
        else:
            return False

    def setGoodGuyStats(self, color, rangeRad, coolDown, damage, targetingMethod, x=None, y=None ):
        posX, posY = pygame.mouse.get_pos()
        self.rect = pygame.Rect(posX, posY, 15, 15)
        self.color = color
        self.rangeRad = rangeRad
        self.coolDown = coolDown
        self.damage = damage
        self.targetingMethod = targetingMethod
        return self


    def setGoodGuy(self):
        if self.color == "green":
            self.setGreen()
        elif self.color == "blue":
            self.setBlue()
        elif self.color == "purple":
            self.setPurple()
        return self

    def setBlue(self):
        self.setGoodGuyStats("blue", 80, 100, 1, "First")

    def setGreen(self):
        self.setGoodGuyStats("green", 150, 500, 2, "First")

    def setPurple(self):
        self.setGoodGuyStats("purple", 300, 1000, 15, "First")

    def copyGoodGuy(self, entityId):
        return GoodGuy(entityId,
                       self.entityType,
                       self.color,
                       self.rect,
                       self.rangeRad,
                       self.coolDown,
                       self.damage,
                       self.targetingMethod)

    def __str__(self) -> str:
        return "entityType=" + str(self.entityType) +\
                " rect=" + str(self.rect) +\
                " coolDown=" + str(self.coolDown) +\
                " color=" + str(self.color) + \
                " items=" + str(self.items) + \
                " fireRate=" + str(self.fireRate) +\
                " damage=" + str(self.damage) +\
                " currentTarget=" + str(self.currentTarget) +\
                " targetingMethod=" + str(self.targetingMethod)

##################### Static functions ###############################

def findFirstTarget(inRangeList: list[BadGuy]) -> BadGuy | None:
    newTarget = None
    for badGuy in inRangeList:
        # Set newTarget for baseline or if badGuy is further than newTarget, make badGuy the newTarget
        if newTarget is None or badGuy.currentIndex > newTarget.currentIndex:
            newTarget = badGuy

    return newTarget

def findLastTarget(inRangeList: list[BadGuy]) -> BadGuy | None:
    newTarget = None
    for badGuy in inRangeList:
        # Set newTarget for baseline or if badGuy is closer than newTarget, make badGuy the newTarget
        if newTarget is None or badGuy.currentIndex < newTarget.currentIndex:
            newTarget = badGuy

    return newTarget

def findStrongestTarget(inRangeList: list[BadGuy]) -> BadGuy | None:
    newTarget = None
    for badGuy in inRangeList:
        # Set newTarget for baseline or if badGuy is stronger than newTarget, make badGuy the newTarget
        if newTarget is None or badGuy.hp > newTarget.hp:
            newTarget = badGuy

    return newTarget


