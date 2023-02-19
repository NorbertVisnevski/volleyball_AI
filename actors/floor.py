import pygame
import pymunk

from actors.actor import Actor
from colors import GREEN


class Floor(Actor):

    def __init__(self, space, screen, y=20):
        self.space = space
        self.screen = screen

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        w, h = pygame.display.get_surface().get_size()
        shape = pymunk.Segment(body, (20, y), (w - 20, y), 10)
        space.add(body, shape)
        shape.elasticity = 0.1
        shape.friction = 1
        self.shape = shape
        self.body = body

    def draw(self):
        a, b = self.get_coordinates()
        pygame.draw.line(self.screen, GREEN, a, b, 4)

    def get_coordinates(self):
        a = self.shape.a
        b = self.shape.b
        w, h = pygame.display.get_surface().get_size()
        return (int(a.x), int(h - a.y-6)), (int(b.x), int(h - b.y-6))
