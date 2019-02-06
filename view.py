# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from world import *
from ants import *
import pygame

################################################################################
#                                 VIEW                                         #
################################################################################

### Constants ###

PIXELSIZE = 4
FPS = 10
WIN_TITLE = "Ant Simulator"
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

### class GraphicView ###

class GraphicView:

    # initialize PyGame graphic view
    def __init__(self, world, colony):
        self.world = world
        self.colony = colony
        self.width = world.width * PIXELSIZE
        self.height = world.height * PIXELSIZE
        # create window
        self.win = pygame.display.set_mode((self.width, self.height))
        # init view
        # pygame.display.set_icon(self.sprite_bomb)
        title = WIN_TITLE
        pygame.display.set_caption(title)
        self.font = pygame.font.SysFont('Consolas', 20)

    # render world
    def renderWorld(self):
        self.win.fill(WHITE)
        # draw colony home
        pygame.draw.rect(self.win, GREEN, pygame.Rect((self.colony.pos[0]*PIXELSIZE, self.colony.pos[1]*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))
        # draw block and food
        for y in range(0, self.world.height):
            for x in range(0, self.world.width):
                if(self.world.food[y][x] > 0):
                    pygame.draw.rect(self.win, RED, pygame.Rect((x*PIXELSIZE, y*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))
                elif(self.world.block[y][x] > 0):
                    pygame.draw.rect(self.win, BLACK, pygame.Rect((x*PIXELSIZE, y*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))
                elif(self.world.pheromone[y][x] > 0):
                    pygame.draw.rect(self.win, YELLOW, pygame.Rect((x*PIXELSIZE, y*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))

    def renderAnts(self):
        for ant in self.colony.ants:
            x = ant.pos[0]
            y = ant.pos[1]
            pygame.draw.rect(self.win, BLUE, pygame.Rect((x*PIXELSIZE, y*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))

    # render PyGame graphic view at each clock tick
    def tick(self, dt):
        self.renderWorld()
        self.renderAnts()
        pygame.display.flip()

