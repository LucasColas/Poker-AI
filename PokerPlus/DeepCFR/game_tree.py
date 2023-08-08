"""

Main code for the game tree CFR Traversal with External Sampling

"""


from copy import deepcopy

from texasholdem.game.game import TexasHoldEm
from PokerPlus.DeepCFR.nn import DeepCFRModel
from PokerPlus.DeepCFR.utils import card_to_int, int_to_card

import numpy as np
import torch
import torch.nn.functional as F


class Node:
    """

    Node for GameTree.

    """

    def __init__(self, state: TexasHoldEm) -> None:
        self.state = deepcopy(state)  # State is a TexasHoldEm object
        self.parent = None
        self.children = {}


def game_tree_traversal(
    current_state: TexasHoldEm,
    ai_player: int,
    strategy_net: DeepCFRModel,
    num_iterations: int,
):
    """

    Function used to perform game tree traversal and update cumulative regrets.

    """

    for _ in range(num_iterations):
        # Initialize a trajectory list to store states, actions, and payoffs
        trajectory = []
        state = current_state

        # Perform the game tree traversal until a terminal state is reached
        while state.is_hand_running():
            legal_actions = state.get_available_moves()
            player = state.current_player

            cards_board = [card_to_int[card.__str__()] for card in state.board]
            hole = state.get_hand(player)
            hole = [card_to_int[card.__str__()] for card in hole]
            cards = hole + cards_board
            # bets
            bets = [
                val_bet for val_bet in state._get_last_pot().player_amounts.values()
            ]
            cards = [torch.tensor(c, dtype=torch.long) for c in cards]
            bets = torch.tensor(bets, dtype=torch.float32)

            # Get action probabilities from strategy network
            action_probs = (
                F.softmax(strategy_net(cards, bets), dim=1).squeeze().detach().numpy()
            )

            # Sample an action based on the action probabilities
            action = np.random.choice(legal_actions, p=action_probs)

            # Transition to the next state based on the selected action
            state.take_action(action)

            # Record the current state, action, player's, player's payoff
            trajectory.append((deepcopy(state), player, action, None))

        # Handle terminal state to compute payoffs and record in the trajectory list
        if not state.is_hand_running():
            # payoffs
            gagnant = int(str(state.hand_history.settle)[7])
            for player in state.players:
                if player.id == ai_player and ai_player == gagnant:
                    payoffs = state.pots[-1]
                    break

            else:
                payoffs = -state.pots[-1]

            trajectory.append((deepcopy(state), None, None, payoffs))

        # Backpropagate the trajectory and update cumulative regrets
        for _, (state_i, player_i, action_i, payoffs_i) in enumerate(trajectory):
            if player_i is not None and action_i is not None:
                counterfactual_regret = (
                    payoffs_i[player_i] - trajectory[-1][3][player_i]
                )
                strategy_net.update_regret(
                    state_i, player_i, action_i, counterfactual_regret
                )


def compute_strategy(state: TexasHoldEm, strategy_net: DeepCFRModel):
    """

    Function used to compute the strategy for a given state.

    """

    # Get the available moves for the current player
    legal_actions = state.get_available_moves()
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
            payoffs = h.pots[-1]
            break

    else:
        payoffs = -h.pots[-1]


def get_info_set(h: TexasHoldEm, p: int):
    cards_board = {card_to_int[card.__str__()] for card in h.board}
    hole = h.get_hand(p)
    hole = {card_to_int[card.__str__()] for card in hole}
    cards = hole + cards_board
    # bets
    bets = (val_bet for val_bet in h._get_last_pot().player_amounts.values())

    return cards, bets


def traverse(h: TexasHoldEm, p: int, theta1, theta2, MV, M_PI, t):
    if not h.is_hand_running():
        return get_payoff(h, p)

    elif h.current_player == p:
        sigma_t = compute_strategy(h, theta1)  # Compute strategy using regret matching

        action_values = np.zeros(len(h.get_available_moves()))
        for idx, a in enumerate(h.get_available_moves()):
            h_copy = deepcopy(h)
            h_copy.take_action(a)
            action_values[idx] = traverse(
                deepcopy(h_copy), p, theta1, theta2, MV, M_PI, t
            )

            regrets = action_values - np.sum(sigma_t * action_values)
        MV.insert(
            get_info_set(h_copy, p), t, regrets
        )  # Insert infoset and its action advantages
        return np.max(action_values)  # Return the value of the best action
    else:
        sigma_t = compute_strategy(
            get_info_set(h, p), theta2
        )  # Compute opponent's strategy

        M_PI.insert(
            get_info_set(h, p), t, sigma_t
        )  # Insert infoset and its action probabilities

        a = np.random.choice(
            h.get_legal_actions(), p=sigma_t
        )  # Sample action according to opponent's strategy
        h.take_action(a)
        return traverse(deepcopy(h), p, theta1, theta2, MV, M_PI, t)
