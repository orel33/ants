# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

### Constants ###

DEBUG = 0

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

# ant states
UNDEFINED = 0
FIRST_STEP = 1
NEAR_FOOD = 2
ON_PHEROMONE = 3
NEAR_PHEROMONE = 4
TARGET_REACHED = 5
NO_TARGET = 6
ON_WAY = 7

STATES = ["undefined", "first step", "near food", "on pheromone", "near pheromone", "target reached", "no target", "on way"]


# ant brain parameters
PHEROMONE_DROP = 450
FOOD_CAPACITY = 1
MAX_PHEROMONE = 1200
DECAY_PHEROMONE = 2
MAX_ESCAPE_STEPS = 20
LOCAL_SEARCH_DIST = 4
