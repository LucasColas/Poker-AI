"""

Reservoir-sampled advantage memory and strategy memory MΠ

"""


import random


class AdvantageMemory:
    def __init__(self):
        self.data = set()  # List to store (infoset_key, t, regrets) tuples

    def insert(self, infoset_key : tuple, iteration_t : int, regrets : int):
        self.data.append((infoset_key, iteration_t, regrets))

    def get_data(self):
        return self.data

    def sample(self, batch_size):
        return random.sample(self.data, batch_size)


class StrategyMemory:
    def __init__(self):
        self.data = {}  # Dictionary to store (infoset_key, t, strategy) pairs

    def insert(self, infoset_key : tuple, iteration_t : int, strategy):
        self.data[(infoset_key, iteration_t)] = strategy

    def get_strategy(self, infoset_key : tuple, iteration_t : int):
        return self.data.get((infoset_key, iteration_t), None)
