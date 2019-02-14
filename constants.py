# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

### Directions ###

# This array contains the 8 directions. They are clockwise
# ordered. Direction 0 corresponds to going up and to the left.
DIRS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
NBDIRS = 8

### World Parameters ###

WIDTH = 120
HEIGHT = 120

### Colony Parameters ###

NBANTS = 1

### Ant Parameters ###

PHEROMONE_DROP = 450
FOOD_CAPACITY = 1
MAX_PHEROMONE = 1200
DECAY_PHEROMONE = 2

# EOF