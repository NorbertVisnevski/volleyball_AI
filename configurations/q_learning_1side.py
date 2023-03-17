import csv
import os

import pygame

from configurations.global_functions import header, GlobalFunctions
from controls.epsilon import EpsilonGreedy
from controls.game_environment import GameEnvironment, GameEnvironmentOneSide
from controls.q_learning import QLearningControls, QLearningControls2
from controls.reward import calculate_reward_type2, calculate_reward_1side_type1, calculate_reward_1side_type2
from resources import global_variables

draw = True
def q_learning_1side():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type2
    stats = []
    policy = EpsilonGreedy(0.01)
    brain = QLearningControls2(policy)

    directory = 'stats/q-1side-1-reward2'
    os.makedirs(directory, exist_ok=True)
    episode = 0

    while True:
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(50_000):
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
        stats.append(brain.calculate_stats())
        stats[-1].append(episode)
        with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 1000 == 0:
            brain.save(f"{directory}/brain{episode}.json")