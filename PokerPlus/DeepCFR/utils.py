from texasholdem.card.deck import Deck
from texasholdem.card.card import Card

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