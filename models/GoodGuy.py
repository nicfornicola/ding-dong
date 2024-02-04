import pygame

from models.BadGuy import BadGuy
from models.Entity import Entity
from util.Util import isInside, dis

class GoodGuy(Entity):
    def __init__(self, towerType, entityId=-1, color=None, rect=None, rangeRad=None, coolDown=None, damage=None, targetingMethod=None, fullCopy=True):
        super().__init__(entityId, "good", rect, coolDown)
        self.towerType = towerType
        self.color = color
        self.items = []
        self.fireRate = 0
        self.damage = damage
        self.currentTarget = None
        self.targetingMethod = targetingMethod
        self.targetingMethods = ["First", "Last", "Strongest", "Closest"]
        self.rangeRad = rangeRad
        self.inRangeList: list[BadGuy] = []
        self.totalDamageDone = 0
        self.sellSpot = None
        self.switchedMethod = False
        self.count = 0
        self.setGoodGuy(fullCopy)

    def getSelectedStats(self):
        return ([self.getTowerType()] +
                 self.getBaseStatsList() +
                [self.getDamage(),
                 self.getItems(),
                 self.getCurrentTarget(),
                 self.getTargetingMethod(),
                 self.getInRangeList()])

    def getInRangeList(self):
        strList = []
        for badGuy in self.inRangeList:
            strList.append(str(badGuy.entityId))
        return "In Range: " + str(strList)

    def getTowerType(self):
        return "Tower Type: " + str(self.towerType)

    def getTotalDamage(self):
        return "Dmg Done: " + str(self.totalDamageDone)

    def getRangeRad(self):
        return "Range: " + str(self.rangeRad)

    def getItems(self):
        return "Items: " + str(self.items)

    def getFireRate(self):
        return "Fire Rate: " + str(self.fireRate)

    def getDamage(self):
        return "Dmg: " + str(self.damage) + " (" + str(self.totalDamageDone) + ")"

    def getCurrentTarget(self):
        if self.currentTarget is None:
            return "Current Target: None"
        return "Current Target: " + str(self.currentTarget.entityId)

    def getTargetingMethod(self):
        return "Targeting Method: " + str(self.targetingMethod) + " >>"

    def setCurrentTarget(self, badGuy:BadGuy) -> None:
        self.currentTarget = badGuy

    def setGoodGuyStats(self, color, damage, bones, rangeRad, coolDown, rect=None):
        if rect is None:
            rect = pygame.Rect(0, 0, 15, 15)
        self.rect = rect
        self.rect.center = pygame.mouse.get_pos()
        self.color = color
        self.rangeRad = rangeRad
        self.coolDown = coolDown
        self.damage = damage
        self.targetingMethod = "First"
        self.bones = bones
        return self

    def setGoodGuy(self, fullCopy):
        if fullCopy:
            if self.towerType == "green":
                return self.setGoodGuyStats("green", damage=5, bones=2, rangeRad=150, coolDown=500)
            elif self.towerType == "blue":
                return self.setGoodGuyStats("blue", damage=1, bones=5, rangeRad=80, coolDown=100)
            elif self.towerType == "purple":
                return self.setGoodGuyStats("purple", damage=15, bones=8, rangeRad=300, coolDown=1000)
            elif self.towerType == "yellow":
                return self.setGoodGuyStats("yellow", damage=1, bones=15, rangeRad=150, coolDown=700)
            elif self.towerType == "black":
                return self.setGoodGuyStats("black", damage=15, bones=8, rangeRad=300, coolDown=1000)
            elif self.towerType == "orange":
                return self.setGoodGuyStats("orange", damage=15, bones=8, rangeRad=300, coolDown=1000)
            elif self.towerType == "brown":
                return self.setGoodGuyStats("brown", damage=15, bones=8, rangeRad=300, coolDown=1000)
            elif self.towerType == "pink":
                return self.setGoodGuyStats("pink", damage=15, bones=8, rangeRad=300, coolDown=1000)

    def copyGoodGuy(self, entityID):
        return GoodGuy(self.towerType, entityId=entityID)


    # Go through the loop of methods
    def handleTargetingMethodChange(self):
        self.switchedMethod = True
        index = self.targetingMethods.index(self.targetingMethod)
        self.targetingMethod = self.targetingMethods[0] if index + 1 == len(self.targetingMethods) else \
                               self.targetingMethods[index + 1]

    def findClosestTarget(self, inRangeList: list[BadGuy]) -> BadGuy | None:
        newTarget = None
        for badGuy in inRangeList:
            if newTarget is None or dis(badGuy, self) < dis(newTarget, self):
                newTarget = badGuy

        return newTarget

    def inRange(self, badGuy):
        return isInside(badGuy.rect.center, self)

    def updateInRangeList(self, badGuyList):
        for badGuy in badGuyList:
            inRange = self.inRange(badGuy)
            # Remove from range list if not inRange or isDead
            if badGuy in self.inRangeList and (not inRange or not badGuy.isAlive):
                self.inRangeList.remove(badGuy)
            # Append to range list if not already in list inRange and isAlive
            elif badGuy not in self.inRangeList and inRange and badGuy.isAlive:
                self.inRangeList.append(badGuy)


    # sets the currentTarget from the list of badGuys
    def findTarget(self, pool):
        self.updateInRangeList(pool.badGuyList)

        if not pool.anyAlive or (self.currentTarget and not self.currentTarget.isAlive):
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

    def dealDamage(self, currentTarget):
        currentTarget.hp -= self.damage
        self.totalDamageDone += self.damage

    def damageNextClosest(self, currentTarget, bounces, badGuyList, alreadyHitList):
        # If run out of bounces or if no more targets then return
        if bounces == 0 or currentTarget is None:
            return []
        else:
            # Do damage to the next guy
            self.dealDamage(currentTarget)
            # Add currentTarget to list so we don't hit again
            alreadyHitList.append(currentTarget)
            # Find nextTarget to send to the slammer
            nextTarget = findClosestLightningTarget(badGuyList, alreadyHitList)
            # Call next iteration with one less bounce
            return [currentTarget] + self.damageNextClosest(nextTarget, bounces-1, badGuyList, alreadyHitList)

    def lightingTargets(self, world):
        return self.damageNextClosest(self.currentTarget, 5, world.pool.badGuyList, [])


    def shootTarget(self, world):
        # If we have a current target then shoot else do nothing
        if self.currentTarget:
            self.lastAction = pygame.time.get_ticks()

            if self.towerType == "yellow":
                return self.lightingTargets(world)
            else:
                return [self.dealDamage(self.currentTarget)]

        else:
            return False

    def __str__(self) -> str:
        return "entityId=" + str(self.entityId) +\
                " entityType=" + str(self.entityType) + \
                " towerType=" + str(self.towerType) + \
                " color=" + str(self.color) + \
                " rect=" + str(self.rect) +\
                " radRange=" + str(self.rangeRad) +\
                " coolDown=" + str(self.coolDown) + \
                " damage=" + str(self.damage) + \
                " targetingMethod=" + str(self.targetingMethod) + \
                " items=" + str(self.items) + \
                " fireRate=" + str(self.fireRate) +\
                " inRangeList=" + str(self.inRangeList) +\
                " totalDamageDone=" + str(self.totalDamageDone) +\
                " currentTarget=" + str(self.currentTarget)


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

def findClosestLightningTarget(badGuyList, alreadyHitList) -> BadGuy | None:
    lastHitGuy = alreadyHitList[-1]
    newTarget = None
    # Go through the list and find the next badGuy that hasn't been hit and is not dead or the lastHitGuy
    for badGuy in badGuyList:
        if badGuy.isAlive and badGuy is not newTarget and isInside(badGuy.rect.center, lastHitGuy, 30) and badGuy not in alreadyHitList:
            # Do this only on the first qualified guy to set a baseline
            if newTarget is None:
                newTarget = badGuy
                continue

            if dis(badGuy, lastHitGuy) < dis(newTarget, lastHitGuy):
                newTarget = badGuy

    if newTarget is lastHitGuy:
        return None

    return newTarget

