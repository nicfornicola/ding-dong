from models.BadGuy import BadGuy


class Pool:

    def __init__(self, poolType):
        self.poolType = poolType
        self.badGuyList:list = []
        self.goodGuyList:list = []
        self.anyAlive = True
        self.numOfBadGuysThrough = 0
        self.numOfBadGuyTypes = []
        self.goodGuyNextId = 1
        self.badGuyNextId = 1
        self.setWavePools(1)

    def setWavePools(self, waveNumber):

        self.badGuyList.clear()
        self.numOfBadGuyTypes.clear()

        waveGroupConfigs = {
            1: [{'badGuyType': 1, 'numOfBadGuys': 3, 'spawnTime': 1, 'spawnDifference': 1}],

            2: [{'badGuyType': 1, 'numOfBadGuys': 3, 'spawnTime': 1, 'spawnDifference': 1},
                {'badGuyType': 2, 'numOfBadGuys': 1, 'spawnTime': 5, 'spawnDifference': 1}],

            3: [{'badGuyType': 1, 'numOfBadGuys': 3, 'spawnTime': 1, 'spawnDifference': 1},
                {'badGuyType': 2, 'numOfBadGuys': 3, 'spawnTime': 5, 'spawnDifference': 1},
                {'badGuyType': 2, 'numOfBadGuys': 3, 'spawnTime': 10, 'spawnDifference': 1}],

            4: [{'badGuyType': 1, 'numOfBadGuys': 3, 'spawnTime': 1, 'spawnDifference': 1},
                {'badGuyType': 2, 'numOfBadGuys': 3, 'spawnTime': 5, 'spawnDifference': 1},
                {'badGuyType': 2, 'numOfBadGuys': 3, 'spawnTime': 5, 'spawnDifference': 1},
                {'badGuyType': 3, 'numOfBadGuys': 1, 'spawnTime': 10, 'spawnDifference': 1}],

            5: [{'badGuyType': 1, 'numOfBadGuys': 3, 'spawnTime': 1, 'spawnDifference': 1},
                {'badGuyType': 2, 'numOfBadGuys': 3, 'spawnTime': 5, 'spawnDifference': 1},
                {'badGuyType': 2, 'numOfBadGuys': 3, 'spawnTime': 5, 'spawnDifference': 1},
                {'badGuyType': 3, 'numOfBadGuys': 1, 'spawnTime': 10, 'spawnDifference': 1},
                {'badGuyType': 3, 'numOfBadGuys': 1, 'spawnTime': 15, 'spawnDifference': 1}],
        }

        if waveNumber in waveGroupConfigs:
            waveGroupList = waveGroupConfigs[waveNumber]
            for waveGroup in waveGroupList:
                self.badGuyFactory(**waveGroup)

    # Add the lists together and return
    def getGuyLists(self):
        return self.goodGuyList + self.badGuyList

    # Spawn time is seconds, spawn difference is how fast after the last spawn
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
        self.anyAlive = any(badGuy.isAlive for badGuy in self.badGuyList)


