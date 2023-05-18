import csv
import os

import pygame

from configurations.global_functions import header, GlobalFunctions
from controls.deep_q_learning import DeepQLearningControls
from controls.epsilon import EpsilonGreedy, EpsilonGreedyDecreasing
from controls.game_environment import GameEnvironment, GameEnvironmentOneSide
from controls.keyboard import KeyboardControls
from controls.q_learning import QLearningControls, QLearningControls2, QLearningHyperParameters
from controls.reward import calculate_reward_type2, calculate_reward_1side_type1, calculate_reward_1side_type2, calculate_reward_1side_type3, calculate_reward_1side_type4, calculate_reward_1side_type5, calculate_reward_1side_type6, calculate_reward_1side_type7, calculate_reward_1side_type8, calculate_reward_1side_type9, calculate_reward_1side_type10, calculate_reward_1side_type11, calculate_reward_1side_type12, calculate_reward_1side_type13
from resources import global_variables
from resources.global_state import global_state

draw = True
def q_learning_1side():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type5
    stats = []
    policy = EpsilonGreedy(0.01)
    brain = QLearningControls2(policy)

    directory = 'stats/q-1side-1-reward5-0.5M-team-ball-1-position-jump'
    os.makedirs(directory, exist_ok=True)
    episode = 0

    while True:
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
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
        stats.append(brain.calculate_stats())
        stats[-1].append(episode)
        with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 1000 == 0:
            brain.save(f"{directory}/brain{episode}.json")


def q_learning_1side_2():
    throw_presets = [
        (50, 100),
        (100, 50),
        (150, 20),
        (90, 60),
        (60, 90),
        (80, 80),
        (90, 40),
        (75, 75)
    ]

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type5
    stats = []
    policy = EpsilonGreedy(0.1)
    brain = QLearningControls2(policy)

    directory = 'stats/q-1side-1-reward5-0.5M-team-ball-static'
    os.makedirs(directory, exist_ok=True)
    episode = 0
    for k in range(len(throw_presets)):
        policy.reset()
        for j in range(1000):
            episode += 1
            game = GameEnvironmentOneSide()
            # game.ball.throw_presets = throw_presets[0:k+1]
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
            stats.append([*brain.calculate_stats(), game.score1.score, game.score2.score, episode])
            print(stats[-1])
            with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(stats)
            if episode % 100 == 0:
                brain.save(f"{directory}/brain{episode}.json")


def q_learning_1side_3():
    throw_presets = [
        (50, 100),
        (100, 50),
        (150, 20),
        (90, 60),
        (60, 90),
        (80, 80),
        (90, 40),
        (75, 75)
    ]

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type5
    stats = []
    policy = EpsilonGreedy(0.1)
    brain = QLearningControls2(policy)
    brain.load('stats/q-1side-1-reward5-0.5M-team-ball-increasing/brain3900.json')

    directory = 'stats/q-1side-1-reward5-0.5M-team-ball-increasing'
    os.makedirs(directory, exist_ok=True)
    episode = 3900
    for k in range(len(throw_presets)):
        policy.reset()
        for j in range(1000):
            episode += 1
            game = GameEnvironmentOneSide()
            game.ball.throw_presets = throw_presets[0:k+1]
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
            stats.append([*brain.calculate_stats(), game.score1.score, game.score2.score, episode])
            print(stats[-1])
            with open(f"{directory}/stats2.csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(stats)
            if episode % 100 == 0:
                brain.save(f"{directory}/brain{episode}.json")

def q_learning_1side_4():
    throw_presets = [
        (50, 100),
        (100, 50),
        (150, 20),
        (90, 60),
        (60, 90),
        (80, 80),
        (90, 40),
        (75, 75)
    ]

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type5
    stats = []
    policy = EpsilonGreedy(0.1)
    policy.epsilon = 0.2
    brain = QLearningControls2(policy)

    directory = 'stats/q-1side-1-reward5-0.5M-team-ball-static-E-0.2'
    os.makedirs(directory, exist_ok=True)
    episode = 0
    for k in range(len(throw_presets)):
        # policy.reset()
        for j in range(1000):
            episode += 1
            game = GameEnvironmentOneSide()
            # game.ball.throw_presets = throw_presets[0:k+1]
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

            # brain.epsilon_policy.decay()
            stats.append([*brain.calculate_stats(), game.score1.score, game.score2.score, episode])
            print(stats[-1])
            with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(stats)
            if episode % 100 == 0:
                brain.save(f"{directory}/brain{episode}.json")

def q_learning_1side_5():
    throw_presets = [
        (50, 100),
        (100, 50),
        (150, 20),
        (90, 60),
        (60, 90),
        (80, 80),
        (90, 40),
        (75, 75)
    ]

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type5
    stats = []
    policy = EpsilonGreedy(0.1)
    policy.epsilon = 0.2
    brain = QLearningControls2(policy)

    directory = 'stats/q-1side-1-reward5-0.5M-team-ball-increasing-E-0.2'
    os.makedirs(directory, exist_ok=True)
    episode = 0
    for k in range(len(throw_presets)):
        # policy.reset()
        for j in range(1000):
            episode += 1
            game = GameEnvironmentOneSide()
            game.ball.throw_presets = throw_presets[0:k+1]
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

            # brain.epsilon_policy.decay()
            stats.append([*brain.calculate_stats(), game.score1.score, game.score2.score, episode])
            print(stats[-1])
            with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(stats)
            if episode % 100 == 0:
                brain.save(f"{directory}/brain{episode}.json")



def q_learning_1side_r1():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type6
    stats = []
    policy = EpsilonGreedy(0.05)
    brain = QLearningControls2(policy)

    directory = 'stats/reward3'
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(1000):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(250_000):
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
        with open(f"{directory}/1.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 100 == 0:
            brain.save(f"{directory}/1brain{episode}.json")


def q_learning_1side_r2():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type7
    stats = []
    policy = EpsilonGreedy(0.05)
    brain = QLearningControls2(policy)

    directory = 'stats/reward3'
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(1000):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(250_000):
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
        with open(f"{directory}/2.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 100 == 0:
            brain.save(f"{directory}/2brain{episode}.json")

def q_learning_1side_r3():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type5
    stats = []
    policy = EpsilonGreedy(0.05)
    brain = QLearningControls2(policy)

    directory = 'stats/reward4'
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(1000):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(250_000):
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

            print(episode)

        brain.epsilon_policy.decay()
        stats.append([*brain.calculate_stats(), game.score1.score, game.score2.score, episode])
        with open(f"{directory}/3.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 100 == 0:
            brain.save(f"{directory}/3brain{episode}.json")

def q_learning_1side_r4():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type8
    stats = []
    policy = EpsilonGreedy(0.05)
    brain = QLearningControls2(policy)

    directory = 'stats/reward3'
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(1000):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(250_000):
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
        with open(f"{directory}/4.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 100 == 0:
            brain.save(f"{directory}/4brain{episode}.json")


def q_learning_1side_7():
    throw_presets = [
        (50, 100),
        (100, 50),
        (150, 20),
        (90, 60),
        (60, 90),
        (80, 80),
        (90, 40),
        (75, 75)
    ]

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type5
    stats = []
    policy = EpsilonGreedy(0.1)
    policy.epsilon = 0.1
    brain = QLearningControls2(policy)

    directory = 'stats/q-1side-1-reward5-0.5M-team-ball-static-E-0.1'
    os.makedirs(directory, exist_ok=True)
    episode = 0
    for k in range(len(throw_presets)):
        # policy.reset()
        for j in range(1000):
            episode += 1
            game = GameEnvironmentOneSide()
            # game.ball.throw_presets = throw_presets[0:k+1]
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

            # brain.epsilon_policy.decay()
            stats.append([*brain.calculate_stats(), game.score1.score, game.score2.score, episode])
            print(stats[-1])
            with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(stats)
            if episode % 100 == 0:
                brain.save(f"{directory}/brain{episode}.json")


def q_learning_1side_8():
    throw_presets = [
        (50, 100),
        (100, 50),
        (150, 20),
        (90, 60),
        (60, 90),
        (80, 80),
        (90, 40),
        (75, 75)
    ]

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type5
    stats = []
    policy = EpsilonGreedy(0.1)
    policy.epsilon = 0.1
    brain = QLearningControls2(policy)

    directory = 'stats/q-1side-1-reward5-0.5M-team-ball-increasing-E-0.1'
    os.makedirs(directory, exist_ok=True)
    episode = 0
    for k in range(len(throw_presets)):
        # policy.reset()
        for j in range(1000):
            episode += 1
            game = GameEnvironmentOneSide()
            game.ball.throw_presets = throw_presets[0:k+1]
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

            # brain.epsilon_policy.decay()
            stats.append([*brain.calculate_stats(), game.score1.score, game.score2.score, episode])
            print(stats[-1])
            with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(stats)
            if episode % 100 == 0:
                brain.save(f"{directory}/brain{episode}.json")


def q_learning_1side_random():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type8
    stats = []
    policy = EpsilonGreedy(0.05)
    brain = QLearningControls2(policy)

    directory = 'stats/random'
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(1000):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(250_000):
            game.ball.throw_ball(1)
            for state in step[0]:
                actions.append(brain.get_action(state))
            game.actions = actions
            game.step()
            next_step = game.get_observations()

            calculate_reward(step, actions, next_step, brain)
            # brain.learn()

            step = next_step
            actions = []

            global_events.handle_global_events()
            if global_events.draw:
                game.draw()
                pygame.display.update()

        stats.append([*brain.calculate_stats(), game.score1.score, game.score2.score, episode])
        with open(f"{directory}/4.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 100 == 0:
            brain.save(f"{directory}/4brain{episode}.json")


def q_learning_1side_discount(discount):

    QLearningHyperParameters.discount = discount
    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type8
    stats = []
    policy = EpsilonGreedy(0.1)
    brain = QLearningControls2(policy)

    directory = f"stats/discount"
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(1000):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(250_000):
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
        with open(f"{directory}/{discount}.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 100 == 0:
            brain.save(f"{directory}/brain{episode}.json")


def q_learning_1side_learning_rate(learning_rate):

    QLearningHyperParameters.learning_rate = learning_rate
    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type8
    stats = []
    policy = EpsilonGreedy(0.1)
    brain = QLearningControls2(policy)

    directory = f"stats/learning-rate"
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(1000):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(350_000):
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
        with open(f"{directory}/{learning_rate}.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 100 == 0:
            brain.save(f"{directory}/brain{episode}.json")


def q_learning_1side_deep():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type8
    stats = []
    policy = EpsilonGreedy(0.1)
    brain = DeepQLearningControls(policy)

    directory = 'stats/deep3'
    brain.load('stats/deep2/brain30.json')
    os.makedirs(directory, exist_ok=True)
    episode = 30

    for j in range(1000):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(100_000):
            game.ball.throw_ball(1)
            for state in step[0]:
                actions.append(brain.get_action(state))
            game.actions = actions
            game.step()
            next_step = game.get_observations()

            calculate_reward(step, actions, next_step, brain)
            if iteration % 50 == 0:
                brain.learn()

            step = next_step
            actions = []

            global_events.handle_global_events()
            if global_events.draw:
                game.draw()
                pygame.display.update()
        brain.epsilon_policy.decay()
        stats.append([*brain.calculate_stats(), game.score1.score, game.score2.score, episode])
        with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 1 == 0:
            brain.save(f"{directory}/brain{episode}.json")

def q_learning_1side_after_self_play():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type8
    stats = []
    policy = EpsilonGreedy(0.1)
    policy.epsilon = 0.05
    brain = QLearningControls2(policy)
    brain.load(f"stats/self-play/brain600.json")

    directory = f"stats/after-self-play-no-learning2"
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(100):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(250_000):
            game.ball.throw_ball(1)
            for state in step[0]:
                actions.append(brain.get_action(state))
            game.actions = actions
            game.step()
            next_step = game.get_observations()

            calculate_reward(step, actions, next_step, brain)
            # brain.learn()

            step = next_step
            actions = []

            global_events.handle_global_events()
            if global_events.draw:
                game.draw()
                pygame.display.update()

        # brain.epsilon_policy.decay()
        stats.append([*brain.calculate_stats(), game.score1.score, game.score2.score, episode])
        print(stats[-1])
        with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 100 == 0:
            brain.save(f"{directory}/brain{episode}.json")

def q_learning_1side_test():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type8
    stats = []
    policy = EpsilonGreedy(0.05)
    brain = QLearningControls2(policy)
    brain.load('stats/q-1side-1-reward5-0.5M-team-ball-increasing-E-0.1/brain200.json')
    episode = 0
    policy.epsilon = 0.2
    player = KeyboardControls()

    for j in range(1000):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(250_000):
            # game.ball.throw_ball(1)
            # for state in step[0]:
            #     actions.append(brain.get_action(state))
            actions[0] = brain.get_action(step[0][0])
            actions[1] = player.get_action(step[0][0])
            game.actions = actions
            game.step()
            next_step = game.get_observations()

            # calculate_reward(step, actions, next_step, brain)
            # brain.learn()

            step = next_step
            # actions = []

            # global_events.handle_global_events()
            # if global_events.draw:
            game.draw()
            pygame.display.update()

            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        game.ball.throw_ball(1)


def q_learning_1side_simplified():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type11
    stats = []
    policy = EpsilonGreedy(0.001)
    brain = QLearningControls2(policy)

    directory = f"stats/simplified23"
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(5_000):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(100_000):
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
        brain.epsilon_policy.reset()
        print(stats[-1])
        with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 100 == 0:
            brain.save(f"{directory}/brain{episode}.json")

def q_learning_1side_simplified2():

    global_events = GlobalFunctions()

    calculate_reward = calculate_reward_1side_type13
    stats = []
    policy = EpsilonGreedyDecreasing(0.01, 0.1)
    brain = QLearningControls2(policy)

    directory = f"stats/simplified15"
    os.makedirs(directory, exist_ok=True)
    episode = 0

    for j in range(5_000):
        episode += 1
        game = GameEnvironmentOneSide()
        step = game.get_observations()
        actions = [0, 0]
        for iteration in range(100_000):
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
        if global_state.this_followed / global_state.this_left > global_state.old_followed / global_state.old_left:
            brain.epsilon_policy.reset()
        else:
            brain.epsilon_policy.epsilon = brain.epsilon_policy.reset_epsilon
        global_state.old_followed = global_state.this_followed
        global_state.this_followed = 0
        global_state.old_left = global_state.this_left
        global_state.this_left = 0
        print(stats[-1])
        with open(f"{directory}/stats.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(stats)
        if episode % 100 == 0:
            brain.save(f"{directory}/brain{episode}.json")