
import random, pygame, sys
import tkinter
import time

from pygame.locals import *

FPS = 8
WINDOWWIDTH = 900
WINDOWHEIGHT = 700
CELLSIZE = 50
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
CELESTE = (78, 242, 209)
AZUL = (77, 77, 135)
BGCOLOR = BLACK
VIOLETA = (122, 77, 135)
CREMA = (250, 246, 200)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head




def main():

    global FPSCLOCK, DISPLAYSURF, BASICFONT


    pygame.init()

    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    pygame.display.set_caption('HELLO PENGUIN!!')

    showStartScreen()

    while True:

        runGame()

        #showGameOverScreen()


def runGame():

    # Set a random start point.

    startx = random.randint(5, CELLWIDTH - 6)

    starty = random.randint(5, CELLHEIGHT - 6)

    wormCoords = [{'x': startx,     'y': starty}]

    direction = None


    # Start the apple in a random place.

    apple1 = getRandomLocation() # set a new apple somewhere
    apple2 = getRandomLocation() # set a new apple somewhere
    apple3 = getRandomLocation() # set a new apple somewhere

    while True: # main game loop

        for event in pygame.event.get(): # event handling loop

            if event.type == QUIT:

                terminate()

            elif event.type == KEYDOWN:

                if (event.key == K_LEFT) and direction != RIGHT:

                    newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
                    wormCoords.insert(0, newHead)
                    wormCoords.pop()

                elif (event.key == K_RIGHT) and direction != LEFT:

                    newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
                    wormCoords.insert(0, newHead)
                    wormCoords.pop()

                elif (event.key == K_UP) and direction != DOWN:

                    newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
                    wormCoords.insert(0, newHead)
                    wormCoords.pop()

                elif (event.key == K_DOWN) and direction != UP:

                    newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
                    wormCoords.insert(0, newHead)
                    wormCoords.pop()

                elif event.key == K_ESCAPE:

                    terminate()


        # check if the worm has hit itself or the edge

        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:

            direction = None # game over

        for wormBody in wormCoords[1:]:

            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:

                direction = None # game over


        # check if worm has eaten an apply

        if wormCoords[HEAD]['x'] == apple1['x'] and wormCoords[HEAD]['y'] == apple1['y']:

            # don't remove worm's tail segment

            apple1 = getRandomLocation() # set a new apple somewhere

        if wormCoords[HEAD]['x'] == apple2['x'] and wormCoords[HEAD]['y'] == apple2['y']:

            apple2 = getRandomLocation() # set a new apple somewhere
            
        if wormCoords[HEAD]['x'] == apple3['x'] and wormCoords[HEAD]['y'] == apple3['y']:
        
            apple3 = getRandomLocation() # set a new apple somewhere


        DISPLAYSURF.fill(CELESTE)

        drawGrid()

        drawWorm(wormCoords)

        drawApple(apple1, RED)

        drawApple(apple2, AZUL)

        drawApple(apple3, GREEN)

        drawScore(len(wormCoords) - 3)

        pygame.display.update()

        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():

    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)

    pressKeyRect = pressKeySurf.get_rect()

    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)

    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)



def checkForKeyPress():

    if len(pygame.event.get(QUIT)) > 0:

        terminate()


    keyUpEvents = pygame.event.get(KEYUP)

    if len(keyUpEvents) == 0:

        return None

    if keyUpEvents[0].key == K_ESCAPE:

        terminate()

    return keyUpEvents[0].key



def showStartScreen():

    titleFont = pygame.font.Font('freesansbold.ttf', 100)

    titleSurf1 = titleFont.render('Hello Penguin!', True, WHITE, AZUL)

    titleSurf2 = titleFont.render('Hello Penguin!', True, CELESTE)

    degrees1 = 0

    degrees2 = 0

    while True:

        DISPLAYSURF.fill(BGCOLOR)

        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)

        rotatedRect1 = rotatedSurf1.get_rect()

        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)


        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)

        rotatedRect2 = rotatedSurf2.get_rect()

        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)


        drawPressKeyMsg()


        if checkForKeyPress():

            pygame.event.get() #clear event queue

            return

        pygame.display.update()

        FPSCLOCK.tick(FPS)

        degrees1 += 3 # rotate by 3 degrees each frame

        degrees2 += 7 # rotate by 7 degrees each frame



def terminate():

    pygame.quit()

    sys.exit()



def getRandomLocation():

    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}



def drawScore(score):

    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)

    scoreRect = scoreSurf.get_rect()

    scoreRect.topleft = (WINDOWWIDTH - 120, 10)

    DISPLAYSURF.blit(scoreSurf, scoreRect)



def drawWorm(wormCoords):

    for coord in wormCoords:

        x = coord['x'] * CELLSIZE

        y = coord['y'] * CELLSIZE

        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)

        pygame.draw.rect(DISPLAYSURF, VIOLETA, wormSegmentRect)

        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)

        pygame.draw.rect(DISPLAYSURF, CREMA, wormInnerSegmentRect)



def drawApple(coord, color):

    x = coord['x'] * CELLSIZE

    y = coord['y'] * CELLSIZE

    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)

    pygame.draw.rect(DISPLAYSURF, color, appleRect)



def drawGrid():

    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines

        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))

    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines

        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))



if __name__ == '__main__':

    main()