import pygame
import pymunk

from actors.actor import Actor
from colors import RED
from controls.keyboard import KeyboardControls
from resources.collision import AGENT_GROUP, AGENT_COLLISION_TYPE
from resources.fonts import font2


class Agent(Actor):

    def __init__(self, space, screen, position=(0, 0), player=1):
        self.space = space
        self.screen = screen
        self.player = player

        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = position
        shape = pymunk.Poly.create_box(body, (40, 120))
        shape.density = 1
        shape.friction = 0.1
        shape.elasticity = 0.01
        shape.mass = 15
        shape.filter = pymunk.ShapeFilter(AGENT_GROUP)
        shape.collision_type = AGENT_COLLISION_TYPE
        space.add(body, shape)
        self.shape = shape
        self.body = body

    def draw(self):
        x, y = self.get_coordinates()
        pygame.draw.rect(self.screen, RED, pygame.Rect(x - 20, y - 60, 40, 120), 1)
        self.screen.blit(font2.render(str(self.player), True, RED), (x - 6, y))

    def get_coordinates(self):
        w, h = pygame.display.get_surface().get_size()
        point = self.body.position
        return int(point.x), int(h - point.y)

    def get_normalized_coordinates(self):
        w, h = pygame.display.get_surface().get_size()
        point = self.body.position
        if self.player == 1 or self.player == 2:
            return min((point.x / (w / 2)), 1), min((point.y / (h / 3)), 1.0)
        else:
            return 1-min(((point.x - (w / 2)) / (w - (w / 2))), 1), min((point.y / (h / 3)), 1)

    def update(self, action):
        if action == 1:
            self.body.apply_impulse_at_local_point((-100, 0))
        elif action == 2:
            self.body.apply_impulse_at_local_point((100, 0))
        elif action == 3:
            if self.body.position.y < 91 and abs(self.body.velocity.y) < 0.5:
                self.body.apply_impulse_at_local_point((0, 10_000))
        self.body.angle = 0
