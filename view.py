# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from world import *
from ants import *
import pygame
import colour

################################################################################
#                                 VIEW                                         #
################################################################################

### Constants ###

PIXELSIZE = 4
FPS = 10
WIN_TITLE = "Ant Simulator"

### Colors ###


def color2rgb(colorstr):
    color = colour.Color(colorstr)
    return (int(color.red*255), int(color.green*255), int(color.blue*255))

# https://pypi.org/project/colour/
# https://www.w3.org/TR/css-color-3/#svg-color

YELLOW = color2rgb("yellow")
BLUE = color2rgb("blue")
GREEN = color2rgb("limegreen")
RED = color2rgb("red")
MAGENTA = color2rgb("magenta")
WHITE = color2rgb("white")
BLACK = color2rgb("black")

# COLOR1 = colour.Color("gold")
# COLOR2 = colour.Color("orangered")
COLOR1 = colour.Color("yellow")
COLOR2 = colour.Color("gold")
COLORS = list(COLOR1.range_to(COLOR2, MAX_PHEROMONE))


### class GraphicView ###


class GraphicView:

    # initialize PyGame graphic view
    def __init__(self, world, colony):
        self.__world = world
        self.__colony = colony
        self.__winwidth = world.width() * PIXELSIZE
        self.__winheight = world.height() * PIXELSIZE
        self.__win = pygame.display.set_mode(
            (self.__winwidth, self.__winheight))
        # pygame.display.set_icon(self.ant_sprite)
        pygame.display.set_caption(WIN_TITLE)
        # self.font = pygame.font.SysFont('Consolas', 20)

    def getPheromoneColor(self, pos):
        level = self.__world.getPheromone(pos)
        if(level == 0):
            return WHITE
        if(level >= MAX_PHEROMONE):
            color = COLOR2
        else:
            color = COLORS[level]
        return (int(color.red*255), int(color.green*255), int(color.blue*255))

    # render world
    def renderWorld(self):
        self.__win.fill(WHITE)
        # draw block, food and pheromone
        for y in range(self.__world.height()):
            for x in range(self.__world.width()):
                if(self.__world.getFood((x, y)) > 0):
                    pygame.draw.rect(self.__win, RED, pygame.Rect(
                        (x*PIXELSIZE, y*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))
                elif(self.__world.isBlock((x, y))):
                    pygame.draw.rect(self.__win, BLACK, pygame.Rect(
                        (x*PIXELSIZE, y*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))
                elif(self.__world.getPheromone((x, y)) > 0):
                    color = self.getPheromoneColor((x, y))  # YELLOW
                    pygame.draw.rect(self.__win, color, pygame.Rect(
                        (x*PIXELSIZE, y*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))
        # draw colony home
        colonypos = self.__colony.pos()
        pygame.draw.rect(self.__win, GREEN, pygame.Rect(
            (colonypos[0]*PIXELSIZE, colonypos[1]*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))

    def renderAnts(self):
        ants = self.__colony.getAnts()
        for ant in ants:
            antpos = ant.pos()
            if ant.brain().mode() == SEARCH:
                antcolor = BLUE
            elif ant.brain().mode() == ESCAPE:
                antcolor = GREEN
            else:
                antcolor = MAGENTA
            pygame.draw.rect(self.__win, antcolor, pygame.Rect(
                (antpos[0]*PIXELSIZE, antpos[1]*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))

    # render PyGame graphic view at each clock tick

    def tick(self, dt):
        self.renderWorld()
        self.renderAnts()
        pygame.display.flip()
