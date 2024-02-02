import pygame

from models.Entity import Entity


class BadGuy(Entity):
    def __init__(self, badGuyType, spawnTime=None, entityId=None, hp=None, color=None, coolDown=None):
        super().__init__(entityId, "bad", pygame.Rect(-20, -20, 20, 20), coolDown)
        self.badGuyType = badGuyType
        self.color = color
        self.hp = hp
        self.spawnTime = spawnTime
        self.setBadGuy()

        self.canSpawn = False
        self.currentIndex = 0
        self.isAlive = True

    def getSelectedStats(self):
        return self.getBaseStatsList() + [self.getBadGuyType(),
                                          self.getHp(),
                                          self.getSpawnTime(),
                                          self.getIsAlive()]

    def switchCanSpawn(self):
        self.canSpawn = not self.canSpawn

    def copyBadGuy(self):
        return BadGuy(self.badGuyType,
                      hp=self.hp,
                      color=self.color,
                      coolDown=self.coolDown)

    def getCurrentIndex(self):
        return "Current Index: " + str(self.currentIndex)

    def getBadGuyType(self):
        return "Type: " + str(self.badGuyType)

    def getHp(self):
        return "HP: " + str(self.hp)

    def getSpawnTime(self):
        return "SpawnTime: " + str(self.spawnTime)

    def getIsAlive(self):
        if self.isAlive:
            return "Status: Alive"
        return "Status: Dead"

    def addToCurrentIndex(self):
        self.currentIndex += 1
        return self.currentIndex

    def setBadGuyStats(self, color, hp, coolDown):
        self.color = color
        self.hp = hp
        self.coolDown = coolDown

    def setBadGuy(self):
        if self.badGuyType == 1:
            self.setOne()
        elif self.badGuyType == 2:
            self.setTwo()
        elif self.badGuyType == 3:
            self.setThree()

    def setOne(self):
        self.setBadGuyStats([59, 255, 103], 300, 50) # Green

    def setTwo(self):
        self.setBadGuyStats([59, 103, 255], 255, 10) # Blue

    def setThree(self):
        self.setBadGuyStats([255, 59, 241], 255, 70) # Pink

    def __str__(self) -> str:
        return "entityId=" + str(self.entityId) +\
            " badGuyType=" + str(self.badGuyType) +\
            " rect=" + str(self.rect) + \
            " coolDown=" + str(self.coolDown) +\
            " color=" + str(self.color) +\
            " currentIndex=" + str(self.currentIndex) +\
            " hp=" + str(self.hp) +\
            " isAlive=" + str(self.isAlive)

    def isTypeEqual(self, otherList):
        for other in otherList:
            if self.badGuyType == other.badGuyType:
                return True

        return False



