import random
import time
import math
from copy import deepcopy, copy
from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.agents.basic import random_agent
from texasholdem.evaluator.evaluator import *
from texasholdem.card.deck import Deck
from texasholdem.game.player_state import PlayerState
from itertools import combinations
from texasholdem.agents.basic import random_agent
from texasholdem.gui.text_gui import TextGUI
from texasholdem.evaluator.evaluator import *
import time
from PokerPlus.Agents.fonctions_auxiliaires import obtenir_cote, cote_en_pourcentage

from PokerPlus.Agents.agents_bots import agent_naif


def HandPotentiel(ourcards, boardcards):
    oppcards = Deck().draw(num=52)
    ahead = 0
    tied = 1
    behind = 2

    oppcards = [
        card for card in oppcards if card not in ourcards and card not in boardcards
    ]
    ourrank = evaluate(ourcards, boardcards)
    HP = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    HPTotal = [0, 0, 0]
    for set_ in combinations(oppcards, 2):
        opprank = evaluate(list(set_), boardcards)
        if ourrank > opprank:
            index = ahead
        elif ourrank == opprank:
            index = tied
        else:
            index = behind

        for T_R in combinations(oppcards, 2):
            if list(T_R)[0] not in list(set_) and list(T_R)[1] not in list(set_):
                board = boardcards + list(T_R)
                # print(ourcards, board)
                ourbest = evaluate(ourcards, board)
                # print(list(set_), board)
                oppbest = evaluate(list(set_), board)
                if ourbest > oppbest:
                    HP[index][ahead] += 1
                elif ourbest == oppbest:
                    HP[index][tied] += 1
                else:
                    HP[index][behind] += 1
                HPTotal[index] += 1
    Ppot = (HP[behind][ahead] + (HP[behind][tied] / 2) + (HP[tied][ahead] / 2)) / (
        HPTotal[behind] + HPTotal[tied]
    )
    Npot = (HP[ahead][behind] + (HP[tied][behind] / 2) + (HP[ahead][tied] / 2)) / (
        HPTotal[ahead] + HPTotal[tied]
    )
    return [Ppot, Npot]


def HandStrength(ourcards, boardcards):
    ahead = 0
    tied = 0
    behind = 0
    ourrank = evaluate(ourcards, boardcards)
    oppcards = Deck().draw(num=52)
    oppcards = [
        card for card in oppcards if card not in ourcards and card not in boardcards
    ]
    for set_ in combinations(oppcards, 2):
        opprank = evaluate(list(set_), boardcards)
        if ourrank > opprank:
            ahead += 1
        elif ourrank == opprank:
            tied += 1
        else:
            behind += 1
    handstrength = (ahead + tied / 2) / (ahead + tied + behind)
    return handstrength


def proba_win(game: TexasHoldEm):
    ts = time.time()
    HS = HandStrength(game.hands[game.current_player], game.board)
    print("HS : ", HS)
    HP = HandPotentiel(game.hands[game.current_player], game.board)
    print("HP : ", HP)
    res = time.time() - ts
    print("Time : ", res)
    return HS * (1 - HP[1]) + (1 - HS) * HP[0]


def agent_proba(game: TexasHoldEm):
    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips
    if len(game.board) == 0:
        action, total = game.get_available_moves().sample()
        if action == ActionType.RAISE:
            return action, min_raise

    elif len(game.board) != 0:
        if game.players[game.current_player].state == PlayerState.IN:
            return ActionType.CHECK, None
        p_win = proba_win(game)
        print("p_win : ", p_win)
        print("cote : ", obtenir_cote(game))
        print("cote pourcentage", cote_en_pourcentage(obtenir_cote(game)))
        print("p win * 100 : ", p_win * 100)
        if p_win * 100 > cote_en_pourcentage(obtenir_cote(game)):
            move, total = game.get_available_moves().sample()

            print("on sample une action")
            return move, total

    return ActionType.FOLD, None
