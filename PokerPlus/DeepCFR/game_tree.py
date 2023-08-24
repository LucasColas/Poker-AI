"""

Main code for the game tree CFR Traversal with External Sampling

"""


from copy import deepcopy

import numpy as np
import torch
import torch.nn.functional as F

from texasholdem.game.game import TexasHoldEm
from PokerPlus.DeepCFR.nn import DeepCFRModel
from PokerPlus.DeepCFR.utils import card_to_int, int_to_card

from PokerPlus.DeepCFR.memory import AdvantageMemory, StrategyMemory


def compute_strategy(state: TexasHoldEm, strategy_net: DeepCFRModel, nb_actions=5):
    """

    Function used to compute the strategy for a given state.

    """

    # Get the available moves for the current player
    legal_actions = state.get_available_moves()[:nb_actions]
    player = state.current_player

    cards_board = [card_to_int[card.__str__()] for card in state.board]
    hole = state.get_hand(player)
    hole = [card_to_int[card.__str__()] for card in hole]
    cards = hole + cards_board
    # bets
    bets = [val_bet for val_bet in state._get_last_pot().player_amounts.values()]
    cards = [torch.tensor(c, dtype=torch.long) for c in cards]
    bets = torch.tensor(bets, dtype=torch.float32)

    # Get action probabilities from strategy network
    action_probs = (
        F.softmax(strategy_net(cards, bets), dim=1).squeeze().detach().numpy()
    )

    # Create a dictionary to store the action probabilities for each available action
    strategy = {}
    for action, prob in zip(legal_actions, action_probs):
        strategy[action] = prob

    return strategy


def get_payoff(h: TexasHoldEm, p: int):
    gagnant = int(str(h.hand_history.settle)[7])
    for player in h.players:
        if player.id == p and p == gagnant:
            return h.pots[-1]

    return -h.pots[-1]


def get_info_set(h: TexasHoldEm, player: int):
    cards_board = {card_to_int[card.__str__()] for card in h.board}
    hole = h.get_hand(player)
    hole = {card_to_int[card.__str__()] for card in hole}
    cards = hole + cards_board
    # bets
    bets = (val_bet for val_bet in h._get_last_pot().player_amounts.values())

    return cards, bets


def get_opponent_player_num(actual_player: int):
    if actual_player == 1:
        return 0
    else:
        return 1


def traverse(
    game: TexasHoldEm,
    actual_player_to_compute_strategy: int,
    theta1,
    theta2,
    AdvantageMemory: AdvantageMemory,
    StrategyMemory: StrategyMemory,
    iteration_t: int,
    nb_actions=5,
):
    if not game.is_hand_running():
        return get_payoff(game, actual_player_to_compute_strategy)

    elif game.current_player == actual_player_to_compute_strategy:
        sigma_t = compute_strategy(
            game, theta1
        )  # Compute strategy using regret matching

        action_values = np.zeros(len(game.get_available_moves()[:nb_actions]))
        for idx, a in enumerate(game.get_available_moves()[:nb_actions]):
            h_copy = deepcopy(game)
            h_copy.take_action(a)
            action_values[idx] = traverse(
                deepcopy(h_copy),
                actual_player_to_compute_strategy,
                theta1,
                theta2,
                AdvantageMemory,
                StrategyMemory,
                iteration_t,
            )

            regrets = action_values - np.sum(sigma_t * action_values)
        AdvantageMemory[actual_player_to_compute_strategy].insert(
            get_info_set(h_copy, actual_player_to_compute_strategy),
            iteration_t,
            regrets,
        )  # Insert infoset and its action advantages
        return np.max(action_values)  # Return the value of the best action
    else:
        player_num = get_opponent_player_num(actual_player_to_compute_strategy)
        sigma_t = compute_strategy(
            get_info_set(game, player_num), theta2
        )  # Compute opponent's strategy

        StrategyMemory.insert(
            get_info_set(game, player_num), iteration_t, sigma_t
        )  # Insert infoset and its action probabilities

        a = np.random.choice(
            game.get_available_moves()[:nb_actions], p=sigma_t
        )  # Sample action according to opponent's strategy
        game.take_action(a)
        return traverse(
            deepcopy(game),
            player_num,
            theta1,
            theta2,
            AdvantageMemory,
            StrategyMemory,
            iteration_t,
        )
