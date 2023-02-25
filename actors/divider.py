import pygame
import pymunk

from actors.actor import Actor
from colors import WHITE
from resources.collision import DIVIDER_COLLISION_TYPE


class Divider(Actor):

    def __init__(self, space, screen):
        self.space = space
        self.screen = screen

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        w, h = pygame.display.get_surface().get_size()
        segment = pymunk.Segment(body, (w/2, 0), (w/2, h*10), 4)
        space.add(body, segment)
        segment.elasticity = 0
        segment.collision_type = DIVIDER_COLLISION_TYPE
        self.segment = segment
        self.body = body

    def handle_collision(self, arbiter, space, data):
        return False
