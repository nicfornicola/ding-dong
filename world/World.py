import pygame
from pygame.rect import Rect

from buttons.Block import Block
from spawning.Pool import Pool

HEIGHT = 720
WIDTH = 1280

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
        self.level = 1
        self.pool = Pool("guys")
        self.timePlayed = 0
        self.timePaused = 0
        self.bones = 30
        self.soldGuy = None
        self.soldGuyPath = []
        self.soldGuyIndex = 0

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


    def isMoreThenOneSelected(self):
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

