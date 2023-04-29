import time

import pygame
import pymunk

from actors.agent import Agent
from actors.ball import Ball
from actors.divider import Divider
from actors.floor import Floor
from actors.floor_collision import FloorCollision
from actors.net import Net
from actors.score import Score
from actors.wall import Wall
from colors import BLACK, WHITE
from resources import global_variables
from resources.collision import FLOOR_COLLISION_TYPE_A, BALL_COLLISION_TYPE, FLOOR_COLLISION_TYPE_B, AGENT_COLLISION_TYPE, DIVIDER_COLLISION_TYPE
from resources.fonts import font1


class GameEnvironment:

    def reset(self):
        pygame.init()
        pygame.display.set_caption('Game')

        self.clock = pygame.time.Clock()

        screen = pygame.display.set_mode((1920, 1080))
        self.screen = screen
        space = pymunk.Space()
        self.space = space
        space.gravity = 0, -981

        w, h = pygame.display.get_surface().get_size()

        floor = Floor(space, screen)
        self.floor = floor
        ceiling = Floor(space, screen, 10_000)
        self.ceiling = ceiling
        ball = Ball(space, screen)
        self.ball = ball
        net = Net(space, screen)
        self.net = net
        wall1 = Wall(space, screen)
        self.wall1 = wall1
        wall2 = Wall(space, screen, w)
        self.wall2 = wall2
        divider = Divider(space, screen)
        self.divider = divider

        score1 = Score(space, screen, (w / 4, h - 100), 0, 0)
        self.score1 = score1
        score2 = Score(space, screen, ((w / 4) * 3, h - 100), 1, 0)
        self.score2 = score2

        floor_collision1 = FloorCollision(space, screen, score2, ball, 0, FLOOR_COLLISION_TYPE_A)
        floor_collision2 = FloorCollision(space, screen, score1, ball, w / 2, FLOOR_COLLISION_TYPE_B)

        collision_handler = space.add_collision_handler(FLOOR_COLLISION_TYPE_A, BALL_COLLISION_TYPE)
        collision_handler.begin = floor_collision1.handle_collision

        collision_handler = space.add_collision_handler(FLOOR_COLLISION_TYPE_B, BALL_COLLISION_TYPE)
        collision_handler.begin = floor_collision2.handle_collision

        collision_handler = space.add_collision_handler(AGENT_COLLISION_TYPE, BALL_COLLISION_TYPE)
        collision_handler.begin = ball.agent_reflect

        collision_handler = space.add_collision_handler(BALL_COLLISION_TYPE, DIVIDER_COLLISION_TYPE)
        collision_handler.begin = divider.handle_collision

        agents = [
            Agent(space, screen, (200, 100), 1),
            Agent(space, screen, (400, 100), 2),
            Agent(space, screen, (w - 400, 100), 3),
            Agent(space, screen, (w - 200, 100), 4)
        ]
        self.agents = agents

    def __init__(self, reset=True):
        self.draw_time = None
        self.update_time = None
        self.clock = None
        self.score2 = None
        self.score1 = None
        self.wall2 = None
        self.wall1 = None
        self.net = None
        self.ball = None
        self.ceiling = None
        self.floor = None
        self.space = None
        self.agents = None
        self.screen = None
        self.divider = None
        self.actions = [0, 0, 0, 0]
        if reset:
            self.reset()

    def get_observations_type1(self):
        a1 = self.agents[0]
        a2 = self.agents[1]
        a3 = self.agents[2]
        a4 = self.agents[3]
        a1_x, a1_y = a1.get_normalized_coordinates()
        a2_x, a2_y = a2.get_normalized_coordinates()
        a3_x, a3_y = a3.get_normalized_coordinates()
        a4_x, a4_y = a4.get_normalized_coordinates()
        b_x, b_y = self.ball.get_normalized_coordinates()
        a1_o = [a1_x, a1_y, a2_x, a2_y, b_x, b_y]
        a2_o = [a2_x, a2_y, a1_x, a1_y, b_x, b_y]
        a3_o = [a3_x, a3_y, a4_x, a4_y, 1-b_x, b_y]
        a4_o = [a4_x, a4_y, a3_x, a3_y, 1-b_x, b_y]
        return [[a1_o, a2_o, a3_o, a4_o], self.score1.score, self.score2.score]

    def get_observations_type2(self):
        a1 = self.agents[0]
        a2 = self.agents[1]
        a3 = self.agents[2]
        a4 = self.agents[3]
        a1_x, a1_y = a1.get_normalized_coordinates()
        a2_x, a2_y = a2.get_normalized_coordinates()
        a3_x, a3_y = a3.get_normalized_coordinates()
        a4_x, a4_y = a4.get_normalized_coordinates()
        b_x, b_y = self.ball.get_normalized_coordinates()
        a1_o = [a1_x, a2_x, b_x, b_y]
        a2_o = [a2_x, a1_x, b_x, b_y]
        a3_o = [a3_x, a4_x, 1-b_x, b_y]
        a4_o = [a4_x, a3_x, 1-b_x, b_y]
        return [[a1_o, a2_o, a3_o, a4_o], self.score1.score, self.score2.score]

    def get_observations(self):
        return self.get_observations_type2()

    def set_actions(self, actions):
        self.actions = actions

    def step(self):
        start_time = time.time()

        for i, agent in enumerate(self.agents):
            agent.update(self.actions[i])
        self.ball.update()
        self.space.step(1 / 120)

        end_time = time.time()
        self.update_time = end_time - start_time

    def draw(self):
        start_time = time.time()
        self.screen.fill(WHITE)
        self.net.draw()
        self.floor.draw()
        for agent in self.agents:
            agent.draw()
        self.ball.draw()
        self.score1.draw()
        self.score2.draw()
        self.clock.tick(120)

        end_time = time.time()
        self.draw_time = end_time - start_time

    def draw_debug(self):
        self.screen.blit(font1.render(f"Update time:  {round(self.update_time * 1000, 2)}", True, BLACK), (5, 10))
        self.screen.blit(font1.render(f"Draw time:  {round(self.draw_time * 1000, 2)}", True, BLACK), (5, 30))
        self.screen.blit(font1.render(f"Frame time:  {round((self.update_time + self.draw_time) * 1000, 2)}", True, BLACK), (5, 50))

    def run_normal_gameplay(self):
        run = True
        while run:
            start_time = time.time()
            self.screen.fill(BLACK)
            self.net.draw()
            self.floor.draw()
            for agent in self.agents:
                agent.draw()
            self.ball.draw()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    return
                if ev.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        self.ball.throw_ball(global_variables.active_team)
            self.clock.tick(120)
            for i, agent in enumerate(self.agents):
                agent.update(self.actions[i])
            self.ball.update()
            self.space.step(1 / 120)

            end_time = time.time()
            self.score1.draw()
            self.score2.draw()
            self.screen.blit(font1.render(f"Frame time:  {round((end_time - start_time) * 1000, 2)}", True, WHITE), (5, 5))

            pygame.display.update()



class GameEnvironmentOneSide(GameEnvironment):
    def reset(self):
        pygame.init()
        pygame.display.set_caption('Game')

        self.clock = pygame.time.Clock()

        screen = pygame.display.set_mode((1920, 1080))
        self.screen = screen
        space = pymunk.Space()
        self.space = space
        space.gravity = 0, -981

        w, h = pygame.display.get_surface().get_size()

        floor = Floor(space, screen)
        self.floor = floor
        ceiling = Floor(space, screen, 10_000)
        self.ceiling = ceiling
        ball = Ball(space, screen)
        self.ball = ball
        net = Net(space, screen)
        self.net = net
        wall1 = Wall(space, screen)
        self.wall1 = wall1
        wall2 = Wall(space, screen, w)
        self.wall2 = wall2
        divider = Divider(space, screen)
        self.divider = divider

        score1 = Score(space, screen, (w / 4, h - 100), 0, 0)
        self.score1 = score1
        score2 = Score(space, screen, ((w / 4) * 3, h - 100), 1, 0)
        self.score2 = score2

        floor_collision1 = FloorCollision(space, screen, score2, ball, 0, FLOOR_COLLISION_TYPE_A)
        floor_collision2 = FloorCollision(space, screen, score1, ball, w / 2, FLOOR_COLLISION_TYPE_B)

        collision_handler = space.add_collision_handler(FLOOR_COLLISION_TYPE_A, BALL_COLLISION_TYPE)
        collision_handler.begin = floor_collision1.handle_collision

        collision_handler = space.add_collision_handler(FLOOR_COLLISION_TYPE_B, BALL_COLLISION_TYPE)
        collision_handler.begin = floor_collision2.handle_collision

        collision_handler = space.add_collision_handler(AGENT_COLLISION_TYPE, BALL_COLLISION_TYPE)
        collision_handler.begin = ball.agent_reflect

        collision_handler = space.add_collision_handler(BALL_COLLISION_TYPE, DIVIDER_COLLISION_TYPE)
        collision_handler.begin = divider.handle_collision

        agents = [
            Agent(space, screen, (200, 100), 1),
            Agent(space, screen, (400, 100), 2),
        ]
        self.agents = agents

    def __init__(self):
        super().__init__(reset=False)
        self.reset()

    def get_observations_type1(self):
        a1 = self.agents[0]
        a2 = self.agents[1]
        a1_x, a1_y = a1.get_normalized_coordinates()
        a2_x, a2_y = a2.get_normalized_coordinates()
        b_x, b_y = self.ball.get_normalized_coordinates()
        a1_o = [a1_x, a1_y, a2_x, a2_y, b_x, b_y]
        a2_o = [a2_x, a2_y, a1_x, a1_y, b_x, b_y]
        return [[a1_o, a2_o], self.score1.score, self.score2.score]

    def get_observations_type2(self):
        a1 = self.agents[0]
        a2 = self.agents[1]
        a1_x, a1_y = a1.get_normalized_coordinates()
        a2_x, a2_y = a2.get_normalized_coordinates()
        b_x, b_y = self.ball.get_normalized_coordinates()
        b_x_v = self.ball.get_normalized_velocity()
        a1_o = [a1_x, a1_y, a2_x, a2_y, b_x, b_y, b_x_v]
        a2_o = [a2_x, a2_y, a1_x, a1_y, b_x, b_y, b_x_v]
        return [[a1_o, a2_o], self.score1.score, self.score2.score]

    def get_observations_type3(self):
        a1 = self.agents[0]
        a2 = self.agents[1]
        a1_x, a1_y = a1.get_normalized_coordinates()
        a2_x, a2_y = a2.get_normalized_coordinates()
        bt1_x, bt2_x, b_y = self.ball.get_normalized_coordinates_by_team()
        b_x_v = self.ball.get_normalized_velocity()
        a1_o = [a1_x, a1_y, a2_x, a2_y, bt1_x, b_y, b_x_v]
        a2_o = [a2_x, a2_y, a1_x, a1_y, bt1_x, b_y, b_x_v]
        return [[a1_o, a2_o], self.score1.score, self.score2.score]

    def get_observations_type4(self):
        a1 = self.agents[0]
        a2 = self.agents[1]

        a1_x, a1_y, a1_j = a1.get_normalized_coordinates()
        a2_x, a2_y, a2_j = a2.get_normalized_coordinates()

        bt1_x, bt2_x, b_y = self.ball.get_normalized_coordinates_by_team()
        b_x_v = self.ball.get_normalized_velocity()

        a1_o = [a1_x, a1_y, a1_j, a2_x, a2_y, bt1_x, b_y, b_x_v]
        a2_o = [a2_x, a2_y, a2_j, a1_x, a1_y, bt1_x, b_y, b_x_v]

        return [[a1_o, a2_o], self.score1.score, self.score2.score]

    def get_observations_type5(self):
        a1 = self.agents[0]
        a2 = self.agents[1]

        a1_x, a1_y, a1_j = a1.get_normalized_coordinates()
        a2_x, a2_y, a2_j = a2.get_normalized_coordinates()

        b_x, b_y = self.ball.get_normalized_coordinates()
        b_x_v = self.ball.get_normalized_velocity()

        a1_o = [a1_x, a1_j, a2_x, b_x, b_y, b_x_v]
        a2_o = [a2_x, a2_j, a1_x, b_x, b_y, b_x_v]

        return [[a1_o, a2_o], self.score1.score, self.score2.score]

    def get_observations(self):
        return self.get_observations_type5()