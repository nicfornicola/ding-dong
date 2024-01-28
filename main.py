import random
import sys

from buttons.Button import Button
from buttons.InfoBlock import InfoBlock
from spawning.Pool import Pool
from models.BadGuy import BadGuy
from models.GoodGuy import GoodGuy

import pygame
from pygame.locals import *

from util.Util import findNewPos, handleClick, inWindow
from world.World import World
from buttons.Block import Block
from buttons.BuyButton import BuyButton

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = [68,206,27] # RGB Color green
BLUEISH = [0,102,102] # RGB Color green
HEIGHT = 720
WIDTH = 1280
pygame.init()
clock = pygame.time.Clock()
running = True
bg = pygame.image.load("util/path.png")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

screen.blit(bg, (0, 0))


def buildPath(pixels) -> list[Rect] :
    # getting length of list
    length = len(pixels)

    path = []
    currentPos = None
    inner = pixels[0]
    for j in range(length):
        if inner[j] == 0:
            # get first position
            currentPos = Rect(0,j,1,1)
            path.append(currentPos)
            break

    # check around the current position for the next position
    firstLoop = True
    newPos = Rect(-100, -100, 0, 0)
    traveled = []
    while True :
        if not firstLoop:
            currentPos = newPos

        newPos = findNewPos(pixels,currentPos.x,currentPos.y,traveled)
        if newPos is None:
            break

        path.append(newPos)
        # keep a record of the last n tiles traveled to avoid backwards traversal
        n = 100
        if len(traveled) > n:
            traveled = [newPos] + traveled[:-1]
        else:
            traveled.append(newPos)
        firstLoop = False

    return path


def drawGoodGuys(pool: Pool):
    for goodGuy in pool.goodGuyList:
        # Draws solid line to show goodGuys currentTarget
        # if goodGuy.currentTarget:
        #     pygame.draw.line(screen, "red", (goodGuy.rect.centerx, goodGuy.rect.centery), (goodGuy.currentTarget.rect.centerx, goodGuy.currentTarget.rect.centery), 1)
        pygame.draw.rect(screen, goodGuy.color, goodGuy.rect)
        pygame.draw.circle(screen, "black", (goodGuy.rect.centerx, goodGuy.rect.centery), goodGuy.rangeRad, width=1)

def updateInRangeList(goodGuy, badGuyList):
    for badGuy in badGuyList:
        inRange = goodGuy.inRange(badGuy)
        # Remove from range list if not inRange or isDead
        if badGuy in goodGuy.inRangeList and (not inRange or not badGuy.isAlive):
            goodGuy.inRangeList.remove(badGuy)
        # Append to range list if not already in list inRange and isAlive
        elif badGuy not in goodGuy.inRangeList and inRange and badGuy.isAlive:
            goodGuy.inRangeList.append(badGuy)

def actionGoodGuys():
    for g in world.pool.goodGuyList:
        if g.canDoAction():
            updateInRangeList(g, world.pool.badGuyList)
            g.findTarget(world.pool)
            if g.shootTarget(world):
                pygame.draw.line(screen, g.color, (g.rect.centerx, g.rect.centery), (g.currentTarget.rect.centerx, g.currentTarget.rect.centery), g.damage)

def drawBadGuys(pool: Pool):
    for b in pool.badGuyList:
        pygame.draw.circle(screen, b.color, (b.rect.centerx, b.rect.centery), b.rect.width/2)
        pygame.draw.circle(screen, "black", (b.rect.centerx, b.rect.centery), b.rect.width/2, width=2)


def actionBadGuys(pool: Pool, path: list[Rect]):
    for badGuy in pool.badGuyList:

        if not badGuy.canSpawn:
            if world.timePlayed >= badGuy.spawnTime:
                badGuy.switchCanSpawn()

        if badGuy.isAlive and badGuy.canSpawn and badGuy.canDoAction():
            # if badGuy makes it to the end of the path
            if len(path) == badGuy.currentIndex + 1:
                world.globalHp -= 1 # take n hp off of globalHp
                # This resets badGuys when they get to the end
                badGuy.currentIndex = 0
                badGuy.hp = 10
                badGuy.isAlive = True

            pathIndex = badGuy.addToCurrentIndex()
            badGuy.rect.centerx = path[pathIndex].x
            badGuy.rect.centery = path[pathIndex].y
            badGuy.lastAction = pygame.time.get_ticks() # record this action

            for goodGuy in pool.goodGuyList:
                inRange = goodGuy.inRange(badGuy)
                if badGuy in goodGuy.inRangeList and not inRange:
                    goodGuy.inRangeList.remove(badGuy)
                elif badGuy not in goodGuy.inRangeList and inRange:
                    goodGuy.inRangeList.append(badGuy)



def findSelectedGuyStatsPosition(guy, maxWidth):
    # Default values for when the stat block is inWindow
    startStraight = pygame.Vector2(guy.rect.center)
    endStraight = pygame.Vector2(startStraight.x + guy.rect.w / 1.5, startStraight.y)
    endDiag = pygame.Vector2(endStraight.x + 5, endStraight.y + 5)
    # Need these values to find the max height
    textPaddingX = 5
    textPaddingY = 2
    textBlockPaddingHeight = 5
    # Max height will be constant for a list of N size
    maxHeight = (font.get_height() + textPaddingY*2 + textBlockPaddingHeight) * len(guy.getSelectedStats()) + textBlockPaddingHeight
    rightInWindow = False
    botInWindow = False

    if inWindow(endDiag.x + maxWidth + textPaddingX * 4, endDiag.y):
        rightInWindow = True
    if inWindow(endDiag.x, endDiag.y + maxHeight):
        botInWindow = True

    blockStart = pygame.Vector2(0, endDiag.y)
    diagonal = pygame.Vector2(endDiag.x, endDiag.y)

    if rightInWindow and botInWindow:  # In the window
        blockStart.x = endDiag.x
    elif not botInWindow and not rightInWindow:  # Both not in window
        endStraight.x = startStraight.x - guy.rect.w / 1.5
        diagonal.xy = (endStraight.x - 5, endStraight.y - 5)
        blockStart.xy = (diagonal.x - maxWidth - textPaddingX * 4, diagonal.y - maxHeight)
    elif not rightInWindow:
        endStraight.x = startStraight.x - guy.rect.w / 1.5
        diagonal.xy = (endStraight.x - 5, endStraight.y + 5)
        blockStart.x = diagonal.x - maxWidth - textPaddingX * 4 + 1
    elif not botInWindow:
        diagonal.xy = (endStraight.x + 5, endStraight.y - 5)
        blockStart.xy = diagonal.x + 1,  diagonal.y - maxHeight

    return startStraight, endStraight, diagonal, blockStart

# Draw the line with the statBlock
def drawSelectedGuyStats(guy):
    maxWidth = 0
    # Find maxWidth to check if inside the window
    for stat in guy.getSelectedStats():
        statWidth = (font.render(stat, True, "black")).get_rect().width

        # Find the largest element in the stats
        if maxWidth < statWidth:
            maxWidth = statWidth

    # Do alot of math to find where the stat block will be and move the coords if necessary
    startStraight, endStraight, endDiagonal, blockStart = findSelectedGuyStatsPosition(guy, maxWidth)

    guy.infoBlock = InfoBlock(drawBlock(blockStart, guy.getSelectedStats(), maxWidth=maxWidth), None)
    pygame.draw.line(screen, "black", startStraight, endStraight, 1)
    pygame.draw.line(screen, "black", endStraight, endDiagonal, 1)

    if guy.entityType == "good" and guy.entityId != -1:
        rect = guy.infoBlock.statBlock.rect
        x = rect.centerx - (rect.centerx - rect.x) / 3
        y = rect.y + rect.h
        guy.setSellBlock(drawBlock((x, y), ["SELL"], urgent=True))

# Set maxWidth to 0
def drawBlock(blockStart, stats, maxWidth=0, textPaddingX=5, textPaddingY=2, textBlockPaddingHeight=5, textBlockPaddingWidth=5, urgent=None):
    findMaxWidth = False
    if maxWidth == 0:
        findMaxWidth = True

    block = Block(Rect(blockStart, (maxWidth, 0)), [])
    color = "red" if urgent else "black"

    for stat in stats:
        # Gets statText render and rect
        statText = font.render(stat, True, color)
        statTextRect = statText.get_rect()

        # Find the largest element in the stats
        if findMaxWidth and block.maxWidth < statTextRect.width:
            block.maxWidth = statTextRect.width

        # Set the x, y of the textBox start from the outer block
        statTextRect.x = block.rect.x + textBlockPaddingWidth
        statTextRect.y = block.currentPaddingHeight + textBlockPaddingHeight

        # Add together the height of the text, textPadding and textBlockPadding to get the y to start the next block
        block.currentPaddingHeight += font.get_height() + textPaddingY*2 + textBlockPaddingHeight

        statTextRect.width += textPaddingX * 2
        statTextRect.height += textPaddingY * 2
        # Add to rectList the textRectBlock position and set the width and height to include the textPadding
        pygame.draw.rect(screen, color, statTextRect, width=1)
        block.rectList.append((stat, statTextRect))

        # Set the text x,y forward a padding amount, so it is centered within the textBlock
        statTextRect.x += textPaddingX
        statTextRect.y += textPaddingY

        # Blit the text
        screen.blit(statText, statTextRect)

    # Set the outer boxes to the largest text width + the  width
    if findMaxWidth:
        block.rect.width = block.maxWidth + textPaddingX*2 + textBlockPaddingWidth*2
    else:
        block.rect.width += textPaddingX*2 + textBlockPaddingWidth*2
    # Set the outer boxes height to the currentPaddingHeight but - blockY since this is the height not the Y value
    # and + textBlockPaddingHeight since it gets left out during the loop
    block.rect.height = block.currentPaddingHeight - block.rect.y + textBlockPaddingHeight
    # Draw the outer block
    pygame.draw.rect(screen, "black", block.rect, width=1)
    return block

def drawButton(button):
    screen.blit(button.img, (button.rect.x, button.rect.y))
    pygame.draw.rect(screen, "black", button.rect, width=1)

def getPlayButtonRect(playButtonWidth):
    block = world.hud
    blockPaddingHeight = 7
    blockPaddingWidth = 5
    # Set x to be right inside the HUD
    playButtonRect = Rect(block.rect.width - playButtonWidth + blockPaddingWidth,
                          block.rect.y + blockPaddingHeight,
                          playButtonWidth - blockPaddingWidth*2,
                          block.rect.h - blockPaddingHeight*2)

    # Put it in the worldList as a BuyButton to call later and set its image
    return Button("play", None, Rect(playButtonRect.x, playButtonRect.y, playButtonRect.w, playButtonRect.h))

def setPlayButtonImg(playButtonRect):
    # Scale the img for the first load only
    img = None
    if world.currentMode == "play":
        img = pygame.transform.scale(world.pauseButtonImg, (playButtonRect.w, playButtonRect.h))
    elif world.currentMode == "pause" or world.currentMode == "build":
        img = pygame.transform.scale(world.playButtonImg, (playButtonRect.w, playButtonRect.h))
    # Put it in the worldList as a BuyButton to call later and set its image
    return img

def getDeselectButtonRect():
    return Button("deselect", world.deselectImg, Rect(world.hud.rect.x + 5,
                                                      world.hud.rect.y - 30,
                                                      world.deselectImg.get_width(),
                                                      world.deselectImg.get_height()))

def drawBuyBlocks():
    playButtonWidth = 70

    # Only set up once
    if len(world.hud.rectList) == 0:
        block = world.hud
        block.currentPaddingWidth = 0

        guyCosts = [5,10,15]
        imgList = [pygame.image.load("img/blueTower.png").convert(),
                   pygame.image.load("img/greenTower.png").convert(),
                   pygame.image.load("img/purpleTower.png").convert(),
                   pygame.image.load("img/greyedOutTower.png").convert()]
        typeList = ["blue", "green", "purple"]
        # Num of blocks inside hud
        num = 3
        # Padding on the bottom and sides of the blocks
        statBlockPaddingHeight = 7
        statBlockPaddingWidth = 5
        buttonRect = Rect(0, 0, (block.rect.w-playButtonWidth)/num - statBlockPaddingWidth*2, block.rect.h - statBlockPaddingHeight*2)
        for i in range(num):

            # Set the x, y of the textBox start from the outer block
            buttonRect.x = block.currentPaddingWidth + statBlockPaddingWidth
            buttonRect.y = block.rect.y + statBlockPaddingHeight

            # Add together the width of the padding and blockPadding to get the x to start the next block
            block.currentPaddingWidth += buttonRect.width + statBlockPaddingWidth*2

            if world.bones < guyCosts[i]:
                img = imgList[-1]
            else:
                img = imgList[i]

            scaledImg = pygame.transform.scale(img, (buttonRect.w, buttonRect.h))

            # Put it in the worldList as a BuyButton to call later and set its image
            block.rectList.append(BuyButton("buy", typeList[i], scaledImg, Rect(buttonRect.x,
                                                                               buttonRect.y,
                                                                               buttonRect.width,
                                                                               buttonRect.height)))
        # Set the playButtonRect just once
        world.hud.rectList.append(getPlayButtonRect(playButtonWidth))

    # Set the playButton img and deselectButton every draw since it can change
    world.hud.rectList[3].img = setPlayButtonImg(world.hud.rectList[3].rect)

    if world.isMoreThenOneSelected():
        world.hud.rectList.append(getDeselectButtonRect())

    # Draw outer block
    pygame.draw.rect(screen, "tan", world.hud.rect, width=0)

    # Draw inner blocks
    for button in world.hud.rectList:
        if not world.isMoreThenOneSelected() and button.buttonFunction == "deselect":
            world.hud.rectList.remove(button)
            continue
        # Send the button to be drawn
        drawButton(button)


def drawSelectedBuyGuy(guy):
    guy.rect.center = pygame.mouse.get_pos()
    pygame.draw.rect(screen, guy.color, guy.rect)

    color = "black"
    if world.checkPlaceErrorTimeOut():
        color = "red"


    pygame.draw.rect(screen, color, guy.rect, width=1)
    pygame.draw.circle(screen, color, (guy.rect.centerx, guy.rect.centery), guy.rangeRad, width=1)
    drawSelectedGuyStats(world.selectedBuyGuy)


def drawNextBadGuys():
    w = 100
    h = 30
    block = Block(Rect(WIDTH * .5 - w/2, HEIGHT * .01, w, h), [])
    # imgList = [pygame.image.load("img/blueTower.png").convert(),
    #            pygame.image.load("img/greenTower.png").convert(),
    #            pygame.image.load("img/purpleTower.png").convert()]

    # Num of unique badGuys inside display
    uniqueList = []
    for badGuy in world.pool.badGuyList:
        if not badGuy.isTypeEqual(uniqueList):
            uniqueList.append(badGuy.copyBadGuy())
    num = len(uniqueList)

    # Padding on the bottom and sides of the blocks
    statBlockPaddingHeight = 3
    statBlockPaddingWidth = 2


    numRectList = []
    numFont = pygame.font.Font('freesansbold.ttf', 10)
    for i in range(num):
        badGuyRect = Rect(0, 0, block.rect.w / num - statBlockPaddingWidth * 2,
                          block.rect.h - statBlockPaddingHeight * 2)
        # Set the x, y of the textBox start from the outer block
        badGuyRect.x = block.currentPaddingWidth + statBlockPaddingWidth
        badGuyRect.y = block.rect.y + statBlockPaddingHeight

        # Add together the width of the padding and blockPadding to get the x to start the next block
        block.currentPaddingWidth += badGuyRect.width + statBlockPaddingWidth * 2
        uniqueList[i].rect = badGuyRect
        block.rectList.append(uniqueList[i])

        numText = numFont.render("x" + str(world.pool.numOfBadGuyTypes[i]), True, "black")
        numTextRect = numText.get_rect()
        numTextRect.center = (badGuyRect.centerx + h/3, badGuyRect.centery + h/3)

        numRectList.append((numText, numTextRect))


    # Draw outer block
    pygame.draw.rect(screen, "tan", block.rect, width=0)

    # Draw inner blocks
    for i in range(len(block.rectList)):
        # Send the buyButton to be drawn
        pygame.draw.circle(screen, block.rectList[i].color, block.rectList[i].rect.center, h/3, width=0)
        # pygame.draw.rect(screen, "red", block.rectList[i].rect)
        screen.blit(numRectList[i][0], numRectList[i][1])

def drawWorldStats():
    drawBlock((WIDTH * .01, HEIGHT * .01), ["HP: " + str(world.globalHp), "Bones: " + str(world.bones), "Played: " + str(round(world.timePlayed, 3))])


def drawHud():
    drawBuyBlocks()
    drawWorldStats()
    drawNextBadGuys()

    if world.selectedBuyGuy:
        drawSelectedBuyGuy(world.selectedBuyGuy)
    print(world.numSelected)
    # Draw stats every loop to make sure they are updated
    for guy in world.pool.getGuyLists():
        if guy.isSelected:
            drawSelectedGuyStats(guy)

########################## init #######################################
world = World()

font = pygame.font.Font('freesansbold.ttf', 12)
currentEntityText = font.render("", True, WHITE, BLACK)
currentEntityText.set_alpha(255)
currentEntityTextRect = Rect(0,0,0,0)

globalHpText = font.render(str(world.globalHp), True, WHITE, BLACK)
globalHpText.set_alpha(255)
globalHpTextRect = Rect(WIDTH * .95, HEIGHT * .05,0,0)

pathList = buildPath(pygame.surfarray.pixels2d(screen))

# Set the level 1 list of badGuys
# Spawn time is seconds, spawn difference is how fast after the last spawn
world.pool.badGuyFactory(badGuyType=1, numOfBadGuys=10, spawnTime=1, spawnDifference=1)
world.pool.badGuyFactory(badGuyType=2, numOfBadGuys=1 , spawnTime=1, spawnDifference=1)
world.pool.badGuyFactory(badGuyType=3, numOfBadGuys=10 , spawnTime=3, spawnDifference=.5)


while running:
    world.updateTime()
    # Draw background
    screen.blit(bg, (0, 0))
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handles mouse clicks on entities, hud and other stuff
        if event.type == pygame.MOUSEBUTTONDOWN:
            handleClick(world, event)

    drawBadGuys(world.pool)
    drawGoodGuys(world.pool)
    drawHud()

    if world.currentMode == "play":
        actionBadGuys(world.pool, pathList)
        actionGoodGuys()


    # change speed every 30 ticks gamble mode
    # timer += 1
    # if timer % 30 == 0:
    #     for i in range(len(badGuyPool.badGuyList)):
    #         badGuyPool.badGuyList[i].coolDown = random.randint(10, 500)

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()