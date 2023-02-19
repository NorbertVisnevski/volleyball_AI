import pygame

from controls.control import Control


def mapping1():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        return 3
    elif keys[pygame.K_a]:
        return 1
    elif keys[pygame.K_d]:
        return 2
    else:
        return 0


def mapping2():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_i]:
        return 3
    elif keys[pygame.K_j]:
        return 1
    elif keys[pygame.K_l]:
        return 2
    else:
        return 0


def mapping3():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        return 3
    elif keys[pygame.K_LEFT]:
        return 1
    elif keys[pygame.K_RIGHT]:
        return 2
    else:
        return 0


def mapping4():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP8]:
        return 3
    elif keys[pygame.K_KP4]:
        return 1
    elif keys[pygame.K_KP6]:
        return 2
    else:
        return 0


class KeyboardControls(Control):

    def __init__(self, mapping=1):
        self.last_action = 0
        if mapping == 1:
            self.mapping = mapping1
        if mapping == 2:
            self.mapping = mapping2
        if mapping == 3:
            self.mapping = mapping3
        if mapping == 4:
            self.mapping = mapping4

    def get_action(self, state):
        return self.mapping()
