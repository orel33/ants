# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

### Debug ###

DEBUG = 1

### Directions ###

# This array contains the 8 directions. They are clockwise
# ordered. Direction 0 corresponds to going up (-1) and to the left (-1).
DIRS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
NBDIRS = 8

### World & Colony Parameters ###

WIDTH = 120
HEIGHT = 120
NBANTS = 1

### Ant Parameters ###

PHEROMONE_DROP = 450
FOOD_CAPACITY = 1
MAX_PHEROMONE = 1200
DECAY_PHEROMONE = 20

# EOF
