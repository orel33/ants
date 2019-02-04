# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

import random
import sys
import numpy

### Constants ###

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 400

### Class world ###

class World:

    # initialize world
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block = numpy.zeros((height, width))
        self.food = numpy.zeros((height, width))

    # add block
    def addBlock(self, pos=None, dim=None):
        if pos is None:
            pos = self.randomPos()
        if dim is None:
            dim = (10, 10)
        posx = pos[0]
        posy = pos[1]
        for y in range(dim[1]):
            for x in range(dim[0]):
                self.block[posy + y][posx + x] = 1
        print("=> add block at position ({},{}) of dimension ({},{})".format(
            pos[0], pos[1], dim[0], dim[1]))

    # add food
    def addFood(self, pos=None, dim=None, level=1):
        if pos is None:
            pos = self.randomPos()
        if dim is None:
            dim = (10, 10)
        posx = pos[0]
        posy = pos[1]
        for y in range(dim[1]):
            for x in range(dim[0]):
                self.food[posy + y][posx + x] = level
        print("=> add food at position ({},{}) of dimension ({},{})".format(
            pos[0], pos[1], dim[0], dim[1]))

    def randomPos(self):
        while True:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            if self.block[y][x] == 0:
                return (x, y)

    # update world at each clock tick
    # def tick(self, dt):
    #     # TODO: nop
