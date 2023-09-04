from texasholdem.card.deck import Deck
from texasholdem.card.card import Card
from texasholdem.game.game import TexasHoldEm

d = Deck()
card_to_int = {}
int_to_card = {}
count = 0

for card in d.cards:
    card_str = Card.STR_RANKS[card.rank] + Card.INT_SUIT_TO_CHAR_SUIT[card.suit]
    card_to_int[card_str] = count
    int_to_card[count] = card
    count += 1


def get_opponent_player_num(current_player: int):
    if current_player == 1:
        return 0
    else:
        return 1


def available_moves(game: TexasHoldEm, nb_actions: int):
    actions = game.get_available_moves()
    available_actions = []
    for index, action in enumerate(actions):
        if index < nb_actions:
            available_actions.append(action[1])
        else:
            return available_actions
