from typing import Tuple

import random

from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.evaluator.evaluator import *


def agent_naif(game: TexasHoldEm) -> Tuple[ActionType, int]:
    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips
    total = None
    print(game.current_player,": agent_naif")
    #pre-flop
    if len(game.board) == 0:
        if game.players[game.current_player].state == PlayerState.IN:
            action_type = ActionType.CHECK
            print("pre flop check")
        elif (max_raise > min_raise) and (game.players[game.current_player].state == PlayerState.TO_CALL):
            print("pre flop call")
            action_type = ActionType.CALL
        else :
            print("pre flop fold")
            action_type = ActionType.FOLD

    #FLOP
    #TODO : vérifier si on peut call (ou s'il faut par exemple relancer)
    elif len(game.board) != 0:
        rank = evaluate(game.hands[game.current_player],game.board)
        p_win = get_five_card_rank_percentage(rank)
        p = random.random()
        if p<p_win and (max_raise > min_raise) :
            print("flop call, p =" ,p)
            action_type = ActionType.CALL
        else:
            print("flop fold")
            action_type = ActionType.FOLD
    
    return action_type, total
