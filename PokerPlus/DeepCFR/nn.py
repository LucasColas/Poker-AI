import torch
import torch.nn as nn

class DeepCFRNetwork(nn.Module):
    def __init__(self):
        super(DeepCFRNetwork, self).__init__()
        self.num_actions = 3
        self.cards_embedding = nn.Embedding(52, embedding_dim=32)
        self.rank_embedding = nn.Embedding(13, embedding_dim=8)
        self.suit_embedding = nn.Embedding(4, embedding_dim=8)
        
        self.cards_fc = nn.Sequential(
            nn.Linear(32 * 4, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU()
        )
        
        self.bets_fc = nn.Sequential(
            nn.Linear(12, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU()
        )
        
        self.final_fc = nn.Sequential(
            nn.Linear(128 + 64, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, self.num_actions),
            nn.Softmax(dim=1)
        )
    
    def forward(self, cards, bets):
        cards_embedding = self.cards_embedding(cards)
        rank_embedding = self.rank_embedding(cards % 13)
        suit_embedding = self.suit_embedding(cards // 13)
        
        cards_sum = torch.sum(cards_embedding, dim=1)
        rank_sum = torch.sum(rank_embedding, dim=1)
        suit_sum = torch.sum(suit_embedding, dim=1)
        
        cards_representation = torch.cat([cards_sum, rank_sum, suit_sum], dim=1)
        cards_output = self.cards_fc(cards_representation)
        
        bets_output = self.bets_fc(bets)
        
        combined_features = torch.cat([cards_output, bets_output], dim=1)
        
        final_output = self.final_fc(combined_features)
        return final_output
