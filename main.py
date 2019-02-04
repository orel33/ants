#!/usr/bin/env python3
# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from world import *
from ants import *
from view import *
from keyboard import *
import sys
import pygame

### python version ###
print("python version: {}.{}.{}".format(
    sys.version_info[0], sys.version_info[1], sys.version_info[2]))
print("pygame version: ", pygame.version.ver)

################################################################################
#                                 MAIN                                         #
################################################################################

width = DEFAULT_WIDTH
height = DEFAULT_HEIGHT

# parse arguments
if len(sys.argv) == 3:
    width = int(sys.argv[1])
    height = int(sys.argv[2])

# initialization
pygame.display.init()
pygame.font.init()
clock = pygame.time.Clock()
world = World(width, height)
world.addBlock((int(width/2)-40, int(height/2)+40), (60, 10))
world.addFood((0, 0), (20, 20))
world.addFood((width-20, 0), (20, 20))
world.addFood((0, height-20), (20, 20))
world.addFood((width-20, height-20), (20, 20))
colony = AntColony(world, (int(width/2), int(height/2)))
colony.addAnts(100)

kb = KeyboardController()
view = GraphicView(world, colony)

# main loop
while True:
    # make sure game doesn't run at more than FPS frames per second
    dt = clock.tick(FPS)
    if not kb.tick(dt):
        break
    # world.tick(dt)
    colony.tick(dt)
    view.tick(dt)

# quit
print("Game Over!")
pygame.quit()
