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

class agent_outs:
    def __init__(self):
        self.__game = None
        self.__rank = {
            "Straight Flush":1,
            "Four of a Kind":2,
            "Full House":3,
            "Flush":4,
            "Straight":5,
            "Three of a Kind":6,
            "Two Pair":7,
            "Pair":8,
            "High card":9,
        }

        self.__info_combi = {}
        self.__best_possible_hand = {9:0}
        self.__agent_cards = None



    def setGame(self, g : TexasHoldEm):
        self.__game = g

    def choix(self):
        len_cards_game_board = len(self.__game.board)
        nb_cards = 52

        if len_cards_game_board == 0:
            return strategie_preflop1(self.__game)

        if len_cards_game_board == 3 or len_cards_game_board == 4:
            self.__agent_cards = self.__game.hands[self.__game.current_player]
            d = Deck()
            cards = d.draw(num=nb_cards)
            other_cards = [card for card in cards if card not in self.__agent_cards and card not in self.__game.board]

            current_rank = evaluate(self.__agent_cards,self.__game.board)

            elements = self.__agent_cards + self.__game.board
            self.__info_combi = {}
            self.__best_possible_hand = {9:0}
            combinaisons = generer_combinaisons(4, elements)
            #print("elements : ", elements)

            for id, combinaison in enumerate(combinaisons):
                self.__info_combi[id] = defaultdict(int)
                for card in other_cards:
                    new_hand = combinaison + (card,)
                    rank = evaluate(new_hand[:2], new_hand[2:])
                    rank = self.__rank[rank_to_string(rank)]
                    self.__info_combi[id][rank] += 1
                    if rank <= list(self.__best_possible_hand.keys())[0]:
                        self.__best_possible_hand = {rank:self.__info_combi[id][rank]}

                self.__info_combi[id] = sorted(self.__info_combi[id].items(), key=lambda item: item[0])
                #print(self.__info_combi[id])

            chance = self.__best_possible_hand[list(self.__best_possible_hand.keys())[0]]*2
            #print("chance : ", chance)
            pot_odd = cote_en_pourcentage(obtenir_cote(self.__game))

            if self.__game.players[self.__game.current_player].state == PlayerState.IN:
                #print("flop check")
                action_type = ActionType.CHECK
            elif (self.__game.players[self.__game.current_player].state == PlayerState.TO_CALL) and chance > pot_odd :
                #print("call, p =" ,p, "p_win=",p_win)
                action_type = ActionType.CALL
            else:
                #print("fold, p =", p, " p_win=", p_win)
                action_type = ActionType.FOLD

        else:
            current_rank = evaluate(self.__agent_cards,self.__game.board)
            rank = self.__rank[rank_to_string(current_rank)]
            good_hand = False
            if rank <= list(self.__best_possible_hand.keys())[0]:
                good_hand = True
            if self.__game.players[self.__game.current_player].state == PlayerState.IN:
                #print("flop check")
                action_type = ActionType.CHECK
            elif (self.__game.players[self.__game.current_player].state == PlayerState.TO_CALL) and good_hand:
                #print("call, p =" ,p, "p_win=",p_win)
                action_type = ActionType.CALL
            else:
                #print("fold, p =", p, " p_win=", p_win)
                action_type = ActionType.FOLD




        return action_type, None

"""
def agent_outs(game: TexasHoldEm):
    len_cards_game_board = len(game.board)
    if len(game.board) == 0:
        return strategie_preflop1(game)


    elif len_cards_game_board == 3 or len_cards_game_board == 4:
        player_cards = game.hands[game.current_player]
        nb_cards = 52
        board_cards = game.board


        #FLOP
        d = Deck()
        cards = d.draw(num=nb_cards)
        other_cards = [card for card in cards if card not in player_cards and card not in board_cards]

        current_rank = evaluate(player_cards,board_cards)

        elements = player_cards + board_cards

        RANK = {
            "Straight Flush":1,
            "Four of a Kind":2,
            "Full House":3,
            "Flush":4,
            "Straight":5,
            "Three of a Kind":6,
            "Two Pair":7,
            "Pair":8,
            "High card":9,
        }




        combinaisons = generer_combinaisons(4, elements)
        #print("elements : ", elements)
        info_combi = {}
        best_possible_hand = {9:0}
        for id, combinaison in enumerate(combinaisons):
            info_combi[id] = defaultdict(int)
            for card in other_cards:
                new_hand = combinaison + (card,)
                rank = evaluate(new_hand[:2], new_hand[2:])
                rank = RANK[rank_to_string(rank)]
                info_combi[id][rank] += 1
                if rank <= list(best_possible_hand.keys())[0]:
                    best_possible_hand = {rank:info_combi[id][rank]}

            info_combi[id] = sorted(info_combi[id].items(), key=lambda item: item[0])
            #print(info_combi[id])

        chance = best_possible_hand[list(best_possible_hand.keys())[0]]*2
        #print("chance : ", chance)
        pot_odd = cote_en_pourcentage(obtenir_cote(game))

        if game.players[game.current_player].state == PlayerState.IN:
            #print("flop check")
            action_type = ActionType.CHECK
        elif (game.players[game.current_player].state == PlayerState.TO_CALL) and chance > pot_odd :
            #print("call, p =" ,p, "p_win=",p_win)
            action_type = ActionType.CALL
        else:
            #print("fold, p =", p, " p_win=", p_win)
            action_type = ActionType.FOLD

    if game.players[game.current_player].state == PlayerState.IN:
        #print("flop check")
        action_type = ActionType.CHECK
    elif (game.players[game.current_player].state == PlayerState.TO_CALL):
        #print("call, p =" ,p, "p_win=",p_win)
        action_type = ActionType.CALL
    else:
        #print("fold, p =", p, " p_win=", p_win)
        action_type = ActionType.FOLD




    return action_type, None
"""
