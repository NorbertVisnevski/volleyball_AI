import json
import random
import numpy as np
from collections import deque

from controls.control import Control
from controls.epsilon import EpsilonGreedy
from resources import global_variables


class QLearningHyperParameters:
    learning_rate = 0.2
    inverse_alpha = 1 - learning_rate
    discount = 0.6


class QLearningControls(Control):

    def __init__(self, epsilon_policy):
        self.Q_Table = {}
        self.replay_memory = deque()
        self.rewards = list()
        self.epsilon_policy = epsilon_policy

    def state_to_key(self, state):
        for i in range(len(state) - 2):
            state[i] = round(state[i], 1)
        state[-1] = round(state[-1], 2)
        state[-2] = round(state[-2], 2)
        return '|'.join([str(float(elem)) for i, elem in enumerate(state)])

    def get_action(self, state):
        key = self.state_to_key(state)
        row = self.Q_Table.get(key)
        if row is None:
            row = [random.random() for _ in range(global_variables.actions_size)]
            self.Q_Table[key] = row
        if random.random() < self.epsilon_policy.epsilon:
            return random.randint(0, global_variables.actions_size - 1)
        return np.argmax(row)

    def store(self, state, action, reward, next_state, final=False):
        self.replay_memory.append((state, action, reward, next_state, final))
        self.rewards.append(reward)

    def learn(self):
        for (state, action, reward, next_state, final) in self.replay_memory:
            key = self.state_to_key(state)
            row = self.Q_Table.get(key) or [random.random() for _ in range(global_variables.actions_size)]
            self.Q_Table[key] = row
            old_q = row[action]
            next_key = self.state_to_key(next_state)
            next_row = self.Q_Table.get(next_key) or [random.random() for _ in range(global_variables.actions_size)]
            self.Q_Table[next_key] = next_row
            max_q = max(next_row)
            if not final:
                row[action] = QLearningHyperParameters.inverse_alpha * old_q + QLearningHyperParameters.learning_rate * (reward + QLearningHyperParameters.discount * max_q)
            else:
                row[action] = reward
        self.replay_memory.clear()

    def calculate_stats(self):
        stats = [sum(self.rewards) / len(self.rewards), min(self.rewards), max(self.rewards), sum(self.rewards), len(self.Q_Table.keys()), round(self.epsilon_policy.epsilon, 4)]
        self.rewards.clear()
        return stats

    def save(self, directory):
        serialized = json.dumps(self.Q_Table, indent=2)
        with open(f"{directory}", "w") as f:
            f.write(serialized)

    def load(self, directory):
        with open(f"{directory}", "r") as f:
            self.Q_Table = json.load(f)


class QLearningControls2(QLearningControls):
    def state_to_key(self, state):
        for i in range(len(state)):
            state[i] = round(state[i], 1)
        return '|'.join([str(float(elem)) for i, elem in enumerate(state)])
