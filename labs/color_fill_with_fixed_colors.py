import pygame
import random, pygame, sys
from pygame.locals import *

WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
BOXSIZE = 60 # size of box height & width in pixels
GAPSIZE = 5 # size of gap between boxes in pixels
BOARDWIDTH = 5 # number of columns of icons
BOARDHEIGHT = 5 # number of rows of icons

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK = (0, 0, 0)

BGCOLOR = BLACK
BOXCOLOR = WHITE
COLORS = [CYAN, YELLOW, GREEN, PURPLE]


def main():
    global DISPLAYSURF, BASICFONT, CURRENT_COLOR_INDEX
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Color Fill Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)

    colored_boxes_num = 0
    boxes = initialize_boxes()

    DISPLAYSURF.fill(BGCOLOR)
    draw_squares(boxes)

    CURRENT_COLOR_INDEX = 0
    CURRENT_COLOR = COLORS[CURRENT_COLOR_INDEX]

    while True:
        checkForQuit()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                box_x, box_y = getBoxAtPixel(event.pos[0], event.pos[1])

                if box_x is not None and box_y is not None:
                    if boxes[box_x][box_y] == BOXCOLOR:
                        boxes[box_x][box_y] = CURRENT_COLOR
                        color_box(box_x, box_y, CURRENT_COLOR)
                        colored_boxes_num += 1

                        if check_boxes_around(box_x, box_y, boxes):
                            if colored_boxes_num == BOARDWIDTH * BOARDHEIGHT:
                                # pobeda
                                game_won()

                            else:
                                # ushte trae igrate
                                DISPLAYSURF.fill(BGCOLOR)
                                draw_squares(boxes)

                                if CURRENT_COLOR_INDEX == 3:
                                    CURRENT_COLOR_INDEX = 0
                                else:
                                    CURRENT_COLOR_INDEX += 1

                                CURRENT_COLOR = COLORS[CURRENT_COLOR_INDEX]
                                show_next_colors()

                        else:
                            # poraz - boite se edna do dr
                            game_lost()

        pygame.display.update()


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top


def draw_squares(boxes):
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(i, j)
            pygame.draw.rect(DISPLAYSURF, boxes[i][j], (left, top, BOXSIZE, BOXSIZE))


def initialize_boxes():
    boxes = []
    for i in range(BOARDHEIGHT):
        row = []
        for j in range(BOARDWIDTH):
            row.append(BOXCOLOR)
        boxes.append(row)
    return boxes


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return boxx, boxy
    return None, None


def get_random_color():
    return random.choice(COLORS)


def check_boxes_around(boxx, boxy, boxes):
    if ((boxx - 1 >= 0 and boxes[boxx][boxy] == boxes[boxx - 1][boxy]) or
            (boxx + 1 < BOARDWIDTH and boxes[boxx][boxy] == boxes[boxx + 1][boxy]) or
            (boxy + 1 < BOARDWIDTH and boxes[boxx][boxy] == boxes[boxx][boxy + 1]) or
            (boxy - 1 >= 0 and boxes[boxx][boxy] == boxes[boxx][boxy - 1])):
        return False
    return True


def color_box(boxx, boxy, color):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, color, (left, top, BOXSIZE, BOXSIZE))


def game_won():
    DISPLAYSURF.fill(BLACK)
    infoSurf = BASICFONT.render('You Won!', 1, WHITE)
    infoRect = infoSurf.get_rect()
    DISPLAYSURF.blit(infoSurf, infoRect)

    pygame.display.update()
    pygame.time.wait(2000)
    terminate()


def game_lost():
    DISPLAYSURF.fill(BLACK)
    infoSurf = BASICFONT.render('Game Over', 1, WHITE)
    infoRect = infoSurf.get_rect()
    DISPLAYSURF.blit(infoSurf, infoRect)

    pygame.display.update()


def get_next_4_colors():
    temp_index = CURRENT_COLOR_INDEX
    next4 = [COLORS[temp_index]]
    for i in range(3):
        if temp_index == 3:
            temp_index = 0
        else:
            temp_index += 1
        next4.append(COLORS[temp_index])
    return next4


def show_next_colors():
    next_colors = get_next_4_colors()
    infoSurf = BASICFONT.render('Next colors:', 1, WHITE)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (WINDOWWIDTH - 130, WINDOWHEIGHT - 300)
    DISPLAYSURF.blit(infoSurf, infoRect)

    pygame.draw.rect(DISPLAYSURF, next_colors[0], (WINDOWWIDTH - 115, WINDOWHEIGHT - 275, BOXSIZE, BOXSIZE / 2))
    pygame.draw.rect(DISPLAYSURF, next_colors[1], (WINDOWWIDTH - 115, WINDOWHEIGHT - 235, BOXSIZE, BOXSIZE / 2))
    pygame.draw.rect(DISPLAYSURF, next_colors[2], (WINDOWWIDTH - 115, WINDOWHEIGHT - 195, BOXSIZE, BOXSIZE / 2))
    pygame.draw.rect(DISPLAYSURF, next_colors[3], (WINDOWWIDTH - 115, WINDOWHEIGHT - 155, BOXSIZE, BOXSIZE / 2))


if __name__ == '__main__':
    main()