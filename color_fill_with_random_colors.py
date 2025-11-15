import random, pygame, sys
from pygame.locals import *

WINDOWWIDTH = 800  # size of window's width in pixels
WINDOWHEIGHT = 640  # size of windows' height in pixels
BOARDWIDTH = 5  # number of columns of icons X
BOARDHEIGHT = 5  # number of rows of icons Y
BOXSIZE = 70
GAPSIZE = 10

GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

COLORS = (GREEN, BLUE, PURPLE, CYAN)

BGCOLOR = GRAY
BOXCOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)


def main():
    global DISPLAYSURF, BASICFONT

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Color fill')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)

    colored_boxes_num = 0
    boxes = initialize_boxes()

    DISPLAYSURF.fill(BGCOLOR)
    draw_squares(boxes)

    CURRENT_COLOR = get_next_color()
    NEXT_4_COLORS = [CURRENT_COLOR, get_next_color(), get_next_color(), get_next_color()]

    while True:
        check_for_quit()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                box_x, box_y = getSpotClicked(event.pos[0], event.pos[1])

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

                                CURRENT_COLOR = NEXT_4_COLORS[1]
                                NEXT_4_COLORS.pop(0)
                                NEXT_4_COLORS.append(get_next_color())
                                draw_current_color(NEXT_4_COLORS)

                        else:
                            #poraz - boite se edna do dr
                            game_lost()

        pygame.display.update()

def draw_current_color(NEXT_4_COLORS):
    infoSurf = BASICFONT.render('Next colors:', 1, BLACK)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (WINDOWWIDTH - 130, WINDOWHEIGHT - 300)
    DISPLAYSURF.blit(infoSurf, infoRect)

    pygame.draw.rect(DISPLAYSURF, NEXT_4_COLORS[0], (WINDOWWIDTH - 115, WINDOWHEIGHT - 275, BOXSIZE, BOXSIZE / 2))
    pygame.draw.rect(DISPLAYSURF, NEXT_4_COLORS[1], (WINDOWWIDTH - 115, WINDOWHEIGHT - 235, BOXSIZE, BOXSIZE / 2))
    pygame.draw.rect(DISPLAYSURF, NEXT_4_COLORS[2], (WINDOWWIDTH - 115, WINDOWHEIGHT - 195, BOXSIZE, BOXSIZE / 2))
    pygame.draw.rect(DISPLAYSURF, NEXT_4_COLORS[3], (WINDOWWIDTH - 115, WINDOWHEIGHT - 155, BOXSIZE, BOXSIZE / 2))


def check_boxes_around(boxx, boxy, boxes):
    if ((boxx - 1 >= 0 and boxes[boxx][boxy] == boxes[boxx - 1][boxy]) or
            (boxx + 1 < BOARDWIDTH and boxes[boxx][boxy] == boxes[boxx + 1][boxy]) or
            (boxy + 1 < BOARDWIDTH and boxes[boxx][boxy] == boxes[boxx][boxy + 1]) or
            (boxy - 1 >= 0 and boxes[boxx][boxy] == boxes[boxx][boxy - 1])):
        return False
    return True


def getSpotClicked(x, y):
    for tileX in range(BOARDWIDTH):
        for tileY in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(tileX, tileY)
            tileRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if tileRect.collidepoint(x, y):
                return tileX, tileY
    return None, None


def get_next_color():
    return random.choice(COLORS)


def color_box(boxx, boxy, color):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, color, (left, top, BOXSIZE, BOXSIZE))


def initialize_boxes():
    # boxes = []
    #     for x in range(BOARDWIDTH):
    #         column = []
    #         for y in range(BOARDHEIGHT):
    #             column.append(BOXCOLOR)
    #         boxes.append(column)
    #     return boxes
    boxes = []
    for i in range(BOARDHEIGHT):
        row = []
        for j in range(BOARDWIDTH):
            row.append(BOXCOLOR)
        boxes.append(row)
    return boxes


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top


def draw_squares(boxes):
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(i, j)
            pygame.draw.rect(DISPLAYSURF, boxes[i][j], (left, top, BOXSIZE, BOXSIZE))


def terminate():
    pygame.quit()
    sys.exit()


def check_for_quit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def game_won():
    DISPLAYSURF.fill(BLACK)
    infoSurf = BASICFONT.render('You Won!', True, WHITE)
    infoRect = infoSurf.get_rect(center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
    DISPLAYSURF.blit(infoSurf, infoRect)

    pygame.display.update()
    pygame.time.wait(2000)
    terminate()


def game_lost():
    DISPLAYSURF.fill(BLACK)
    infoSurf = BASICFONT.render('Game Over', True, WHITE)
    infoRect = infoSurf.get_rect(center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
    DISPLAYSURF.blit(infoSurf, infoRect)

    pygame.display.update()
    pygame.time.wait(2000)
    terminate()


if __name__ == '__main__':
    main()
