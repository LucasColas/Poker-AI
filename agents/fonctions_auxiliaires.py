from texasholdem.game.game import TexasHoldEm, Pot
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.evaluator.evaluator import *
from texasholdem.gui.text_gui import TextGUI
from typing import Tuple
import itertools

import numpy as np

def conversion(game: TexasHoldEm):

    Conversion = {'1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    nbr1 = Conversion[str(game.hands[game.current_player])[7]]
    #str(game.hands[game.current_player])[7].translate(str.maketrans(Conversion))
    coul1 = str(game.hands[game.current_player])[8]
    nbr2 = Conversion[str(game.hands[game.current_player])[19]]

    coul2 = str(game.hands[game.current_player])[20]
    return nbr1, coul1, nbr2, coul2


def obtenir_cote(game: TexasHoldEm):
    """
    Fonction permettant d'obtenir la cote actuelle du pot.
    """

    id_last_pot = -1
    #print("pot actuel",game.pots[id_last_pot].get_total_amount())
    pot_actuel = game.pots[id_last_pot].get_total_amount()
    chips_to_call = game.pots[id_last_pot].chips_to_call(game.current_player)
    #print("chips to call", chips_to_call)
    if chips_to_call != 0:
        #print("cote actuelle : ", pot_actuel / chips_to_call)
        return round(pot_actuel / chips_to_call, 2)
    return 1

def cote_en_pourcentage(cote: int):
    """
    Fonction qui renvoie la cote en pourcentage.

    """
    return (1/cote)*100


def strategie_preflop1(game: TexasHoldEm):
    """
    Fonction qui implémente la première stratégie preflop :
    continuer à jouer uniquement si on a un début de mains.
    """
    nbr1, coul1, nbr2, coul2 = conversion(game)

    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips
    total = None

    if game.players[game.current_player].state == PlayerState.IN:
        action_type = ActionType.CHECK
    elif (max_raise > min_raise) and (game.players[game.current_player].state == PlayerState.TO_CALL):
        if (nbr1==nbr2) or (coul1==coul2) or (abs(nbr1-nbr2)==1) or (abs(nbr1-nbr2)==12):
            action_type = ActionType.CALL

        else:
            action_type = ActionType.FOLD
    else :
        action_type = ActionType.FOLD

    return (action_type, total)


def generer_combinaisons(k : int, elements : List[Card]):

    return list(itertools.combinations(elements, k))
