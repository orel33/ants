# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

import pygame

### Class KeyboardController ###

class KeyboardController:

    def __init__(self):
        pygame.key.set_repeat(1,200) # repeat keydown events every 200ms

    def tick(self, dt):

        # process all keyboard & window events
        for event in pygame.event.get():
            cont = True
            if event.type == pygame.QUIT:
                cont = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                cont = False
            # don't continue?
            if not cont: return False

        return True
