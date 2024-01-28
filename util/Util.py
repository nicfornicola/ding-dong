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

def handleEntitySelect(world, pos):
    clicked = False
    for guy in world.pool.getGuyLists():
        if (guy.entityType == "good" and guy.rect.collidepoint(pos)) or (guy.entityType == "bad" and isInside(pos[0], pos[1], guy)):
            guy.isSelected = not guy.isSelected
            clicked = True

    if world.numSelected == 1 and not clicked:
        handleDeselectButton(world.pool)

def mouseInHud(hud, pos):
    return hud.rect.collidepoint(pos)

def mouseInHudButtons(hud, pos):
    for button in hud.rectList:
        if button.rect.collidepoint(pos):
            return button
    return None

def mouseInSell(pool, pos):
    for guy in pool.goodGuyList:
        if guy.infoBlock.sellBlock:
            # [("SELL", Rect(x,y,w,h)]
            if guy.infoBlock.sellBlock.rectList[0][1].collidepoint(pos):
                return guy
    return None


def handleBuyButton(world, clickedButton):
    world.selectedBuyGuy = clickedButton.goodGuy


def handlePlayButton(world):
    world.switchCurrentMode()

def handlePlaceGoodGuy(world, pos):
    if mouseInHud(world.hud, pos):
        world.setPlaceError()
    else:
        world.pool.addGoodGuy(world.selectedBuyGuy.copyGoodGuy(world.pool.goodGuyNextId))
        world.pool.goodGuyNextId += 1
        world.minusBones(world.selectedBuyGuy.bones)
        world.selectedBuyGuy = None

def mouseInSelectedStats(pool, pos):
    for goodGuy in pool.goodGuyList:
        if goodGuy.isSelected and goodGuy.infoBlock.statBlock.rect.collidepoint(pos):
            return goodGuy


def handleStatClick(clickedGuy, pos):
    for statTuple in clickedGuy.infoBlock.statBlock.rectList:
        if statTuple[1].collidepoint(pos):
            if "Targeting Method" in statTuple[0]:
                guy = clickedGuy
                index = guy.targetingMethods.index(guy.targetingMethod)
                guy.targetingMethod = guy.targetingMethods[0] if index + 1 == len(guy.targetingMethods) else guy.targetingMethods[index+1]

def handleSell(world, soldGuy):
    world.pool.sellGoodGuy(soldGuy.entityId)
    world.addBones(soldGuy.bones)

def handleDeselectButton(pool):
    for guy in pool.getGuyLists():
        if guy.isSelected:
            guy.isSelected = False

def handleClick(world):
    pos = pygame.mouse.get_pos()

    # If clicked hud to get selectedGuy with ID: -1 then this click will place guy in world
    if world.selectedBuyGuy:
        handlePlaceGoodGuy(world, pos)
    else:  # If no selected then check where mouse click happened, if on placed entity or hud
        # If mouse is in hud then check for clicked buttons
        if clickedGuy := mouseInSelectedStats(world.pool, pos):
            handleStatClick(clickedGuy, pos)
            # newSelectedGuy = world.selectedGuy
        elif soldGuy := mouseInSell(world.pool, pos):
            handleSell(world, soldGuy)
        elif clickedButton := mouseInHudButtons(world.hud, pos):
                if clickedButton.buttonFunction == "buy":
                    handleBuyButton(world, clickedButton)
                elif clickedButton.buttonFunction == "play": # Acts as play/pause button
                    handlePlayButton(world)
                elif clickedButton.buttonFunction == "deselect": # Acts as play/pause button
                    handleDeselectButton(world.pool)
        # Else check for clickedEntity
        else:
            handleEntitySelect(world, pos)




