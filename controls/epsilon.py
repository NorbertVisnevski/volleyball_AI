class EpsilonGreedy:
    def __init__(self, decay_rate=0.00000001):
        self.epsilon = 1
        self.decay_rate = 1-decay_rate

    def decay(self):
        self.epsilon *= self.decay_rate

    def reset(self):
        self.epsilon = 1

class EpsilonGreedyDecreasing:
    def __init__(self, decay_rate=0.01, global_decay=0.01):
        self.epsilon = 1
        self.reset_epsilon = 1
        self.decay_rate = 1-decay_rate
        self.global_decay = 1-global_decay

    def decay(self):
        self.epsilon *= self.decay_rate

    def reset(self):
        self.reset_epsilon *= self.global_decay
        self.epsilon = self.reset_epsilon

