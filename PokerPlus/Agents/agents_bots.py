from time import sleep
from typing import Tuple
import random

from texasholdem.game.game import TexasHoldEm, Pot
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.evaluator.evaluator import *
from texasholdem.gui.text_gui import TextGUI

from PokerPlus.Agents.fonctions_auxiliaires import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
import os
#print(os.getcwd())


def agent_naif(game: TexasHoldEm) -> Tuple[ActionType, int]:
    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips
    total = None

    #pre-flop
    #Strategie : on CHECK si on peut, on CALL si on a un début de main et sinon on FOLD
    if len(game.board) == 0:
        nbr1, coul1, nbr2, coul2 = conversion(game)
        if game.players[game.current_player].state == PlayerState.IN:
            action_type = ActionType.CHECK
        elif (max_raise > min_raise) and (game.players[game.current_player].state == PlayerState.TO_CALL):
            if (nbr1==nbr2) or (coul1==coul2) or (abs(nbr1-nbr2)==1) or (abs(nbr1-nbr2)==12):
                action_type = ActionType.CALL
            else:
                action_type = ActionType.FOLD
        else :
            action_type = ActionType.FOLD

    #FLOP Turn River
    #Strategie : on CHECK si on peut, on RAISE si on a une chance de gagner et sinon on FOLD
    elif len(game.board) != 0:
        rank = evaluate(game.hands[game.current_player],game.board)
        p_win = get_five_card_rank_percentage(rank)
        p = random.random()
        if game.players[game.current_player].state == PlayerState.IN:
            #print("flop check")
            action_type = ActionType.CHECK
        elif (game.players[game.current_player].state == PlayerState.TO_CALL) and (p<p_win) and (max_raise > min_raise) :
            action_type = ActionType.RAISE
            total = min_raise
        else:
            #print("fold, p =", p, " p_win=", p_win)
            action_type = ActionType.FOLD

    return action_type, total


def agent_serre_non_agressif(game: TexasHoldEm, seuil: int=0.4):
    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips
    total = None
    #pre-flop
    #Strategie : on CHECK si on peut, on fold si on a un début de main et sinon on call
    if len(game.board) == 0:
        nbr1, coul1, nbr2, coul2 = conversion(game)

        if game.players[game.current_player].state == PlayerState.IN:
            action_type = ActionType.CHECK
        elif (max_raise > min_raise) and (game.players[game.current_player].state == PlayerState.TO_CALL):
            if (nbr1==nbr2) and (nbr1 >= 10):
                action_type = ActionType.CALL
            else:
                action_type = ActionType.FOLD

        else :
            action_type = ActionType.FOLD

    #FLOP Turn River
    elif len(game.board) != 0:
        rank = evaluate(game.hands[game.current_player],game.board)
        p_win = get_five_card_rank_percentage(rank)


        if (game.players[game.current_player].state == PlayerState.IN) and (p_win > seuil) and (max_raise > min_raise):
        
            action_type = ActionType.CALL

        else:
            action_type = ActionType.FOLD
    return action_type, total


def agent_large_non_agressif(game: TexasHoldEm, seuil: int=0.1):
    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips
    total = None
    #pre-flop
    #Strategie : on CHECK si on peut, on fold si on a un début de main et sinon on call
    if len(game.board) == 0:
        nbr1, coul1, nbr2, coul2 = conversion(game)

        if game.players[game.current_player].state == PlayerState.IN:
            action_type = ActionType.CHECK
        elif (max_raise > min_raise) and (game.players[game.current_player].state == PlayerState.TO_CALL):
            if (nbr1 >= 9 and nbr2 >= 9) or (nbr1 == nbr2) or (coul1 == coul2):
                action_type = ActionType.CALL
            else:
                action_type = ActionType.FOLD

        else :
            action_type = ActionType.FOLD

    #FLOP Turn River
    elif len(game.board) != 0:
        rank = evaluate(game.hands[game.current_player],game.board)
        p_win = get_five_card_rank_percentage(rank)

        if (game.players[game.current_player].state == PlayerState.IN):
            action_type = ActionType.CHECK

        elif (game.players[game.current_player].state == PlayerState.IN) and (p_win > seuil) and (max_raise > min_raise):
        
            action_type = ActionType.CALL

        else:
            action_type = ActionType.FOLD
    return action_type, total

def agent_allIn(game: TexasHoldEm, seuil: int = 0.1): #Agressif et large
    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips
    total = None
    #pre-flop
    #Strategie : on CHECK si on peut, on CALL si on a un début de main et sinon on FOLD
    if len(game.board) == 0:
        nbr1, coul1, nbr2, coul2 = conversion(game)

        #on joue si on a une paire, deux cartes de la meme couleur ou 2 cartes consecutives
        # attention l'as peut etre considere comme 1 ou 14 donc on fait attention

        if game.players[game.current_player].state == PlayerState.IN and (max_raise > min_raise):
            action_type = ActionType.ALL_IN
        
        elif (max_raise > min_raise) and (game.players[game.current_player].state == PlayerState.TO_CALL):
            """
            
            if (nbr1==nbr2) or (coul1==coul2) or (abs(nbr1-nbr2)==1) or (abs(nbr1-nbr2)==12):
                action_type = ActionType.ALL_IN
            else:
                action_type = ActionType.FOLD
            """
            action_type = ActionType.ALL_IN
        else :
            action_type = ActionType.FOLD

    #FLOP Turn River
    #Strategie : si le pourcentage de mains battu par notre main est supérieur au seuil alors le
    #bot fait ALL_IN, FOLD sinon.
    elif len(game.board) != 0:
        rank = evaluate(game.hands[game.current_player],game.board)
        p_win = get_five_card_rank_percentage(rank)

        if (game.players[game.current_player].state == PlayerState.IN) and (p_win >seuil) and (max_raise > min_raise):
            action_type = ActionType.CHECK
        elif (game.players[game.current_player].state == PlayerState.TO_CALL) and (p_win >seuil) and (max_raise > min_raise) :
            action_type = ActionType.ALL_IN
        else:
            action_type = ActionType.FOLD
    if (action_type == ActionType.ALL_IN):
        total = max_raise
    return action_type, total



def agent_saboteur(game: TexasHoldEm):
    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips
    total = None
    #pre-flop
    #Strategie : on CHECK si on peut, on fold si on a un début de main et sinon on call
    if len(game.board) == 0:
        nbr1, coul1, nbr2, coul2 = conversion(game)

        if game.players[game.current_player].state == PlayerState.IN:
            action_type = ActionType.CHECK
        elif (max_raise > min_raise) and (game.players[game.current_player].state == PlayerState.TO_CALL):
            if (nbr1==nbr2) or (coul1==coul2) or (abs(nbr1-nbr2)==1) or (abs(nbr1-nbr2)==12):
                action_type = ActionType.FOLD
            else:
                action_type = ActionType.CALL

        else :
            action_type = ActionType.FOLD

    #FLOP Turn River
    #Strategie : joue si il a que moins de 5% de chance de gagner
    elif len(game.board) != 0:
        rank = evaluate(game.hands[game.current_player],game.board)
        p_win = get_five_card_rank_percentage(rank)


        if (game.players[game.current_player].state == PlayerState.IN) and (p_win < 0.05) and (max_raise > min_raise):
            action_type = ActionType.RAISE
            total = min_raise
        elif (game.players[game.current_player].state == PlayerState.TO_CALL) and (p_win < 0.05):
            action_type = ActionType.CALL

        else:
            action_type = ActionType.FOLD
    return action_type, total
