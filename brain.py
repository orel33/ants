# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from constants import *
from geom import *
from world import *
from ants import *
import random
import numpy
import math


### Class AntBrain ###


class Brain:

    def __init__(self, world, colony, ant):
        self.__world = world
        self.__colony = colony
        self.__ant = ant
        self.__mode = SEARCH        # current mode in [SEARCH, BACK, ESCAPE]
        self.__state = UNDEFINED    # current ant state
        self.__steps = 0            # nb steps done in current mode
        self.__lastpos = None       # last ant position
        self.__targetpos = None     # set target position
        self.__enabledrop = True    # enable to drop pheromone (or not)


    def mode(self):
        return self.__mode

    def setMode(self, mode):
        self.__mode = mode
        self.__state = UNDEFINED
        self.__steps = 0
        self.__targetpos = None

    ### search food ###
    def searchFood(self):
        self.__mode = SEARCH

        # select next direction
        direction = -1
        if self.__ant.nearFood():
            self.__targetpos = None
            self.__state = NEAR_FOOD
            direction = foodDir(self.__world, self.__ant.pos())
            print("I am near food in direction {}".format(direction))
        elif self.__ant.onPheromone():
            self.__state = ON_PHEROMONE
            self.__targetpos = None
            direction = pheromoneDir(
                self.__world, self.__ant.pos(), self.__ant.home(), True)
            print("I follow pheromone in direction {}".format(direction))
        elif self.__ant.nearPheromone():
            self.__state = NEAR_PHEROMONE
            self.__targetpos = None
            direction = pheromoneDir(
                self.__world, self.__ant.pos(), self.__ant.home(), False)
            print("I'am near pheromone in direction {}".format(direction))
        # global search
        elif self.__steps == 0:
            self.__state = FIRST_STEP
            print("I setup new target position for global search...")
            self.__targetpos = randomTargetPos(self.__world, self.__ant.pos())
            direction = targetDir(self.__world, self.__ant.pos(), self.__targetpos)
        # local search
        elif self.__targetpos == self.__ant.pos():
            self.__state = TARGET_REACHED
            print("Target reached!!! I setup new target position for local search...")
            self.__targetpos = randomTargetPos(self.__world, self.__ant.pos(), LOCAL_SEARCH_DIST)
            direction = targetDir(self.__world, self.__ant.pos(), self.__targetpos)
        # local search
        elif self.__targetpos == None:
            self.__state = NO_TARGET
            print("No target anymore!!! I setup new target position for local search...")
            self.__targetpos = randomTargetPos(self.__world, self.__ant.pos(), LOCAL_SEARCH_DIST)
            direction = targetDir(self.__world, self.__ant.pos(), self.__targetpos)
        else:
            self.__state = ON_WAY
            # I am moving to a target position
            direction = targetDir(self.__world, self.__ant.pos(), self.__targetpos)

        # check direction
        if direction ==  -1:
            print("Why direction -1 with ant state \"{}\"?".format(STATES[self.__state]))
            # if no more pheromone...
            if self.__state == ON_PHEROMONE:
                print("Fail to follow pheromone... I choose a random direction!")
                direction = randomDir(self.__world, self.__ant.pos())

        return direction

    ### back home ###
    def backHome(self):
        self.__mode = BACK
        direction = -1
        self.__targetpos = None
        direction = targetDir(
            self.__world, self.__ant.pos(), self.__ant.home())
        return direction


    ### search escape ###
    def searchEscape(self):
        self.__mode = ESCAPE
        direction = -1
        if self.__steps == 0:
            self.__targetpos = randomTargetPos(self.__world, self.__ant.pos())
        direction = targetDir(self.__world, self.__ant.pos(), self.__targetpos)
        return direction

    def endEscape(self):
        if self.__steps == MAX_ESCAPE_STEPS:
            return True
        return False

    def act(self):

        # save last position
        self.__lastpos = self.__ant.pos()

        # seach mode
        if self.__mode == SEARCH:
            direction = self.searchFood()
            if self.__ant.move(direction):
                self.__steps += 1
                if self.__ant.onFood():
                    self.__ant.takeFood()
                    self.setMode(BACK)
            else:
                # self.setMode(ESCAPE)
                print("oups, I cannot move in this direction...")
                self.setMode(SEARCH)

        # back mode
        elif self.__mode == BACK:
            direction = self.backHome()
            if self.__ant.move(direction):
                self.__steps += 1
                if self.__enabledrop:
                    self.__ant.dropPheromone()
                if self.__ant.atHome():
                    self.__ant.releaseFood()
                    self.setMode(SEARCH)
            else:
                self.setMode(ESCAPE)

        # escape mode
        elif self.__mode == ESCAPE:
            direction = self.searchEscape()
            if self.__ant.move(direction):
                self.__steps += 1
                if(self.endEscape()):
                    if self.__ant.food() > 0:
                        self.__enabledrop = False # disable pheromone drop
                        self.setMode(BACK)
                    else:
                        self.__enabledrop = True # enable pheromone drop
                        self.setMode(SEARCH)
            else:
                self.setMode(ESCAPE)    # try to escape again

