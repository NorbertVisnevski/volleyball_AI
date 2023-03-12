from collections import deque
import json
import random
import numpy as np

from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from controls.control import Control
from resources import global_variables


class DeepQLearningHyperParameters:
    learning_rate = 0.001
    inverse_alpha = 1 - learning_rate
    discount = 0.6
    batch_size = 128
    update_limit = 10

class DeepQLearningControls(Control):

    def __init__(self, epsilon_policy):
        self.epsilon_policy = epsilon_policy
        self.replay_memory = deque()

        self.model = self.build_compile_model()
        self.target_model = self.build_compile_model()
        self.align_target_model()
        self.rewards = list()

        self.target_update_counter = 0

    def store(self, state, action, reward, next_state):
        self.replay_memory.append((state, action, reward, next_state))
        self.rewards.append(reward)

    def build_compile_model(self):
        model = Sequential()
        model.add(Dense(32, input_shape=[global_variables.observations_size], activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(global_variables.actions_size, activation='sigmoid'))

        model.compile(loss="mse", optimizer=Adam(learning_rate=DeepQLearningHyperParameters.learning_rate), metrics=['accuracy'])
        return model

    def align_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def get_action(self, state):
        if random.random() < self.epsilon_policy.epsilon:
            return random.randint(0, global_variables.actions_size-1)
        qs = self.get_qs(state)
        action = np.argmax(qs)
        return action

    def learn(self):
        if len(self.replay_memory) < DeepQLearningHyperParameters.batch_size:
            return

        minibatch = random.sample(self.replay_memory, DeepQLearningHyperParameters.batch_size)

        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_list = self.model.predict(current_states, verbose=0)

        new_current_states = np.array([transition[3] for transition in minibatch])
        future_qs_list = self.target_model.predict(new_current_states, verbose=0)

        X = []
        y = []

        for index, (current_state, action, reward, new_current_state) in enumerate(minibatch):
            max_future_q = np.max(future_qs_list[index])
            new_q = reward + DeepQLearningHyperParameters.discount * max_future_q

            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            X.append(current_state)
            y.append(current_qs)

        self.model.fit(np.array(X), np.array(y), epochs=1, batch_size=DeepQLearningHyperParameters.batch_size,  verbose=0, shuffle=False)

        self.target_update_counter += 1

        if self.target_update_counter > DeepQLearningHyperParameters.update_limit:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    def get_qs(self, state):
        state = [state]
        qs = self.model(np.array(state), training=False)
        return qs[0]

    def calculate_stats(self):
        stats = [sum(self.rewards) / len(self.rewards), min(self.rewards), max(self.rewards), sum(self.rewards), 0, round(self.epsilon_policy.epsilon, 4)]
        self.rewards.clear()
        return stats


    def save(self, directory):
        self.model.save_weights(f"{directory}")

    def load(self, directory):
        self.model.load_weights(f"{directory}")
        self.align_target_model()
