import os

import pygame

from configurations.global_functions import GlobalFunctions
from controls.epsilon import EpsilonGreedy
from controls.game_environment import GameEnvironment
from controls.q_learning import QLearningControls2
from controls.reward import calculate_reward_1side_type5


def demonstration():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type5
    stats = []
    policy = EpsilonGreedy(0.001)
    policy.epsilon = 0.3
    brain = QLearningControls2(policy)
    brain.load(f"stats/q-1side-1-reward5-0.5M-team-ball-static-E-0.2/brain8000.json")

    directory = f"stats/simplified21"
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(15_000):
        episode += 1
        game = GameEnvironment()
        step = game.get_observations()
        actions = [0, 0, 0, 0]
        for iteration in range(100_000):
            game.ball.throw_ball(1)
            for state in step[0]:
                actions.append(brain.get_action(state))
            game.actions = actions
            game.step()
            next_step = game.get_observations()


            step = next_step
            actions = []

            global_events.handle_global_events()
            game.draw()
            pygame.display.update()