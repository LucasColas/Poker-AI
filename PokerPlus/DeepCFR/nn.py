"""

Architecture of the neural network for the Deep CFR model.


"""


import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class CardEmbedding(nn.Module):
    def __init__(self, dim):
        super(CardEmbedding, self).__init__()
        self.rank = nn.Embedding(13, dim)
        self.suit = nn.Embedding(4, dim)
        self.card = nn.Embedding(52, dim)

    def forward(self, input):
        print("forward of CardEmbedding")
        print("input: ", input)
        B, num_cards = input.shape
        x = input.view(-1)
        valid = x.ge(0).float()  # -1 means 'no card'
        x = x.clamp(min=0)
        embs = self.card(x) + self.rank(x // 4) + self.suit(x % 4)
        embs = embs * valid.unsqueeze(1)  # zero out 'no card' embeddings
        return embs.view(B, num_cards, -1).sum(1)


class DeepCFRModel(nn.Module):
    def __init__(self, n_card_types, n_bets, max_bet=100000, n_actions=5, dim=256):
        super(DeepCFRModel, self).__init__()
        self.max_bet = max_bet
        self.card_embeddings = nn.ModuleList(
            [CardEmbedding(dim) for _ in range(n_card_types)]
        )
        self.card1 = nn.Linear(dim * n_card_types, dim)
        self.card2 = nn.Linear(dim, dim)
        self.card3 = nn.Linear(dim, dim)
        self.bet1 = nn.Linear(n_bets * 2, dim)
        self.bet2 = nn.Linear(dim, dim)
        self.comb1 = nn.Linear(2 * dim, dim)
        self.comb2 = nn.Linear(dim, dim)
        self.comb3 = nn.Linear(dim, dim)
        self.action_head = nn.Linear(dim, n_actions)

    def forward(self, cards, bets):
        """
        cards: ((Nx2), (Nx3) [, (Nx1), (Nx1)]) # (hole, board, [turn, river])
        bets: Nx n_bet_feats
        """
        # 1. card branch
        # embed hole, flop, and optionally turn and river
        card_embs = []
        print("cards: ", cards)
        print("bets: ", bets)

        for embedding, card_group in zip(self.card_embeddings, cards):
            print("do embedding")
            print("card_group: ", card_group)
            if card_group.numel():
                card_embs.append(embedding(card_group.view(1, -1)))
        card_embs = torch.cat(card_embs, dim=1)
        x = F.relu(self.card1(card_embs))
        x = F.relu(self.card2(x))
        x = F.relu(self.card3(x))

        # 2. bet branch
        bet_size = bets.clamp(0, self.max_bet)
        bet_occurred = bets.ge(0)
        bet_feats = torch.cat([bet_size, bet_occurred.float()], dim=1)
        y = F.relu(self.bet1(bet_feats))
        y = F.relu(self.bet2(y) + y)

        # 3. combined trunk
        z = torch.cat([x, y], dim=1)
        z = F.relu(self.comb1(z))
        z = F.relu(self.comb2(z) + z)
        z = F.relu(self.comb3(z) + z)
        z = F.normalize(z, p=2, dim=1)  # (z - mean) / std
        return self.action_head(z)

    def update_regret(self, state, player, action, counterfactual_regret):
        """
        Update the cumulative regrets for the specified action at the given information set.

        Args:
            state (TexasHoldEm): The current state of the game.
            player (int): The player for whom to update the cumulative regrets.
            action (int): The action taken by the player.
            counterfactual_regret (float): The counterfactual regret for the action.

        """
        cards = state.board
        # bets
        bets = [val_bet for val_bet in state._get_last_pot().player_amounts.values()]
        cards = [torch.tensor(c, dtype=torch.long) for c in cards]
        bets = torch.tensor(bets, dtype=torch.float32)

        with torch.no_grad():
            # Get the action probabilities from the current strategy network
            action_probs = (
                F.softmax(self(cards, bets), dim=1).squeeze().detach().numpy()
            )

        # Compute the cumulative regrets for each action at the information set
        cumulative_regrets = np.zeros(self.action_head.out_features)
        for a in state.get_available_moves():
            cumulative_regrets[a] = max(action_probs[a] + counterfactual_regret, 0)

        # Update the strategy network with the updated cumulative regrets
        self.update_strategy(cards, bets, cumulative_regrets)

    def update_strategy(self, cards, bets, cumulative_regrets):
        """
        Update the strategy network with the updated cumulative regrets.

        Args:
            cards: ((Nx2), (Nx3) [, (Nx1), (Nx1)]) # (hole, board, [turn, river])
            bets: Nx n_bet_feats
            cumulative_regrets (numpy array): The updated cumulative regrets for each action.

        """
        cards = [c.view(1, -1) for c in cards]
        bets = bets.view(1, -1)
        cumulative_regrets = torch.tensor(cumulative_regrets, dtype=torch.float32)
        # Compute the new action probabilities using regret-matching
        action_probs = F.softmax(cumulative_regrets, dim=0)

        # Perform a single optimization step to update the strategy network
        optimizer = torch.optim.SGD(self.parameters(), lr=0.01)
        optimizer.zero_grad()
        loss = F.mse_loss(self(cards, bets), action_probs)
        loss.backward()
        optimizer.step()
