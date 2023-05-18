import pygame

from controls.control import Control


def mapping1():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        return 2
    elif keys[pygame.K_a]:
        return 0
    elif keys[pygame.K_d]:
        return 1
    else:
        return 99


def mapping2():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_i]:
        return 2
    elif keys[pygame.K_j]:
        return 0
    elif keys[pygame.K_l]:
        return 1
    else:
        return 99


def mapping3():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        return 2
    elif keys[pygame.K_LEFT]:
        return 1
    elif keys[pygame.K_RIGHT]:
        return 0
    else:
        return 99


def mapping4():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP8]:
        return 2
    elif keys[pygame.K_KP4]:
        return 1
    elif keys[pygame.K_KP6]:
        return 0
    else:
        return 99


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
