import pygame
import pymunk

from actors.actor import Actor
from colors import WHITE, BLACK


class Net(Actor):

    def __init__(self, space, screen):
        self.space = space
        self.screen = screen

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        w, h = pygame.display.get_surface().get_size()
        segment = pymunk.Segment(body, (w/2, h/5), (w/2, 0), 14)
        space.add(body, segment)
        segment.elasticity = 0.05
        self.segment = segment
        self.body = body

    def draw(self):
        w, h = pygame.display.get_surface().get_size()
        a, b = self.get_coordinates()
        pygame.draw.line(self.screen, BLACK, a, b, 8)

    def get_coordinates(self):
        a = self.segment.a
        b = self.segment.b
        w, h = pygame.display.get_surface().get_size()
        return (int(a.x-2), int(h - a.y)), (int(b.x-2), int(h - b.y))
