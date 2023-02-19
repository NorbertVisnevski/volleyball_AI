import pygame
import pymunk

from actors.actor import Actor
from resources import global_variables
from resources.collision import FLOOR_COLLISION_TYPE_A, AGENT_GROUP


class FloorCollision(Actor):

    def __init__(self, space, screen, score, ball, x=0, collision_type=FLOOR_COLLISION_TYPE_A):
        self.space = space
        self.screen = screen
        self.score = score
        self.ball = ball

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        w, h = pygame.display.get_surface().get_size()
        shape = pymunk.Segment(body, (x + 20, 20), (w / 2 - 20 + x, 20), 20)
        shape.collision_type = collision_type
        shape.filter = pymunk.ShapeFilter(AGENT_GROUP)
        space.add(body, shape)

        self.shape = shape
        self.body = body

    def handle_collision(self, arbiter, space, data):
        self.score.score += 1
        self.ball.reset = True
        if self.shape.collision_type == FLOOR_COLLISION_TYPE_A:
            global_variables.active_team = 1
        else:
            global_variables.active_team = 0
        return True
