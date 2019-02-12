# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

### Constants ###

# This array contains the 8 directions. They are clockwise
# ordered. Direction 0 corresponds to going up and to the left.
DIRS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
NBDIRS = 8

PROBA = [1/2, 1/4, 1/8, 1/8, 0]
PROBASUM = [0.5, 0.75, 0.875, 1.0, 1.0]

# ant brain mode 
SEARCH = 0
BACK = 1
ESCAPE = 2

# ant brain parameters
PHEROMONE_DROP = 450
FOOD_CAPACITY = 1
MAX_PHEROMONE = 1200
DECAY_PHEROMONE = 2
MAX_STEP = 50