# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from world import *
import random
import numpy
import math

### Constants ###

# Directions X and Y are clockwise ordered. Direction 0 corresponds to going up and to the left.
DIRX = [-1, 0, 1, 1, 1, 0, -1, -1]
DIRY = [-1, -1, -1, 0, 1, 1,  1,  0]
ANGLE = [-135, -90, -45, 0, 45, 90, 135, 180]
NBDIRS = 8

SEARCH = 0
BACK = 1

### Class AntBrain ###

class AntBrain:

    def __init__(self, world, colony, ant):
        self.world = world
        self.colony = colony
        self.ant = ant
        self.heading = None # angle in radian
        self.mode = SEARCH

    def swapMode(self):
        if(self.mode == SEARCH):
            self.mode = BACK
        else:
            self.mode = SEARCH

    def randomDir(self):
        while True:
            direction = random.randint(0, NBDIRS - 1)
            newposx = self.ant.pos[0] + DIRX[direction]
            newposy = self.ant.pos[1] + DIRY[direction]
            if(self.world.isValidPos((newposx, newposy))):
                break
        return direction

    # given a target position, find the best discrete direction
    def targetPos(self, targetpos):
        if self.ant.pos == targetpos:
            return -1
        mindist = float("inf")
        bestdir = -1
        for i in range(NBDIRS):
            newpos = numpy.array(
                [self.ant.pos[0] + DIRX[i], self.ant.pos[1] + DIRY[i]])
            tgtpos = numpy.array([targetpos[0], targetpos[1]])
            dist = numpy.linalg.norm(tgtpos-newpos)
            if dist < mindist:
                mindist = dist
                bestdir = i
        return bestdir

    def targetDir(self, angle):
        homepos = self.ant.home()
        r = max(self.world.width, self.world.height)
        vec = (r*math.cos(angle), r*math.sin(angle))
        targetpos = (homepos[0] + vec[0], homepos[1] + vec[1])
        return self.targetPos(targetpos)

    def act(self):
        direction = -1

        # seach mode
        if self.mode == SEARCH:
            if self.heading == None:
                self.heading = random.random()*2*math.pi
            direction = self.targetDir(self.heading)
            # direction = self.randomDir()

        # back mode
        if self.mode == BACK:
            self.heading = None
            direction = self.targetPos(self.ant.home())

        # 2) move forward in this direction
        ok = self.ant.move(direction)
        if not ok:
            self.heading = None

        # 3) swap mode
        if self.mode == SEARCH and self.ant.onFood():
            self.swapMode()
        elif self.mode == BACK and self.ant.atHome():
            self.swapMode()

### Class Ant ###

class Ant:

    def __init__(self, world, colony):
        self.world = world
        self.colony = colony
        self.pos = colony.pos
        self.brain = AntBrain(world, colony, self)
        self.food = 0

    def move(self, direction):
        if direction not in range(NBDIRS):
            return False
        newposx = self.pos[0] + DIRX[direction]
        newposy = self.pos[1] + DIRY[direction]
        newpos = (newposx, newposy)
        if not self.world.isValidPos(newpos):
            return False
        self.pos = (newposx, newposy)
        return True

    def onFood(self):
        return self.world.isFood(self.pos)

    def atHome(self):
        return (self.pos == self.colony.pos)

    def home(self):
        return self.colony.pos

    # def takeFood(self):
    #     if(self.food == 0 and self.world.isFood(self.pos)):
    #         self.world.food[self.pos[1]][self.pos[0]] -= 1
    #         self.food = 1
    #         return True
    #     return False

    def tick(self, dt):
        self.brain.act()

### Class AntColony ###


class AntColony:
    def __init__(self, world, pos):
        self.world = world
        self.pos = pos
        self.ants = []

    def addAnt(self):
        ant = Ant(self.world, self)
        self.ants.append(ant)
        return ant

    def addAnts(self, nb):
        for _ in range(nb):
            ant = self.addAnt()

    def tick(self, dt):
        for ant in self.ants:
            ant.tick(dt)
