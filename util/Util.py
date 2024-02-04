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
def isInside(point, guy, r=None):
    # (x - center_x)² + (y - center_y)² < radius²
    if r is None:
        if guy.entityType == "bad":
            r = guy.rect.width/2
        else:
            r = guy.rangeRad
    return pow(point[0] - guy.rect.centerx, 2) + pow(point[1] - guy.rect.centery, 2) < pow(r, 2)

def dis(guy1, guy2):
    return math.dist([guy1.rect.x, guy1.rect.y], [guy2.rect.x, guy2.rect.y])

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
            # guy.infoBlock.sellBlock.rectList is [("SELL", Rect(x,y,w,h)]
            if guy.infoBlock.sellBlock.rectList[0][1].collidepoint(pos):
                return guy
    return None

def mouseInSelectedStats(pool, pos):
    for goodGuy in pool.goodGuyList:
        if goodGuy.isSelected and goodGuy.infoBlock.statBlock.rect.collidepoint(pos):
            return goodGuy

def handleEntitySelect(world, pos):
    # Draw stats every loop to make sure they are updated

    clicked = False
    for guy in world.pool.getGuyLists():
        # Use different clicks since goodGuys are squares and badGuys are circles
        if (guy.entityType == "good" and guy.rect.collidepoint(pos))\
           or (guy.entityType == "bad" and isInside(pos, guy)):
            clicked = True
            guy.isSelected = not guy.isSelected

            # if guy clicked isSelected increment, if guy is deselected decrement
            if guy.isSelected:
                world.numSelected += 1
            else:
                world.numSelected -= 1

    return clicked

def handleClickedNothing(world):
    # If only one guy is selected allow for screen click to deselect
    if world.numSelected == 1:
        handleDeselectButton(world)

def handleBuyButton(world, clickedButton):
    world.selectedBuyGuy = clickedButton.goodGuy

def handlePlayButton(world):
    world.switchCurrentMode()

def handlePlaceGoodGuy(world):
    world.pool.addGoodGuy(world.selectedBuyGuy.copyGoodGuy(world.pool.goodGuyNextId))
    world.pool.goodGuyNextId += 1
    world.minusBones(world.selectedBuyGuy.bones)
    world.selectedBuyGuy = None

def handlePlaceGuyClick(world, event):
    # If right click deselect the buyGuy
    if event.button == 3:
        world.selectedBuyGuy = None
    # If left click
    elif event.button == 1:
        # if mouse in hud do some red lines around the guy
        if mouseInHud(world.hud, event.pos):
            world.setPlacingTowerError()
        else: # if anywhere else place guy
            handlePlaceGoodGuy(world)

def handleStatClick(clickedGuy, pos):
    # look through the guys infoBlock stats
    # statTuple = [("String", Rect)]
    for statTuple in clickedGuy.infoBlock.statBlock.rectList:
        if statTuple[1].collidepoint(pos): # If clicked a stat
            if "Targeting Method" in statTuple[0]: # if click stat String is "Targeting Method"
                clickedGuy.handleTargetingMethodChange()

def handleSell(world, soldGoodGuy):
    for button in world.hud.rectList:
        if button.buttonFunction == "buy" and button.goodGuy.towerType == soldGoodGuy.towerType:
            world.setSoldGuy(soldGoodGuy, button.rect)

    world.pool.sellGoodGuy(soldGoodGuy.entityId)
    world.addBones(soldGoodGuy.bones)
    world.numSelected -= 1

def handleDeselectButton(world):
    world.numSelected = 0
    for guy in world.pool.getGuyLists():
        if guy.isSelected:
            guy.isSelected = False

def handleClick(world, event):
    # If buying a guy then place guy in world and subtract money
    if world.selectedBuyGuy:
        handlePlaceGuyClick(world, event)
    else:  # If no selected then check if mouse click on entity or hud buttons
        if clickedGuy := mouseInSelectedStats(world.pool, event.pos):
            handleStatClick(clickedGuy, event.pos)
        elif soldGoodGuy := mouseInSell(world.pool, event.pos):
            handleSell(world, soldGoodGuy)
        # If in hud buttons then see which hud button was clicked
        elif clickedButton := mouseInHudButtons(world.hud, event.pos):
                if clickedButton.buttonFunction == "buy": # Prepare to buy a guy
                    handleBuyButton(world, clickedButton)
                elif clickedButton.buttonFunction == "play": # Acts as play/pause button
                    handlePlayButton(world)
                elif clickedButton.buttonFunction == "deselect": # Deselect all entities
                    handleDeselectButton(world)
        # If not in hud then for clickedEntity
        elif not handleEntitySelect(world, event.pos):
            handleClickedNothing(world)
