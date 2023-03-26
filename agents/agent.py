from time import sleep
from typing import Tuple

import random

from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.evaluator.evaluator import *
from texasholdem.gui.text_gui import TextGUI


def agent_naif(game: TexasHoldEm) -> Tuple[ActionType, int]:
    #sleep(2)
    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips
    total = None
    print(game.current_player,": agent_naif")
    #pre-flop
    #Strategie : on CHECK si on peut, on CALL si on a une main particuliere et sinon on FOLD
    if len(game.board) == 0:
        print("mes cartes sont:",game.hands[game.current_player])
        #on recupere les 2 cartes de la main du joueur:  nbr1 = 4, coul1 = c, nbr2 = 2, coul2 = d
        #Pour les nbr on transforme les lettres en chiffres : "T" -> 10,"J" -> 11, "Q" -> 12,"K" -> 13, "A" -> 14
        nbr1 = str(game.hands[game.current_player])[7].translate(str.maketrans({'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'} ) )
        coul1 = str(game.hands[game.current_player])[8]
        nbr2 = str(game.hands[game.current_player])[19].translate(str.maketrans({'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}))
        coul2 = str(game.hands[game.current_player])[20]

        print(nbr1,nbr2)
        print("couleur : ", coul1, coul2)
        #on joue si on a une paire, deux cartes de la meme couleur ou 2 cartes consecutives
        # attention l'as peut etre considere comme 1 ou 14 donc on fait attention
        # pour resoudre cela nous allons verifier que la difference entre les 2 cartes est 1 ou 12

        if game.players[game.current_player].state == PlayerState.IN:
            action_type = ActionType.CHECK
            print("pre flop check")
        elif (max_raise > min_raise) and (game.players[game.current_player].state == PlayerState.TO_CALL):
            if (nbr1==nbr2) or (coul1==coul2) or (abs(int(nbr1)-int(nbr2))==1) or (abs(int(nbr1)-int(nbr2))==12):
                action_type = ActionType.CALL
                print("pre flop call car main ok")
            else:
                print("pre flop Fold car main non ok")
                action_type = ActionType.FOLD
        else :
            print("pre flop fold")
            action_type = ActionType.FOLD

    #FLOP Turn River
    #Strategie : on CHECK si on peut, on CALL si on a une chance de gagner et sinon on FOLD
    elif len(game.board) != 0:
        rank = evaluate(game.hands[game.current_player],game.board)
        p_win = get_five_card_rank_percentage(rank)
        p = random.random()
        if game.players[game.current_player].state == PlayerState.IN:
            print("flop check")
            action_type = ActionType.CHECK
        elif (game.players[game.current_player].state == PlayerState.TO_CALL) and (p<p_win) and (max_raise > min_raise) :
            print("call, p =" ,p, "p_win=",p_win)
            action_type = ActionType.CALL
        else:
            print("fold, p =", p, " p_win=", p_win)
            action_type = ActionType.FOLD

    return action_type, total
