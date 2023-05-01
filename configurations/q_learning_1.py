import csv
import os

import pygame

from configurations.global_functions import header, GlobalFunctions
from controls.epsilon import EpsilonGreedy
from controls.game_environment import GameEnvironment
from controls.q_learning import QLearningControls
from controls.reward import calculate_reward_type2, calculate_reward_1side_type8
from resources import global_variables

draw = False
# def q_learning():
#     global draw
#
#     calculate_reward = calculate_reward_type2
#     stats = []
#     policy = EpsilonGreedy(0.01)
#     brain = QLearningControls(policy)
#
#     directory = 'stats/test-4-observation-bigger-precision-resetting-epsilon'
#     os.makedirs(directory, exist_ok=True)
#     episode = 0
#
#     while True:
#         policy.epsilon = 1
#         episode += 1
#         game = GameEnvironment()
#         step = game.get_observations()
#         actions = [0, 0, 0, 0]
#         for iteration in range(50_000):
#             game.ball.throw_ball(global_variables.active_team)
#             for state in step[0]:
#                 actions.append(brain.get_action(state))
#             game.actions = actions
#             game.step()
#             next_step = game.get_observations()
#
#             calculate_reward(step, actions, next_step, brain)
#             brain.learn()
#             brain.epsilon_policy.decay()
#
#             step = next_step
#             actions = []
#
#             handle_global_events()
#             if draw:
#                 game.draw()
#                 pygame.display.update()
#
#         stats.append(brain.calculate_stats())
#         stats[-1].append(episode)
#         with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(header)
#             writer.writerows(stats)
#         if episode % 1000 == 0:
#             brain.save(f"{directory}/brain{episode}.json")

def q_learning_self_play():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type8
    stats = []
    policy = EpsilonGreedy(0.05)
    brain = QLearningControls(policy)

    directory = f"stats/self-play"
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(1000):
        episode += 1
        game = GameEnvironment()
        step = game.get_observations()
        actions = [0, 0, 0, 0]
        for iteration in range(500_000):
            game.ball.throw_ball(1)
            for state in step[0]:
                actions.append(brain.get_action(state))
            game.actions = actions
            game.step()
            next_step = game.get_observations()

            calculate_reward(step, actions, next_step, brain)
            brain.learn()

            step = next_step
            actions = []

            global_events.handle_global_events()
            if global_events.draw:
                game.draw()
                pygame.display.update()

        brain.epsilon_policy.decay()
        stats.append([*brain.calculate_stats(), game.score1.score, game.score2.score, episode])
        print(stats[-1])
        with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 200 == 0:
            brain.save(f"{directory}/brain{episode}.json")