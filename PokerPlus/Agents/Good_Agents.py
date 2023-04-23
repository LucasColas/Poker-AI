
from texasholdem.game.game import TexasHoldEm

#PokerPlus
from PokerPlus.Agents.fonctions_auxiliaires import *
import random

class agent_SA():
    """
    Stratégie :
    Preflop : joue uniquement s'il a une paire de mains vraiment intéressante. Prendre aussi en
    compte la position du joueur. Raise si paire particulière.
    Flop : si bonne condition alors raise.
    bonne condition :
        -Bonne main. Par exemple nombre de mains battue > seuil. Seuil pris au hasard entre 0,5 et 1,0.
        -Prendre en compte la position
        -Prendre en compte la taille du pot.
    Turn : Pareil.
    River : Pareil.
    Raise aléatoire aussi. Raise découpé en nombre de small blind.
    Si la main n'est pas bonne, autoriser de temps en temps à jouer.
    """

    def __init__(self, min=0.5, seuil_random=0.15):
        self.pos = None
        self.min = min
        self.max = 1.0
        #Plus l'entier associé est grand meilleure est la position
        self.rank_pos = {
                        "Small Blind":0,
                        "Big Blind":0,
                        "Cut Off":2,
                        "Button":3,
                        "Other":1
        }
        self.last_action = None
        self.seuil_random = seuil_random

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, val):
        self._min = val

    def getPosition(self, game: TexasHoldEm):
        if game.players[game.current_player] == game.btn_loc:
            self.pos = "Button"

        elif game.players[game.current_player] == game.sb_loc:
            self.pos = "Small Blind"

        elif game.players[game.current_player] == game.bb_loc:
            self.pos = "Big Blind"

        elif game.players[game.current_player] == game.btn_loc-1:
            self.pos = "Cut Off"

        else:
            self.pos = "Other"



    def strategie_preflop(self, game: TexasHoldEm):
        """
        self.getPosition(game)
        nbr1, coul1, nbr2, coul2 = conversion(game)
        bet_amount = game.player_bet_amount(game.current_player)
        chips = game.players[game.current_player].chips
        min_raise = game.value_to_total(game.min_raise(), game.current_player)
        max_raise = chips

        action_type = None
        total = None
        if (nbr1 == nbr2 and (nbr1 == 14 or nbr1 == 13 or nbr1 == 12)) or ((nbr1 == 14 or nbr2 == 14) and (nbr1 == 12 or nbr2 == 12)):

            if game.players[game.current_player].state == PlayerState.IN:
                    #print("flop check")
                action_type = ActionType.CHECK
                #print("check")
                self.last_action = ActionType.FOLD
                return action_type, total
            elif (max_raise > min_raise) and (game.players[game.current_player].state == PlayerState.TO_CALL):
                    #print("call, p =" ,p, "p_win=",p_win)
                action_type = ActionType.RAISE
                print("min raise : ",min_raise)
                total = random.randint(min_raise, max_raise)
                print("raise : ", total)
                self.last_action = action_type
                return action_type, total

            else:
                print("Fold preflop")
                self.last_action = ActionType.FOLD
                return ActionType.FOLD, total


        print("Fold preflop")
        return ActionType.FOLD, total
        """
        nbr1, coul1, nbr2, coul2 = conversion(game)
        print("strategie preflop")
        bet_amount = game.player_bet_amount(game.current_player)
        chips = game.players[game.current_player].chips
        min_raise = game.value_to_total(game.min_raise(), game.current_player)
        max_raise = bet_amount + chips
        total = None
        action_type = ActionType.FOLD

        if game.players[game.current_player].state == PlayerState.IN:
            
            if (min_raise > max_raise):
                action_type = ActionType.RAISE
                total = min_raise
            else:
                action_type = ActionType.CHECK
            return action_type, total

        elif (game.players[game.current_player].state == PlayerState.TO_CALL):
            if (nbr1==nbr2) or (coul1==coul2) or (abs(nbr1-nbr2)==1) or (abs(nbr1-nbr2)==12):
                if (min_raise < max_raise):
                    action_type = ActionType.RAISE
                    print("min raise : ",min_raise)
                    print("max raise : ", max_raise)
                    total = random.randint(min_raise, max_raise)
                    print("raise : ", total)
                    return action_type, total
                else:
                    action_type = ActionType.FOLD
                return action_type, total

            else:
                p = random.random()
                if p < self.seuil_random:
                    action_type = ActionType.CALL
                else:
                    action_type = ActionType.FOLD
                return action_type, total
        else :
            action_type = ActionType.FOLD

        self.last_action = action_type
        return action_type, total


    def strategie_flop(self, game: TexasHoldEm):
        rank = evaluate(game.hands[game.current_player], game.board)
        p_win = get_five_card_rank_percentage(rank)
        p = random.random()
        bet_amount = game.player_bet_amount(game.current_player)
        chips = game.players[game.current_player].chips
        min_raise = game.value_to_total(game.min_raise(), game.current_player)
        max_raise = bet_amount + chips
        action_type = None
        total = None
        if p_win >= self.min or p < self.seuil_random:


            if game.players[game.current_player].state == PlayerState.IN:
                    #print("flop check")
                
                action_type = ActionType.CHECK
                return action_type, total

            elif (max_raise > min_raise) and (game.players[game.current_player].state == PlayerState.TO_CALL):
                    #print("call, p =" ,p, "p_win=",p_win)
                action_type = ActionType.RAISE
                print("prend total")
                total = random.randint(min_raise, max_raise)
                print("raise", total)
                print("flop turn ou river : ", action_type, total)
                self.last_action = action_type
                return action_type, total

            else:
                self.last_action = ActionType.FOLD
                return ActionType.FOLD, total

        self.last_action = ActionType.FOLD
        return ActionType.FOLD, total




    def strategie_turn(game: TexasHoldEm):
        pass

    def strategie_river(game: TexasHoldEm):
        pass

    def action(self, game: TexasHoldEm) -> Tuple[ActionType, int]:
        if len(game.board) == 0:
            return self.strategie_preflop(game)

        else:
            return self.strategie_flop(game)

    def __str__(self):
        print("Agent Serré Agressif")
