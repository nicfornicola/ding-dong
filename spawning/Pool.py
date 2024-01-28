from numpy import array

from models.BadGuy import BadGuy


class Pool:

    def __init__(self, poolType):
        self.poolType = poolType
        self.badGuyList:list = []
        self.goodGuyList:list = []
        self.anyAlive = True
        self.levelOne = []
        self.numOfBadGuyTypes = []
        self.goodGuyNextId = 1
        self.badGuyNextId = 1

    # Add the lists together and return
    def getGuyLists(self):
        return self.goodGuyList + self.badGuyList

    def badGuyFactory(self, numOfBadGuys, badGuyType, spawnTime, spawnDifference):
        self.numOfBadGuyTypes.append(numOfBadGuys)
        for i in range(numOfBadGuys):
            self.addBadGuy(BadGuy(badGuyType, spawnTime+(spawnDifference*i), entityId=len(self.badGuyList)+1))

    # add getting money back later and animation to move guy back to wallet
    def sellGoodGuy(self, entityId):
        for goodGuy in self.goodGuyList:
            if goodGuy.entityId == entityId:
                self.goodGuyList.remove(goodGuy)

    def addGoodGuy(self, goodGuy):
        self.goodGuyList.append(goodGuy)

    def addBadGuy(self, badGuy):
        self.badGuyList.append(badGuy)

    def addBadGuyList(self, guyList, reset=None):
        if reset:
            self.badGuyList = []
        self.badGuyList += guyList

    def updateAllDead(self):
        for badGuy in self.badGuyList:
            if badGuy.isAlive:
                self.anyAlive = True
                return

        self.anyAlive = False

