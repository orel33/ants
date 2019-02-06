# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from constants import *
from world import *
import random
import numpy
import math

### Class AntBrain ###


class AntBrain:

    def __init__(self, world, colony, ant):
        self.__world = world
        self.__colony = colony
        self.__ant = ant
        # self.__heading = None  # angle in radian relative to the colony position
        self.__targetpos = None
        self.__mode = SEARCH

    def swapMode(self):
        if(self.__mode == SEARCH):
            self.__mode = BACK
        else:
            self.__mode = SEARCH

    def act(self):
        # seach mode
        if self.__mode == SEARCH:
            if self.__targetpos == None or self.__targetpos == self.__ant.pos():
                self.__targetpos = randomPos(self.__world)
            direction = targetPos(self.__world, self.__ant.pos(), self.__targetpos)
            self.__ant.move(direction)
            # if self.__heading == None:
            #     self.__heading = random.random()*2*math.pi
            # direction = targetDir(
            #     self.__world, self.__ant.home(), self.__ant.pos(), self.__heading)
            # ok = self.__ant.move(direction)
            # if not ok:
            #     direction = randomDir(self.__world, self.__ant.pos())
            #     self.__ant.move(direction)
            if self.__ant.onFood():
                self.__ant.takeFood()
                self.swapMode()
                return
            if self.__ant.nearFood():
                pass
            if self.__ant.onPheromone():
                direction = pheromoneDir(self.__world, self.__ant.pos(), self.__ant.home())
                self.__ant.move(direction)
                return
            if self.__ant.nearPheromone():
                pass

        # back mode
        if self.__mode == BACK:
            self.__heading = None
            direction = targetPos(
                self.__world, self.__ant.pos(), self.__ant.home())
            ok = self.__ant.move(direction)
            if not ok:
                return
            self.__ant.dropPheromone()
            if self.__ant.atHome():
                self.__ant.releaseFood()
                self.swapMode()
                return

### Class Ant ###


class Ant:

    def __init__(self, world, colony):
        self.__world = world
        self.__colony = colony
        self.__pos = colony.pos()
        self.__brain = AntBrain(world, colony, self)
        self.__food = 0

    def pos(self):
        return self.__pos

    def food(self):
        return self.__food

    def move(self, direction):
        if direction not in range(NBDIRS):
            return False
        newposx = self.__pos[0] + DIRS[direction][0]
        newposy = self.__pos[1] + DIRS[direction][1]
        newpos = (newposx, newposy)
        if not self.__world.isValidPos(newpos):
            return False
        self.__pos = newpos  # (newposx, newposy)
        return True

    def onFood(self):
        return (self.__world.getFood(self.__pos) > 0)

    def onPheromone(self):
        return (self.__world.getPheromone(self.__pos) > 0)

    def nearFood(self):
        for i in range(NBDIRS):
            neighborpos = (self.__pos[0] + DIRS[i][0],
                           self.__pos[1] + DIRS[i][1])
            if self.__world.isValidPos(neighborpos) and self.__world.getFood(neighborpos) > 0:
                return True
        return False

    def nearPheromone(self):
        for i in range(NBDIRS):
            neighborpos = (self.__pos[0] + DIRS[i][0],
                           self.__pos[1] + DIRS[i][1])
            if self.__world.isValidPos(neighborpos) and self.__world.getPheromone(neighborpos) > 0:
                return True
        return False

    def atHome(self):
        return (self.__pos == self.__colony.pos())

    def home(self):
        return self.__colony.pos()

    def takeFood(self):
        if(self.__food < FOOD_CAPACITY and self.onFood()):
            available = self.__world.getFood(self.__pos)
            need = FOOD_CAPACITY - self.__food
            self.__food = min(available, need)
            self.__world.removeFood(self.__pos, self.__food)
            return True
        return False

    def releaseFood(self):
        if(self.__food > 0 and self.atHome()):
            self.__colony.addFood(self.__food)
            self.__food = 0
            return True
        return False

    def dropPheromone(self):
        self.__world.addPheromone(self.__pos, PHEROMONE_DROP/2)
        for i in range(NBDIRS):
            neighborpos = (self.__pos[0] + DIRS[i][0],
                           self.__pos[1] + DIRS[i][1])
            if self.__world.isValidPos(neighborpos):
                self.__world.addPheromone(neighborpos, PHEROMONE_DROP/16)

    def tick(self, dt):
        self.__brain.act()

### Class AntColony ###


class AntColony:
    def __init__(self, world, pos=None):
        self.__world = world
        if pos == None:
            pos = (int(world.width()/2), int(world.height()/2))
        self.__pos = pos
        self.__ants = []
        self.__food = 0

    def pos(self):
        return self.__pos

    def food(self):
        return self.__food

    def addFood(self, level=1):
        self.__food += level

    def getAnts(self):
        return self.__ants

    def addAnt(self):
        ant = Ant(self.__world, self)
        self.__ants.append(ant)
        return ant

    def addAnts(self, nb):
        for _ in range(nb):
            self.addAnt()

    def tick(self, dt):
        for ant in self.__ants:
            ant.tick(dt)
