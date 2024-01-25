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
        self.selectedGuy = None
        self.selectedBuyGuy = None
        self.selectedGuyStats = []
        self.selectedGuySellBlock = None
        self.selectedGuyStatBlock = None
        self.hud = Block(Rect(0, HEIGHT * .90, WIDTH, HEIGHT - HEIGHT * .90), [])
        self.playButtonImg = pygame.image.load("img/playButton.png").convert()
        self.pauseButtonImg = pygame.image.load("img/pauseButton.png").convert()
        self.level = 1
        self.pool = Pool("guys")
        self.timePlayed = 0
        self.timePaused = 0

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