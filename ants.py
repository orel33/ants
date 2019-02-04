# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from world import *
import random

### Constants ###

DIRX = [-1, 0, 1, 1, 1, 0, -1, -1]
DIRY = [-1, -1, -1, 0, 1, 1,  1,  0]
NBDIRS = 8

### Class Ant ###

class Ant:
    def __init__(self, world, pos):
        self.world = world
        self.pos = pos
        self.direction = 0

    def randomDir(self):
        while True:
            direction = random.randint(0, NBDIRS - 1)
            newposx = self.pos[0] + DIRX[direction]
            newposy = self.pos[1] + DIRY[direction]
            if newposx < self.world.width and newposx >= 0 and newposy < self.world.height and newposy >= 0:
                break
        return direction

    def move(self):
        newposx = self.pos[0] + DIRX[self.direction]
        newposy = self.pos[1] + DIRY[self.direction]
        self.pos = (newposx, newposy)

    def tick(self, dt):
        self.direction = self.randomDir()
        self.move()


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

    def addAnts(self, nb, pos=None):
        for _ in range(nb):
            self.addAnt(pos)

    def tick(self, dt):
        for ant in self.ants:
            ant.tick(dt)
