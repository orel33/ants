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
        self.__targetpos = None
        self.__mode = SEARCH
        self.__escsteps = 0
        self.__regsteps = 0
        self.__negsteps = 0

    def mode(self):
        return self.__mode

    ### search food ###
    def searchFood(self):
        self.__mode = SEARCH

        # select next direction
        direction = -1
        if self.__ant.nearFood():
            self.__targetpos = None
            direction = foodDir(self.__world, self.__ant.pos())
            # print("I am near food in direction {}".format(direction))
        elif self.__ant.onPheromone():
            self.__targetpos = None
            direction = pheromoneDir(self.__world, self.__ant.pos(), self.__ant.home(), True)
            # print("I follow pheromone in direction {}".format(direction))
        elif self.__ant.nearPheromone():
            self.__targetpos = None
            direction = pheromoneDir(self.__world, self.__ant.pos(), self.__ant.home(), False)
            # print("I'am near pheromone in direction {}".format(direction))
        elif self.__targetpos == None or self.__targetpos == self.__ant.pos():
            self.__escsteps = 0
            self.__targetpos = randomPos(self.__world)
            direction = targetDir(self.__world, self.__ant.pos(), self.__targetpos)
        else:
            direction = targetDir(self.__world, self.__ant.pos(), self.__targetpos)

        # check direction
        if direction == -1:
            self.__regsteps = 0
            self.__negsteps += 1
            direction = randomDir(self.__world, self.__ant.pos())
        else:
            self.__regsteps += 1
            if self.__regsteps == 4:
                self.__negsteps = 0
        # direction = rotateDir(self.__world, self.__ant.pos(), direction)

        # move ant in the selected direction
        self.__ant.move(direction)

        return self.__ant.onFood()

    ### back home ###
    def backHome(self):
        self.__mode = BACK
        direction = -1
        self.__targetpos = None
        direction = targetDir(self.__world, self.__ant.pos(), self.__ant.home())

        if direction == -1:
            # print("I am back to home, but I need an escape!!!")
            self.__regsteps = 0
            self.__negsteps += 1
            direction = randomDir(self.__world, self.__ant.pos())
        else:
            self.__regsteps += 1
            if self.__regsteps == 4:
                self.__negsteps = 0

        # move your body
        if self.__ant.move(direction):
            self.__ant.dropPheromone()

        return self.__ant.atHome()

    ### search escape ###
    def searchEscape(self):
        self.__mode = ESCAPE
        direction = -1

        if self.__escsteps == 0 or self.__targetpos == None: # or self.__targetpos == self.__ant.pos():
            self.__targetpos = randomPos(self.__world)

        direction = targetDir(self.__world, self.__ant.pos(), self.__targetpos)

        # if direction == -1:
        #     self.__targetpos = None
        #     print("I need a better escape !!!!")

        # direction = rotateDir(self.__world, self.__ant.pos(), direction)

        if direction == -1:
            direction = randomDir(self.__world, self.__ant.pos())

        # move your body
        self.__ant.move(direction)
        self.__escsteps += 1

        if self.__escsteps == MAX_STEP:
            return True

        return False


    def act(self):

        # seach mode
        if self.__mode == SEARCH:
            if self.searchFood():
                self.__ant.takeFood()
                self.__mode = BACK
            elif self.__negsteps >= 4:
                print("I need to escape !!!")
                self.__escsteps = 0
                self.__mode = ESCAPE
            return

        # back mode
        if self.__mode == BACK:
            if self.backHome():
                self.__ant.releaseFood()
                self.__mode = SEARCH
            elif self.__negsteps >= 4:
                print("I need to escape !!!")
                self.__escsteps = 0
                self.__mode = ESCAPE
            return

        # escape mode
        if self.__mode == ESCAPE:
            if self.searchEscape():
                self.__escsteps = 0
                self.__negsteps = 0
                self.__regsteps = 0
                if self.__ant.food() > 0:
                    self.__mode = BACK
                else:
                    self.__mode = SEARCH
            return

### Class Ant ###

class Ant:

    def __init__(self, world, colony):
        self.__world = world
        self.__colony = colony
        self.__pos = colony.pos()
        self.__brain = AntBrain(world, colony, self)
        self.__food = 0

    def brain(self):
        return self.__brain

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
        self.__pos = newpos
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
        print("=> add colony home at position ({},{})".format(
            pos[0], pos[1]))

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
