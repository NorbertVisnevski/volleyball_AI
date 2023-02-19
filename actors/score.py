import pygame

from actors.actor import Actor
from colors import WHITE, RED
from resources import global_variables
from resources.fonts import font4


class Score(Actor):

    def __init__(self, space, screen, position=(0, 0), team=0, score=0):
        self.space = space
        self.screen = screen
        self.position = position
        self.score = score
        self.team = team

    def draw(self):
        self.screen.blit(font4.render(str(self.score), True, WHITE), self.get_coordinates())
        if self.team == global_variables.active_team:
            x, y = self.get_coordinates()
            pygame.draw.circle(self.screen, RED, (x - 32, y + 42), 12)

    def get_coordinates(self):
        a = self.position[0]
        b = self.position[1]
        w, h = pygame.display.get_surface().get_size()
        return int(a), int(h - b)
