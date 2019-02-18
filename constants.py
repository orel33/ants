# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

### Debug ###

DEBUG = 0

### Directions ###

NBDIRS = 8

# This array contains the 8 directions. They are clockwise ordered.
# Direction 0 corresponds to the NW, i.e. going up (-1) and to the left (-1).

DIRS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
STRDIRS = ["NW", "N", "NE", "E", "SE", "S", "SW", "W"]

### World & Colony Parameters ###

WIDTH = 120
HEIGHT = 120
NBANTS = 100
NTURNS = 0      # infinite turns

### Ant Parameters ###

PHEROMONE_DROP = 450
FOOD_CAPACITY = 1
MAX_PHEROMONE = 1200
DECAY_PHEROMONE = 2

# EOF
