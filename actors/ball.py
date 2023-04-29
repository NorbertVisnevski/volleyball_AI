import random

import pygame
import pymunk

from actors.actor import Actor
from colors import RED
from resources.collision import BALL_COLLISION_TYPE


class Ball(Actor):

    def __init__(self, space, screen, position=(0, 0)):
        self.space = space
        self.screen = screen

        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = position
        shape = pymunk.Circle(body, 20)
        shape.density = 1
        shape.elasticity = 8
        shape.mass = 0.1
        shape.filter = pymunk.ShapeFilter(BALL_COLLISION_TYPE)
        shape.collision_type = BALL_COLLISION_TYPE
        space.add(body, shape)
        self.shape = shape
        self.body = body

        self.reflect_y = 600
        self.reflect_x = 500
        self.sleep()
        self.reset = False
        self.active = False
        self.throw_presets = [
            (50, 100),
            (100, 50),
            (150, 20),
            (90, 60),
            (60, 90),
            (80, 80),
            (90, 40),
            (75, 75)
        ]
        self.reflect_presets = [
            (500, 600),
            (600, 500),
            (600, 400),
            (400, 600),
        ]

    def draw(self):
        pygame.draw.circle(self.screen, RED, self.get_coordinates(), 20, width=5)

    def update(self):
        # print(self.body.velocity)
        if self.reset:
            self.sleep()
            self.reset = False

    def get_coordinates(self):
        w, h = pygame.display.get_surface().get_size()
        point = self.body.position
        return int(point.x), int(h - point.y)

    def get_normalized_coordinates(self):
        w, h = pygame.display.get_surface().get_size()
        point = self.body.position
        return min((point.x / w), 1), min((point.y / h), 1)

    def get_normalized_coordinates_by_team(self):
        w, h = pygame.display.get_surface().get_size()
        point = self.body.position
        t1_x = min((point.x / (w / 2)), 1)
        t2_x = min(((w - point.x) / (w / 2)), 1)
        y = min((point.y / h), 1)
        return t1_x, t2_x, y

    def get_normalized_velocity(self):
        return min(abs(self.body.velocity.x) / 1500, 1)

    def apply_pulse(self, pulse):
        self.body.apply_impulse_at_local_point(pulse)

    def agent_reflect(self, arbiter, space, data):
        agent_shape = arbiter.shapes[0]
        agent_body = agent_shape.body
        position = self.body.position
        w, h = pygame.display.get_surface().get_size()

        reflect_x, reflect_y = random.choice(self.reflect_presets)

        additional_y = max(0, agent_shape.surface_velocity.y * 2)
        y = reflect_y + additional_y + agent_body.position.y

        if position.x < w / 2:
            additional_x = max(0, agent_shape.surface_velocity.x * 2)
            x = reflect_x + additional_x
        else:
            additional_x = min(0, agent_shape.surface_velocity.x * 2)
            x = -reflect_x + additional_x

        self.body.velocity = (x, y)
        return True

    def sleep(self):
        w, h = pygame.display.get_surface().get_size()
        self.body.velocity = (0, 0)
        self.body.position = (w / 2, 11_000)
        self.active = False

    def activate(self):
        self.active = True

    def throw_ball(self, team=0):
        if not self.active:
            self.activate()
            self.body.velocity = (0, 0)
            pulse = random.choice(self.throw_presets)
            # pulse = self.throw_presets[0]
            if team == 0:
                self.body.position = (40, 500)
                self.apply_pulse(pulse)
            else:
                w, h = pygame.display.get_surface().get_size()
                self.body.position = (w - 40, 500)
                self.apply_pulse((-pulse[0], pulse[1]))
