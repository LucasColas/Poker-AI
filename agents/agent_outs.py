from texasholdem.game.game import TexasHoldEm, Pot
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.evaluator.evaluator import *
from texasholdem.gui.text_gui import TextGUI
from texasholdem.card.deck import Deck
from texasholdem.evaluator.lookup_table import LOOKUP_TABLE
from fonctions_auxiliaires import *
from collections import defaultdict
import random

def agent_outs(game: TexasHoldEm):
    if len(game.board) == 0:
        return strategie_preflop1(game)

    player_cards = game.hands[game.current_player]
    nb_cards = 52
    board_cards = game.board


    #FLOP
    d = Deck()
    cards = d.draw(num=nb_cards)
    other_cards = [card for card in cards if card not in player_cards and card not in board_cards]

    current_rank = evaluate(player_cards,board_cards)

    elements = player_cards + board_cards

    combinaisons = generer_combinaisons(4, elements)
    print("elements : ", elements)
    info_combi = {}
    for id, combinaison in enumerate(combinaisons):
        info_combi[id] = defaultdict(int)
        for card in other_cards:
            new_hand = combinaison + (card,)
            rank = evaluate(new_hand[:2], new_hand[2:])
            info_combi[id][rank_to_string(rank)] += 1




    print("info combi", info_combi)






    current_best_hand = evaluate(player_cards, board_cards)
    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips
    total = None
    rank = evaluate(game.hands[game.current_player],game.board)
    p_win = get_five_card_rank_percentage(rank)
    p = random.random()
    if game.players[game.current_player].state == PlayerState.IN:
        #print("flop check")
        action_type = ActionType.CHECK
    elif (game.players[game.current_player].state == PlayerState.TO_CALL) and (p<p_win) and (max_raise > min_raise) :
        #print("call, p =" ,p, "p_win=",p_win)
        action_type = ActionType.CALL
    else:
        #print("fold, p =", p, " p_win=", p_win)
        action_type = ActionType.FOLD

    return action_type, total
