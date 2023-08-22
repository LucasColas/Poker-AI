"""

Main file of the DeepCFR algorithm.


"""


from copy import deepcopy

import torch
import torch.optim as optim
import torch.nn.functional as F

from PokerPlus.DeepCFR.nn import DeepCFRModel
from PokerPlus.DeepCFR.game_tree import traverse
from PokerPlus.DeepCFR.memory import AdvantageMemory, StrategyMemory
from texasholdem.game.game import TexasHoldEm

"""
n_card_types = 4
n_bets = 2
n_actions = 3
"""


def deep_cfr(
    nb_iterations: int = 10000,
    nb_players: int = 2,
    nb_game_tree_traversals: int = 200,
    game: TexasHoldEm = None,
    n_actions: int = 3,
    n_card_types: int = 4,
    n_bets: int = 20,
):
    """

    Main function of the DeepCFR algorithm.
    Initialize each player’s advantage network V (I, a|θp) with parameters θp so that it returns 0 for all inputs.
    Initialize reservoir-sampled advantage memories MV,1, MV,2 and strategy memory MΠ.

    """
    if not game:
        game = TexasHoldEm(buyin=1500, big_blind=80, small_blind=40, max_players=2)
        game.start_hand()
    # Initialize each player’s advantage network
    advantage_net = [
        DeepCFRModel(n_card_types, n_bets, n_actions) for _ in range(nb_players)
    ]

    # Initialize reservoir-sampled advantage memories MV_1, MV_2 and strategy memory MΠ.
    advantage_memories = [AdvantageMemory() for _ in range(nb_players)]
    strategy_memory = StrategyMemory()

    for iteration_t in range(nb_iterations):
        for player in range(nb_players):
            for _ in range(nb_game_tree_traversals):
                # Traverse the game tree
                traverse(
                    deepcopy(game),
                    player,
                    advantage_net,
                    advantage_memories[player],
                    strategy_memory,
                    iteration_t,
                )

            # Train
            train_advantage_network(advantage_net[player], advantage_memories[player])

    # Train the strategy network
    strategy_net = DeepCFRModel(n_card_types, n_bets, n_actions)
    train_strategy_network(strategy_net, strategy_memory)

    return strategy_net


def train_advantage_network(net, MV, lr=0.001, batch_size=10000, nb_epochs=4000):
    optimizer = optim.Adam(net.parameters(), lr=lr, clip_value=1.0)

    for epoch in range(nb_epochs):
        total_loss = 0.0
        num_batches = len(MV) // batch_size

        for _ in range(num_batches):
            batch = MV.sample(batch_size)
            losses = []

            for info, _, regrets in batch:
                optimizer.zero_grad()
                cards, bets = info
                regrets_tensor = torch.tensor(regrets, dtype=torch.float32)

                action_probs = net(cards, bets)
                loss = F.mse_loss(action_probs, regrets_tensor)
                losses.append(loss)
                loss.backward()
                optimizer.step()

            batch_loss = sum(losses) / len(losses)
            total_loss += batch_loss

        avg_loss = total_loss / num_batches
        print(f"Epoch [{epoch+1}], Avg Loss: {avg_loss:.4f}")


def train_strategy_network(net, M_PI, lr=0.001, batch_size=10000, nb_epochs=4000):
    optimizer = optim.Adam(net.parameters(), lr=lr)

    for epoch in range(nb_epochs):
        total_loss = 0.0
        num_batches = len(M_PI) // batch_size

        for _ in range(num_batches):
            batch = M_PI.sample(batch_size)
            losses = []

            for infoset_key, _, sigma_t in batch:
                cards, bets = infoset_key
                sigma_t_tensor = torch.tensor(sigma_t, dtype=torch.float32)

                action_probs = net(cards, bets)
                loss = F.mse_loss(action_probs, sigma_t_tensor)
                loss.backward()
                optimizer.step()
                losses.append(loss)

            batch_loss = sum(losses) / len(losses)
            total_loss += batch_loss

            optimizer.zero_grad()

        avg_loss = total_loss / num_batches
        print(f"Epoch [{epoch+1}], Avg Loss: {avg_loss:.4f}")


def save_deep_cfr(
    path: str,
    name_file: str,
    nb_iterations: int,
    nb_players: int,
    nb_game_tree_traversals: int,
    game: TexasHoldEm,
    n_actions: int,
    n_card_types: int,
    n_bets: int,
):
    strategy_net = deep_cfr(
        nb_iterations,
        nb_players,
        nb_game_tree_traversals,
        game,
        n_actions,
        n_card_types,
        n_bets,
    )
    torch.save(strategy_net.state_dict(), path + "/" + name_file + ".pth")
