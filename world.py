# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from constants import *
import random
import sys
import numpy
import math

### Auxiliary Functions ###

def distance(pos0, pos1):
    dx = pos1[0] - pos0[0]
    dy = pos1[1] - pos0[1]
    return math.sqrt(dx*dx + dy*dy)

# compute the discrete direction that minimize the distance from the target position


def targetPos(world, antpos, targetpos):
    if antpos == targetpos:
        return -1
    mindist = float("inf")
    bestdir = -1
    for i in range(NBDIRS):
        neighborpos = (antpos[0] + DIRS[i][0], antpos[1] + DIRS[i][1])
        dist = distance(neighborpos, targetpos)
        if dist < mindist:
            mindist = dist
            bestdir = i
    return bestdir


# def targetDir(world, homepos, antpos, angle):
#     r = max(world.width(), world.height())
#     # angle += (random.random()-0.5)*PERTURBATION
#     vec = (r*math.cos(angle), r*math.sin(angle))
#     targetpos = (homepos[0] + vec[0], homepos[1] + vec[1])
#     return targetPos(world, antpos, targetpos)


def randomDir(world, antpos):
    while True:
        direction = random.randint(0, NBDIRS - 1)
        newpos = (antpos[0] + DIRS[direction][0],
                  antpos[1] + DIRS[direction][1])
        if(world.isValidPos(newpos)):
            break
    return direction


def pheromoneDir(world, antpos, homepos):
    antdist = distance(homepos, antpos)
    maxpheromone = 0
    bestdir = -1
    for i in range(NBDIRS):
        neighborpos = (antpos[0] + DIRS[i][0], antpos[1] + DIRS[i][1])
        pheromone = world.getPheromone(neighborpos)
        neighbordist = distance(homepos, neighborpos)
        if(neighbordist > antdist):
            if(pheromone > maxpheromone):
                maxpheromone = pheromone
                bestdir = i
    return bestdir


def randomPos(world):
    while True:
        x = random.randint(0, world.width()-1)
        y = random.randint(0, world.height()-1)
        if not world.isBlock((x,y)):
            return (x, y)

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
            pos = randomPos(self)
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
            pos = randomPos(self)
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
