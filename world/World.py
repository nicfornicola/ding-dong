import pygame
from pygame.rect import Rect

from buttons.Block import Block
from buttons.Button import Button
from models.GoodGuy import GoodGuy
from models.SoldGuy import SoldGuy
from spawning.Pool import Pool

HEIGHT = 720
WIDTH = 1280

# Using the Bresenham method
def setSellPath(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    i = 0
    while True:
        if i % 5 == 0:
            points.append(pygame.Vector2(x0, y0))

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
        i += 1

    return points

def setTemplateGoodGuys():
    towerTypes = ["green", "blue", "purple", "yellow", "pink", "black"]
    templateGoodGuys = []
    for towerType in towerTypes:
        templateGoodGuys.append(GoodGuy(towerType))
    return templateGoodGuys

class World:

    def __init__(self):
        self.globalHp = 100
        self.currentMode = "pause" # build play pause
        self.selectedBuyGuy = None
        self.selectedBuyGuyError = False
        self.errorTimer = 0
        self.numSelected = 0
        self.hud = Block(Rect(0, HEIGHT * .90, WIDTH, HEIGHT - HEIGHT * .90), [])
        self.playButtonImg = pygame.image.load("img/playButton.png").convert()
        self.pauseButtonImg = pygame.image.load("img/pauseButton.png").convert()
        self.deselectImg = pygame.transform.scale(pygame.image.load("img/deselectButton.png").convert(), (20, 20))
        self.pool = Pool("guys")
        self.timePlayed = 0
        self.timePaused = 0
        self.bones = 1000
        self.soldGuys: list = []
        self.templateGuys = setTemplateGoodGuys()
        self.buyButtonImgList = []
        self.buyButtonGreyImgList = []
        self.deselectButton = self.setDeselectButton()
        self.currentWave = 1
        self.finalWave = 2
        self.wonLevel = False
        self.endLevel = False
        self.testMode = False
        self.setButtonImgs()


    def setDeselectButton(self):
        return Button("deselect", self.deselectImg,
                      Rect(self.hud.rect.x + 5,
                           self.hud.rect.y - 30,
                           self.deselectImg.get_width(),
                           self.deselectImg.get_height())
                      )

    def setButtonImgs(self):
        for guy in self.templateGuys:
            imgString = "img/" + guy.towerType + "Tower.png"
            self.buyButtonImgList.append(pygame.image.load(imgString).convert())
            self.buyButtonGreyImgList.append(pygame.image.load("img/greyedOutTower.png").convert())

    def setSoldGuy(self, guy, endRect):
        soldGuy = SoldGuy(guy)
        soldGuy.sellSpot = Rect(soldGuy.rect.x, soldGuy.rect.y, soldGuy.rect.w, soldGuy.rect.h)
        soldGuy.path = setSellPath(soldGuy.rect.center, endRect.center)
        self.soldGuys.append(soldGuy)

    def setPlacingTowerError(self):
        self.selectedBuyGuyError = True
        self.errorTimer = 10

    def checkPlaceErrorTimeOut(self):
        if self.selectedBuyGuyError and self.errorTimer > 0:
            self.errorTimer -= 1
            return True
        else:
            self.selectedBuyGuyError = False
            return False

    def showDeselect(self):
        return self.numSelected > 1

    def addBones(self, bones):
        self.hud.rectList = [] # Reset the hudList so it renders again
        self.bones += bones

    def minusBones(self, bones):
        self.hud.rectList = [] # Reset the hudList so it renders again
        self.bones -= bones

    def switchCurrentMode(self):
        # If currently playing then pause the game
        if self.currentMode == "play":
            self.currentMode = "pause"
            self.setTimePlayed()
        # If currently paused then play
        elif self.currentMode == "pause":
            self.setTimePaused()
            self.currentMode = "play"

    def updateTime(self):
        if self.currentMode == "play":
            self.setTimePlayed()

        # If not playing then play
        elif self.currentMode == "pause":
            self.setTimePaused()

    def setTimePlayed(self):
        self.timePlayed = pygame.time.get_ticks()/1000 - self.timePaused

    def setTimePaused(self):
        self.timePaused = pygame.time.get_ticks()/1000 - self.timePlayed

    def checkWonLevel(self):
        if self.endLevel and self.currentWave == self.finalWave:
            print("you won")
            self.wonLevel = True
            return True
        else:
            return False


    def checkLevelStatus(self):
        if self.pool.numOfBadGuysThrough == len(self.pool.badGuyList) or not self.pool.anyAlive:
            self.endLevel = True
            self.currentMode = "pause"
            self.pool.anyAlive = True

            if not self.checkWonLevel():
                self.currentWave += 1
                self.pool.setWavePools(self.currentWave)

