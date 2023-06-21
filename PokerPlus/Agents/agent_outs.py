from texasholdem.game.game import TexasHoldEm, Pot
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.evaluator.evaluator import *
from texasholdem.gui.text_gui import TextGUI
from texasholdem.card.deck import Deck
from texasholdem.evaluator.lookup_table import LOOKUP_TABLE
from PokerPlus.Agents.fonctions_auxiliaires import *
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
        self.__bet_amount = None
        self.__chips = None
        self.__min_raise = None
        self.__max_raise = None
        self.__total = None
        self.__nb_check_consecutifs = 0



    def setGame(self, g : TexasHoldEm):
        self.__game = g

    def action_river(self, good_hand):
        self.raise_config()
        if self.__game.players[self.__game.current_player].state == PlayerState.IN:
            #print("flop check")
            """
            p = random.random()
            if p > 0.5 and self.__min_raise < self.__max_raise:
                action_type = ActionType.CALL
            else:
                action_type = ActionType.CHECK
            """
            action_type = ActionType.CHECK
            self.__nb_check_consecutifs += 1
            

        elif (self.__game.players[self.__game.current_player].state == PlayerState.TO_CALL) and good_hand and (self.__min_raise < self.__max_raise):
            #print("call, p =" ,p, "p_win=",p_win)
            action_type = ActionType.RAISE
            self.__total = self.__max_raise
        elif (self.__game.players[self.__game.current_player].state == PlayerState.TO_CALL) and (self.__min_raise < self.__max_raise):
            rank = evaluate(self.__game.hands[self.__game.current_player],self.__game.board)
            p_win = get_five_card_rank_percentage(rank)
            p = random.random()
            
            if (self.__max_raise > self.__min_raise) and (self.__game.players[self.__game.current_player].state == PlayerState.TO_CALL) and (p<p_win):
                #print("call, p =" ,p, "p_win=",p_win)
                action_type = ActionType.RAISE
                if (self.__game.big_blind*3) > self.__min_raise:
                    self.__total = random.randint(self.__min_raise, self.__game.big_blind*3)

                else:
                    self.__total = random.randint(self.__min_raise, self.__max_raise)
        else:
            #print("fold, p =", p, " p_win=", p_win)
            action_type = ActionType.FOLD

        return action_type, self.__total

    def raise_config(self):
        self.__bet_amount = self.__game.player_bet_amount( self.__game.current_player)
        self.__chips =  self.__game.players[self.__game.current_player].chips
        self.__min_raise =  self.__game.value_to_total( self.__game.min_raise(),  self.__game.current_player)
        self.__max_raise = self.__bet_amount + self.__chips
        self.__total = None




    def choix(self, g: TexasHoldEm):
        self.setGame(g)
        len_cards_game_board = len(self.__game.board)
        nb_cards = 52


        if len_cards_game_board == 0:
            return strategie_preflop_raise(self.__game)

        elif len_cards_game_board == 3 or len_cards_game_board == 4:
            self.raise_config()
            self.__agent_cards = self.__game.hands[self.__game.current_player]
            d = Deck()
            cards = d.draw(num=nb_cards)
            p = random.random()
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
                if self.__nb_check_consecutifs >= 1 and self.__min_raise < self.__max_raise:
                    action_type = ActionType.RAISE
                    self.__total = random.randint(self.__min_raise, min(self.__game.big_blind*3, self.__max_raise))
                    self.__nb_check_consecutifs = 0
                else:    
                    action_type = ActionType.CHECK
                    self.__nb_check_consecutifs += 1
            elif (self.__max_raise > self.__min_raise) and (self.__game.players[self.__game.current_player].state == PlayerState.TO_CALL) and chance >= pot_odd :
                #print("call, p =" ,p, "p_win=",p_win)
                action_type = ActionType.RAISE
                if 0.5*self.__max_raise > self.__min_raise:
                    self.__total = random.randint(self.__min_raise, int(0.5*self.__max_raise))
                else:
                    self.__total = random.randint(self.__min_raise, self.__max_raise)
            else:
                #print("fold, p =", p, " p_win=", p_win)
                """
                
                rank = evaluate(self.__game.hands[self.__game.current_player],self.__game.board)
                p_win = get_five_card_rank_percentage(rank)
                if p_win > p:
                    action_type = ActionType.CALL
                else:
                """
                moves = self.__game.get_available_moves()
                return moves.sample()

        else:
            current_rank = evaluate(self.__agent_cards,self.__game.board)
            rank = self.__rank[rank_to_string(current_rank)]
            good_hand = False
            #print("rnk : ",rank)
            #print(self.__best_possible_hand.keys())
            if rank >= list(self.__best_possible_hand.keys())[0]:
                good_hand = True
            return self.action_river(good_hand)

        return action_type, self.__total
