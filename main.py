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

width = 120
height = 120
turn = 0
nbants = 100

# parse arguments
if len(sys.argv) == 1:
    pass
elif len(sys.argv) == 2:
    turn = int(sys.argv[1])
elif len(sys.argv) == 4:
    turn = int(sys.argv[1])
    width = int(sys.argv[2])
    height = int(sys.argv[3])
elif len(sys.argv) == 5:
    turn = int(sys.argv[1])
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    nbants = int(sys.argv[4])
else:
    print("Usage: ./main.py [turn] [width height] [nbants]]")

# initialization
pygame.display.init()
pygame.font.init()
clock = pygame.time.Clock()
world = World(width, height)
# world.addBlock((int(width/2)-20, int(height/2)+20), (40, 5))
world.addFood((0, 0), (20, 20))
world.addFood((width-20, 0), (20, 20))
world.addFood((0, height-20), (20, 20))
world.addFood((width-20, height-20), (20, 20))
colony = AntColony(world)
colony.addAnts(nbants)

kb = KeyboardController()
view = GraphicView(world, colony)

# main loop
while True:
    # make sure game doesn't run at more than FPS frames per second
    dt = clock.tick(FPS)
    if not kb.tick(dt):
        break
    world.tick(dt)
    colony.tick(dt)
    turn += 1
    print("{} {}".format(turn, colony.food()))
    view.tick(dt)

# quit
print("Game Over!")
pygame.quit()
