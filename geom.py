# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from constants import *
from world import *
from ants import *

import numpy
import random
import sys
import math
import bresenham

### Geometry Functions ###

def distance(pos0, pos1):
    dx = pos1[0] - pos0[0]
    dy = pos1[1] - pos0[1]
    return math.sqrt(dx*dx + dy*dy)


def isValidDir(world, antpos, antdir):
    newpos = (antpos[0] + DIRS[antdir][0], antpos[1] + DIRS[antdir][1])
    if world.isValidPos(newpos):
        return True
    return False


def targetDir(world, antpos, targetpos):
    if antpos == targetpos:
        return -1
    b = bresenham.bresenham(antpos[0], antpos[1], targetpos[0], targetpos[1])
    nextpos = next(b)
    if(nextpos == antpos):
        nextpos = next(b)
    # find direction
    bestdir = -1
    for i in range(NBDIRS):
        neighborpos = (antpos[0] + DIRS[i][0], antpos[1] + DIRS[i][1])
        if not world.isValidPos(neighborpos):
            continue
        if nextpos == neighborpos:
            bestdir = i
            break
    return bestdir


def rotateDir(world, antpos, antdir):
    if antdir == -1:
        return -1
    clockwise = 2 * random.randint(0, 1) - 1
    # r = random.randint(0, 4) # uniform distribution
    p = random.random()
    for r in range(5):
        if(p <= PROBASUM[r]):
            break
    newdir = (antdir + clockwise * r) % NBDIRS
    if isValidDir(world, antpos, newdir):
        return newdir
    return antdir


def randomDir(world, antpos):
    while True:
        direction = random.randint(0, NBDIRS - 1)
        newpos = (antpos[0] + DIRS[direction][0],
                  antpos[1] + DIRS[direction][1])
        if(world.isValidPos(newpos)):
            break
    return direction


def pheromoneDir(world, antpos, homepos, optdist):
    antdist = distance(homepos, antpos)
    maxpheromone = 0
    bestdir = -1
    for i in range(NBDIRS):
        neighborpos = (antpos[0] + DIRS[i][0], antpos[1] + DIRS[i][1])
        if not world.isValidPos(neighborpos):
            continue
        pheromone = world.getPheromone(neighborpos)
        neighbordist = distance(homepos, neighborpos)
        if((not optdist) and (pheromone > maxpheromone)):
            maxpheromone = pheromone
            bestdir = i
        if(optdist and (pheromone > maxpheromone) and (neighbordist > antdist)):
            maxpheromone = pheromone
            bestdir = i
    return bestdir

def foodDir(world, antpos):
    maxfood = 0
    bestdir = -1
    for i in range(NBDIRS):
        neighborpos = (antpos[0] + DIRS[i][0], antpos[1] + DIRS[i][1])
        if not world.isValidPos(neighborpos):
            continue
        food = world.getFood(neighborpos)
        if(food > maxfood):
            maxfood = food
            bestdir = i
    return bestdir

def randomTargetPos(world, antpos, dist = 0):
    if dist == 0:
        dist = max(world.width(),world.height())
    while True:
        dx = random.randint(-dist, dist)
        dy = random.randint(-dist, dist)
        if dx != 0 and dy != 0:
            break
    return (antpos[0] + dx, antpos[1] + dy)

def randomPos(world):
    while True:
        x = random.randint(0, world.width()-1)
        y = random.randint(0, world.height()-1)
        if world.isValidPos((x, y)):
            return (x, y)

