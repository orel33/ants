# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

import random
import sys
import numpy

MAX_PHEROMONE = 1200
DECAY_PHEROMONE = 2

### Class world ###


class World:

    # initialize world
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__block = numpy.zeros((height, width), dtype=int)
        self.__food = numpy.zeros((height, width), dtype=int)
        self.__pheromone = numpy.zeros((height, width), dtype=int)

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def isValidPos(self, pos):
        if pos[0] >= self.__width or pos[0] < 0 or pos[1] >= self.__height or pos[1] < 0:
            return False
        if self.isBlock(pos):
            return False
        return True

    def isBlock(self, pos):
        if self.__block[pos[1]][pos[0]] == 0:
            return False
        return True

    def getFood(self, pos):
        return self.__food[pos[1]][pos[0]]

    def getPheromone(self, pos):
        return self.__pheromone[pos[1]][pos[0]]

    def addBlock(self, pos=None, dim=None):
        if pos is None: 
            pos = self.randomPos()
        if dim is None:
            dim = (10, 10)
        posx = pos[0]
        posy = pos[1]
        for y in range(dim[1]):
            for x in range(dim[0]):
                self.__block[posy + y][posx + x] = 1
        print("=> add block at position ({},{}) of dimension ({},{})".format(
            pos[0], pos[1], dim[0], dim[1]))

    def addFood(self, pos, dim=(1, 1), level=1):
        if pos is None:
            pos = self.randomPos()
        if dim is None:
            dim = (10, 10)
        for y in range(dim[1]):
            for x in range(dim[0]):
                self.__food[pos[1] + y][pos[0] + x] += level
        print("=> add food at position ({},{}) of dimension ({},{})".format(
            pos[0], pos[1], dim[0], dim[1]))

    def removeFood(self, pos, level=1):
        self.__food[pos[1]][pos[0]] -= level
        if self.__food[pos[1]][pos[0]] < 0:
            self.__food[pos[1]][pos[0]] = 0

    def randomPos(self):
        while True:
            x = random.randint(0, self.__width-1)
            y = random.randint(0, self.__height-1)
            if self.__block[y][x] == 0:
                return (x, y)

    def addPheromone(self, pos, level):
        x = pos[0]
        y = pos[1]
        self.__pheromone[y][x] += level
        if self.__pheromone[y][x] > MAX_PHEROMONE:
            self.__pheromone[y][x] = MAX_PHEROMONE

    def decayPheromone(self):
        for y in range(self.__height):
            for x in range(self.__width):
                self.__pheromone[y][x] -= DECAY_PHEROMONE
                if self.__pheromone[y][x] <= 0:
                    self.__pheromone[y][x] = 0

    # update world at each clock tick
    def tick(self, dt):
        self.decayPheromone()
        pass
