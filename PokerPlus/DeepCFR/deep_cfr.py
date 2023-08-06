
from copy import deepcopy

import torch
import torch.optim as optim

from PokerPlus.DeepCFR.nn import DeepCFRModel
from PokerPlus.DeepCFR.game_tree import traverse
from PokerPlus.DeepCFR.memory import AdvantageMemory, StrategyMemory
from texasholdem.game.game import TexasHoldEm


n_card_types = 4
n_bets = 2
n_actions = 3


def deep_cfr(T : int, nb_players : int, K : int, game : TexasHoldEm, n_actions : int, n_card_types : int, n_bets : int):
    """
    
    Main function of the DeepCFR algorithm.
    Initialize each player’s advantage network V (I, a|θp) with parameters θp so that it returns 0 for all inputs.
    Initialize reservoir-sampled advantage memories MV,1, MV,2 and strategy memory MΠ.
    
    """
    # Initialize each player’s advantage network V (I, a|θp) with parameters θp so that it returns 0 for all inputs.
    advantage_net = DeepCFRModel(n_card_types, n_bets, n_actions)
    advantage_net.zero_grad()
    # Initialize reservoir-sampled advantage memories MV,1, MV,2 and strategy memory MΠ.
    advantage_memories = [AdvantageMemory() for _ in range(nb_players)]
    strategy_memory = [StrategyMemory() for _ in range(nb_players)]
    # Initialize the optimizer
    optimizer = optim.Adam(advantage_net.parameters(), lr=0.001)

    for _ in range(T):
        for _ in range(nb_players):
            for _ in range(K):
                # Traverse the game tree
                traverse(deepcopy(game), advantage_net, advantage_memories, strategy_memory)

            


