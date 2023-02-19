import pygame
import pymunk

from actors.actor import Actor
from colors import GREEN


class Wall(Actor):

    def __init__(self, space, screen, x=0):
        self.space = space
        self.screen = screen

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        w, h = pygame.display.get_surface().get_size()
        shape = pymunk.Segment(body, (x, 0), (x, h * 10), 10)
        space.add(body, shape)
        shape.elasticity = 0.1
        shape.friction = 1
        self.shape = shape
        self.body = body

    def draw(self):
        a, b = self.get_coordinates()
        pygame.draw.line(self.screen, GREEN, a, b, 20)

    def get_coordinates(self):
        a = self.shape.a
        b = self.shape.b
        w, h = pygame.display.get_surface().get_size()
        return (int(a.x), int(h - a.y)), (int(b.x), int(h - b.y))
