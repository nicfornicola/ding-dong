import math

import pygame
from pygame.rect import Rect

HEIGHT = 720
WIDTH = 1280


def inWindow(x,y):
    return -1 < x < 1280 and -1 < y < 720

def notSeen(x,y,traveled):
    return not Rect(x, y, 1, 1) in traveled

def findNewPos(pixels,x,y,traveled):
    newPos = None

    if inWindow(x + 1, y) and pixels[x + 1][y] == 0 and notSeen(x + 1, y, traveled): # right
        newPos = Rect(x + 1, y, 1, 1)
    elif inWindow(x - 1, y) and pixels[x - 1][y] == 0 and notSeen(x - 1, y, traveled):  # left
        newPos = Rect(x - 1, y, 1, 1)
    elif inWindow(x, y + 1) and pixels[x][y + 1] == 0 and notSeen(x, y + 1, traveled):  # down
        newPos = Rect(x, y + 1, 1, 1)
    elif inWindow(x, y - 1) and pixels[x][y - 1] == 0 and notSeen(x, y - 1, traveled):  # up
        newPos = Rect(x, y - 1, 1, 1)
    elif inWindow(x + 1, y + 1) and pixels[x + 1][y + 1] == 0 and notSeen(x + 1, y + 1, traveled):  # right down
        newPos = Rect(x + 1, y + 1, 1, 1)
    elif inWindow(x - 1, y - 1) and pixels[x - 1][y - 1] == 0 and notSeen(x - 1, y - 1, traveled):  # left up
        newPos = Rect(x - 1, y - 1, 1, 1)
    elif inWindow(x + 1, y - 1) and pixels[x + 1][y - 1] == 0 and notSeen(x + 1, y - 1, traveled):  # right up
        newPos = Rect(x + 1, y - 1, 1, 1)
    elif inWindow(x - 1, y + 1) and pixels[x - 1][y + 1] == 0 and notSeen(x - 1, y + 1, traveled):  # left down
        newPos = Rect(x - 1, y + 1, 1, 1)

    return newPos

# x and y are point to find if in circle
def isInside(pointX, pointY, guy):
    # (x - center_x)² + (y - center_y)² < radius²
    if guy.entityType == "bad":
        r = guy.rect.width/2
    else:
        r = guy.rangeRad
    return pow(pointX - guy.rect.centerx, 2) + pow(pointY - guy.rect.centery, 2) < pow(r ,2)

def dis(guy1, guy2):
    return math.dist([guy1.rect.x, guy1.rect.y], [guy2.rect.x, guy2.rect.y])

def handleEntitySelect(guyPool, pos):
    clickedGoodGuy = []
    clickedBadGuy = []

    for i in range(len(guyPool.goodGuyList)):
        if guyPool.goodGuyList[i].rect.collidepoint(pos):
            clickedGoodGuy.append(guyPool.goodGuyList[i])

    for i in range(len(guyPool.badGuyList)):
        if isInside(pos[0], pos[1], guyPool.badGuyList[i]):
            clickedBadGuy.append(guyPool.badGuyList[i])

    if len(clickedGoodGuy) > 0:
        guy = clickedGoodGuy[0]
    elif len(clickedBadGuy) > 0:
        guy = clickedBadGuy[0]
    else:
        guy = None

    return guy

def selectHudButton(hud, pos):
    for button in hud.rectList:
        if button.rect.collidepoint(pos):
            return button

    return None

def mouseInHud(world, pos):
    return world.hud.rect.collidepoint(pos)

def mouseInSell(world, pos):
    if world.selectedGuySellBlock:
        # [("SELL", Rect(x,y,w,h)]
        return world.selectedGuySellBlock.rectList[0][1].collidepoint(pos)
    return False

def handleBuyButton(clickedButton):
    return clickedButton.goodGuy.setGoodGuy()

def handlePlayButton(world):
    world.switchCurrentMode()

def handlePlaceGoodGuy(world):
    world.pool.addGoodGuy(world.selectedGuy.copyGoodGuy(world.pool.goodGuyNextId))
    world.pool.goodGuyNextId += 1

def mouseInSelectedStats(selectedGuyStatBlock, pos):
    if selectedGuyStatBlock:
        return selectedGuyStatBlock.rect.collidepoint(pos)

def handleStatClick(world, pos):
    for statTuple in world.selectedGuyStatBlock.rectList:
        if statTuple[1].collidepoint(pos):
            if "Targeting Method" in statTuple[0]:
                guy = world.selectedGuy
                index = guy.targetingMethods.index(guy.targetingMethod)
                guy.targetingMethod = guy.targetingMethods[0] if index + 1 == len(guy.targetingMethods) else guy.targetingMethods[index+1]


def handleClick(world):
    newSelectedGuy = None
    # If clicked hud to get selectedGuy with ID: -1 then this click will place guy in world
    if world.selectedGuy and world.selectedGuy.entityId == -1:
        handlePlaceGoodGuy(world)

    else:  # If no selected then check where mouse click happened, if on placed entity or hud
        pos = pygame.mouse.get_pos()
        # If mouse is in hud then check for clicked buttons
        if mouseInSelectedStats(world.selectedGuyStatBlock, pos):
            handleStatClick(world, pos)
            newSelectedGuy = world.selectedGuy
        elif mouseInSell(world, pos):
            world.pool.sellGoodGuy(world.selectedGuy.entityId)
        elif mouseInHud(world, pos):
            if clickedButton := selectHudButton(world.hud, pos):
                if clickedButton.buttonType == "buy":
                    newSelectedGuy = handleBuyButton(clickedButton)
                elif clickedButton.buttonType == "play": # Acts as play/pause button
                    handlePlayButton(world)
        # Else check for clickedEntity
        else:
            newSelectedGuy = handleEntitySelect(world.pool, pos)

    return newSelectedGuy



