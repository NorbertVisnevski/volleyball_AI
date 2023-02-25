class EpsilonGreedy:
    def __init__(self, decay_rate=0.01):
        self.epsilon = 1
        self.decay_rate = 1-decay_rate

    def decay(self):
        self.epsilon *= 1-self.decay_rate

    def reset(self):
        self.epsilon = 1
