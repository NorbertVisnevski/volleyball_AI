import csv
import os

import pygame

from configurations.global_functions import handle_global_events, header
from controls.epsilon import EpsilonGreedy
from controls.game_environment import GameEnvironment
from controls.q_learning import QLearningControls
from controls.reward import calculate_reward_type2
from resources import global_variables

draw = False
def q_learning():
    global draw

    calculate_reward = calculate_reward_type2
    stats = []
    policy = EpsilonGreedy(0.01)
    brain = QLearningControls(policy)

    directory = 'stats/test-4-observation-bigger-precision-resetting-epsilon'
    os.makedirs(directory, exist_ok=True)
    episode = 0

    while True:
        policy.epsilon = 1
        episode += 1
        game = GameEnvironment()
        step = game.get_observations()
        actions = [0, 0, 0, 0]
        for iteration in range(50_000):
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
        if episode % 1000 == 0:
            brain.save(f"{directory}/brain{episode}.json")