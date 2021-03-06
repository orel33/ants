# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from constants import *

### Misc ###

def debug(value):
    if DEBUG == 1:
        print(value)


def strdir(direction):
        if direction not in range(NBDIRS):
                return "?"
        return STRDIRS[direction]

