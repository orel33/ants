# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from constants import DEBUG

### Misc ###

def debug(value):
    if DEBUG == 1:
        print(value)
