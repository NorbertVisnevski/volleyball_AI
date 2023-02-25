import csv
import os
import time
import pygame
import pymunk

from actors.agent import Agent
from actors.ball import Ball
from actors.floor import Floor
from actors.floor_collision import FloorCollision
from actors.net import Net
from actors.score import Score
from actors.wall import Wall
from colors import WHITE, BLACK
from controls.epsilon import EpsilonGreedy
from controls.game_environment import GameEnvironment
from controls.keyboard import KeyboardControls
from controls.q_learning import QLearningControls
from controls.reward import calculate_reward_type1
from resources import global_variables
from resources.collision import AGENT_COLLISION_TYPE, BALL_COLLISION_TYPE, FLOOR_COLLISION_TYPE_A, FLOOR_COLLISION_TYPE_B
from resources.fonts import font1

import tensorflow as tf

# def throw_ball(ball, team=0):
#     if not ball.active:
#         ball.activate()
#         if team == 0:
#             ball.body.position = (40, 500)
#             ball.body.velocity = (0, 0)
#             ball.apply_pulse((50, 100))
#         else:
#             w, h = pygame.display.get_surface().get_size()
#             ball.body.position = (w - 40, 500)
#             ball.body.velocity = (0, 0)
#             ball.apply_pulse((-50, 100))
#
#
# def run_game_loop():
#     pygame.init()
#     pygame.display.set_caption('Game')
#
#     clock = pygame.time.Clock()
#
#     screen = pygame.display.set_mode((1920, 1080))
#     space = pymunk.Space()
#     space.gravity = 0, -981
#
#     w, h = pygame.display.get_surface().get_size()
#
#     floor = Floor(space, screen)
#     ceiling = Floor(space, screen, 10_000)
#     ball = Ball(space, screen)
#     net = Net(space, screen)
#     wall1 = Wall(space, screen)
#     wall2 = Wall(space, screen, w)
#
#     score1 = Score(space, screen, (w / 4, h - 100), 0, 0)
#     score2 = Score(space, screen, ((w / 4) * 3, h - 100), 1, 0)
#
#     floor_collision1 = FloorCollision(space, screen, score2, ball, 0, FLOOR_COLLISION_TYPE_A)
#     floor_collision2 = FloorCollision(space, screen, score1, ball, w / 2, FLOOR_COLLISION_TYPE_B)
#
#     collision_handler = space.add_collision_handler(FLOOR_COLLISION_TYPE_A, BALL_COLLISION_TYPE)
#     collision_handler.begin = floor_collision1.handle_collision
#
#     collision_handler = space.add_collision_handler(FLOOR_COLLISION_TYPE_B, BALL_COLLISION_TYPE)
#     collision_handler.begin = floor_collision2.handle_collision
#
#     # collision_handler = space.add_wildcard_collision_handler(FLOOR_COLLISION_TYPE)
#     # collision_handler.begin = floor_collision1.wild_card_handle
#     #
#     # collision_handler = space.add_wildcard_collision_handler(FLOOR_COLLISION_TYPE)
#     # collision_handler.begin = floor_collision2.wild_card_handle
#
#     collision_handler = space.add_collision_handler(AGENT_COLLISION_TYPE, BALL_COLLISION_TYPE)
#     collision_handler.begin = ball.agent_reflect
#
#     agents = [
#         Agent(space, screen, (200, 100), 1),
#         Agent(space, screen, (400, 100), 2),
#         Agent(space, screen, (w - 400, 100), 3),
#         Agent(space, screen, (w - 200, 100), 4)
#     ]
#
#     run = True
#     while run:
#         start_time = time.time()
#         screen.fill(BLACK)
#         net.draw()
#         floor.draw()
#         for agent in agents:
#             agent.draw()
#         ball.draw()
#         for ev in pygame.event.get():
#             if ev.type == pygame.QUIT:
#                 pygame.quit()
#                 return
#             if ev.type == pygame.KEYDOWN:
#                 keys = pygame.key.get_pressed()
#                 if keys[pygame.K_SPACE]:
#                     throw_ball(ball, global_variables.active_team)
#         clock.tick(120)
#         for agent in agents:
#             agent.update()
#         ball.update()
#         space.step(1 / 120)
#
#         end_time = time.time()
#         score1.draw()
#         score2.draw()
#         screen.blit(font1.render(f"Frame time:  {round((end_time - start_time) * 1000, 2)}", True, WHITE), (5, 5))
#
#         pygame.display.update()

draw = False
header = ['avg', 'min', 'max', 'cumulative', 'table_size', 'epsilon', 'episode']


def handle_global_events():
    global draw
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            return
        if ev.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                draw = not draw


def normal_game():
    controllers = [KeyboardControls(i) for i in range(1, 5)]
    game = GameEnvironment()
    while True:
        game.step()
        game.actions = [control.get_action(None) for control in controllers]
        game.draw()
        game.draw_debug()
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return
            if ev.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    game.ball.throw_ball(global_variables.active_team)


def q_learning():
    global draw

    calculate_reward = calculate_reward_type1
    stats = []
    policy = EpsilonGreedy()
    brain = QLearningControls(policy)

    directory = 'stats/test'
    os.makedirs(directory, exist_ok=True)
    episode = 0

    while True:
        episode += 1
        game = GameEnvironment()
        step = game.get_observations()
        actions = [0, 0, 0, 0]
        for iteration in range(1_000_000):
            game.ball.throw_ball(global_variables.active_team)
            for state in step[0]:
                actions.append(brain.get_action(state))
            game.actions = actions
            game.step()
            next_step = game.get_observations()

            calculate_reward(step, actions, next_step, brain)
            brain.learn()
            brain.epsilon_policy.decay()

            step = next_step
            actions = []

            handle_global_events()
            if draw:
                game.draw()
                pygame.display.update()

        stats.append(brain.calculate_stats())
        stats[-1].append(episode)
        with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 100 == 0:
            brain.save(f"{directory}/brain{episode}.json")


if __name__ == '__main__':
    # run_game_loop()
    q_learning()
