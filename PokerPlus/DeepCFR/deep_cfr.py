
from copy import deepcopy

import torch
import torch.optim as optim
import torch.nn.functional as F

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
    advantage_net = [DeepCFRModel(n_card_types, n_bets, n_actions) for _ in range(nb_players)]
    #advantage_net.zero_grad()
    # Initialize reservoir-sampled advantage memories MV,1, MV,2 and strategy memory MΠ.
    advantage_memories = [AdvantageMemory() for _ in range(nb_players)]
    strategy_memory = StrategyMemory()
    # Initialize the optimizer
    optimizer = optim.Adam(advantage_net.parameters(), lr=0.001)

    for _ in range(T):
        for p in range(nb_players):
            for _ in range(K):
                # Traverse the game tree
                traverse(deepcopy(game), advantage_net[p], advantage_memories[p], strategy_memory)
            
            # Train 
            train_advantage_network(advantage_net[p], advantage_memories[p])

    # Train the strategy network
    strategy_net = DeepCFRModel(n_card_types, n_bets, n_actions)
    train_strategy_network(strategy_net, strategy_memory)

    return strategy_net


            


def train_advantage_network(net, MV):
    optimizer = optim.Adam(net.parameters(), lr=0.001, clip_value=1.0)
    batch_size = 10000
    
    for epoch in range(4000):
        total_loss = 0.0
        num_batches = len(MV) // batch_size
        
        for _ in range(num_batches):
            batch = MV.sample(batch_size)
            losses = []
            
            for info, _, regrets in batch:
                cards, bets = info
                regrets_tensor = torch.tensor(regrets, dtype=torch.float32)
                
                action_probs = net(cards, bets)
                loss = F.mse_loss(action_probs, regrets_tensor)
                losses.append(loss)
                loss.backward()
                optimizer.step()
                
            
            batch_loss = sum(losses) / len(losses)
            total_loss += batch_loss
            
            optimizer.zero_grad()
            
        
        avg_loss = total_loss / num_batches
        print(f"Epoch [{epoch+1}/4000], Avg Loss: {avg_loss:.4f}")


def train_strategy_network(net, M_PI):
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    batch_size = 10000

    for epoch in range(4000):
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
                losses.append(loss)

            batch_loss = sum(losses) / len(losses)
            total_loss += batch_loss

            optimizer.zero_grad()
            batch_loss.backward()
            optimizer.step()

        avg_loss = total_loss / num_batches
        print(f"Epoch [{epoch+1}/4000], Avg Loss: {avg_loss:.4f}")
