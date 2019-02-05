# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from world import *
import random
import numpy

### Constants ###

# Directions X and Y are clockwise ordered. Direction 0 corresponds to going up and to the left.
DIRX = [-1, 0, 1, 1, 1, 0, -1, -1]
DIRY = [-1, -1, -1, 0, 1, 1,  1,  0]
ANGLE = [-135, -90, -45, 0, 45, 90, 135, 180]
NBDIRS = 8

### Class Ant ###

class Ant:
    def __init__(self, world, pos):
        self.world = world
        self.pos = pos
        self.direction = -1
        self.targetpos = None

    def setTargetPos(self, pos=None):
        if(pos == None):
            pos = self.world.randomPos()
        self.targetpos = pos
        self.direction = -1
        return pos

    def randomDir(self):
        while True:
            direction = random.randint(0, NBDIRS - 1)
            newposx = self.pos[0] + DIRX[direction]
            newposy = self.pos[1] + DIRY[direction]
            if(self.world.isValidPos((newposx, newposy))):
                break
        return direction

    # given a target position, find the best discrete direction
    def targetDir(self, targetpos):
        if self.pos == targetpos:
            return -1
        mindist = float("inf")
        bestdir = -1
        for i in range(NBDIRS):
            newpos = numpy.array(
                [self.pos[0] + DIRX[i], self.pos[1] + DIRY[i]])
            tgtpos = numpy.array([targetpos[0], targetpos[1]])
            dist = numpy.linalg.norm(tgtpos-newpos)
            if dist < mindist:
                mindist = dist
                bestdir = i
        return bestdir

    def move(self):
        newposx = self.pos[0] + DIRX[self.direction]
        newposy = self.pos[1] + DIRY[self.direction]
        newpos = (newposx, newposy)
        if self.world.isValidPos(newpos):
            self.pos = (newposx, newposy)

    def tick(self, dt):
        # choose direction
        if self.targetpos != None:
            self.direction = self.targetDir(self.targetpos)
        else:
            self.direction = self.randomDir()
        # move forward in this direction
        if self.direction in range(NBDIRS):
            self.move()
        # check position
        if self.targetpos == self.pos:
            self.targetpos = None

### Class AntColony ###

class AntColony:
    def __init__(self, world, pos):
        self.world = world
        self.pos = pos
        self.ants = []

    def addAnt(self, pos=None):
        if pos is None:
            pos = self.pos
        ant = Ant(self.world, pos)
        self.ants.append(ant)
        return ant

    def addAnts(self, nb, pos=None):
        for _ in range(nb):
            ant = self.addAnt(pos)
            ant.setTargetPos((0,0))

    def tick(self, dt):
        for ant in self.ants:
            ant.tick(dt)
