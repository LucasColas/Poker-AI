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

from PokerPlus.DeepCFR.utils import get_opponent_player_num, available_moves


def compute_strategy(state: TexasHoldEm, strategy_net: DeepCFRModel, nb_actions=5):
    """

    Function used to compute the strategy for a given state.

    """

    # Get the available moves for the current player
    print("state: ", state)
    legal_actions = available_moves(state, nb_actions)
    player = state.current_player

    cards_board = [card_to_int[str(card)] for card in state.board]
    flop = [card for card in cards_board[:3]]
    turn = cards_board[3:4]
    river = cards_board[4:5]
    hole = state.get_hand(player)
    hole = [card_to_int[str(card)] for card in hole]
    cards = [hole, flop]
    if turn:
        cards.extend([turn])

    if river:
        cards.extend([river])
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


def get_payoff(game: TexasHoldEm, player: int):
    gagnant = int(str(game.hand_history.settle)[7])
    for player in game.players:
        if player.id == player and player == gagnant:
            return game.pots[-1]

    return -game.pots[-1]


def get_info_set(game: TexasHoldEm, player: int):
    cards_board = [card_to_int[card.__str__()] for card in game.board]
    hole = game.get_hand(player)
    hole = [card_to_int[card.__str__()] for card in hole]
    cards = hole + cards_board
    # bets
    bets = (val_bet for val_bet in game._get_last_pot().player_amounts.values())

    return cards, bets


def traverse(
    game: TexasHoldEm,
    current_player_to_compute_strategy: int,
    theta1,
    theta2,
    AdvantageMemory: AdvantageMemory,
    StrategyMemory: StrategyMemory,
    iteration_t: int,
    nb_actions=5,
):
    if not game.is_hand_running():
        print("game : ", game)
        return get_payoff(game, current_player_to_compute_strategy)

    elif game.current_player == current_player_to_compute_strategy:
        sigma_t = compute_strategy(
            game, theta1, nb_actions
        )  # Compute strategy using regret matching

        available_moves_ = available_moves(game, nb_actions)
        regrets = np.zeros(len(available_moves_))

        action_values = np.zeros(len(available_moves_))
        for idx, action in enumerate(available_moves_):
            game.take_action(action)
            action_values[idx] = traverse(
                deepcopy(game),
                current_player_to_compute_strategy,
                theta1,
                theta2,
                AdvantageMemory,
                StrategyMemory,
                iteration_t,
            )
            regrets[idx] = action_values - np.sum(
                list(sigma_t.values()) * action_values
            )
        AdvantageMemory[current_player_to_compute_strategy].insert(
            get_info_set(game, current_player_to_compute_strategy),
            iteration_t,
            regrets,
        )  # Insert infoset and its action advantages
        return np.max(action_values)  # Return the value of the best action
    else:
        available_moves_ = available_moves(game, nb_actions)
        opponent_num = get_opponent_player_num(current_player_to_compute_strategy)
        sigma_t = compute_strategy(
            game, theta2, nb_actions
        )  # Compute opponent's strategy

        StrategyMemory.insert(
            get_info_set(game, opponent_num), iteration_t, sigma_t
        )  # Insert infoset and its action probabilities

        a = np.random.choice(
            available_moves_, p=list(sigma_t.values())
        )  # Sample action according to opponent's strategy
        game.take_action(a)
        return traverse(
            deepcopy(game),
            opponent_num,
            theta1,
            theta2,
            AdvantageMemory,
            StrategyMemory,
            iteration_t,
        )
