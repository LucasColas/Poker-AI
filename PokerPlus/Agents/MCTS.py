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
from PokerPlus.Agents.fonctions_auxiliaires import obtenir_cote,cote_en_pourcentage

from PokerPlus.Agents.agents_bots import agent_naif

from texasholdem.game.history import (
    History,
    PrehandHistory,
    BettingRoundHistory,
    PlayerAction,
    HistoryImportError,
    SettleHistory,
)


def generate_game(history, blinds, gui=False):
    """
    print("history : ", history)
    num_players = len(history.prehand.player_chips)
    game = TexasHoldEm(
            buyin=1,
            big_blind=history.prehand.big_blind,
            small_blind=history.prehand.small_blind,
            max_players=num_players,
    )

        # button placed right before 0
    game.btn_loc = num_players - 1

    # read chips
    for i in game.player_iter(0):
        game.players[i].chips = history.prehand.player_chips[i]

    # stack deck
    deck = Deck()
    if history.settle:
        deck.cards = list(history.settle.new_cards)

    # player actions in a stack
    player_actions = []
    for bet_round in (history.river, history.turn, history.flop, history.preflop):
        if bet_round:
            deck.cards = bet_round.new_cards + deck.cards
            for action in reversed(bet_round.actions):
                player_actions.insert(
                    0, (action.player_id, action.action_type, action.total)
                )

    # start hand (deck will deal)

    game.start_hand()
    print("sb_loc : ", game.sb_loc)
    print("bb_loc : ", game.bb_loc)
    
    #game.current_player = next(game.in_pot_iter(loc=game.bb_loc + 1))


        # give players old cards
    for i in game.player_iter():
        game.hands[i] = history.prehand.player_cards[i]

    

        # swap decks
    if not history.settle:
        #Les cartes sauf celles des mains des joueurs
        cards = []
        for card in deck.cards:
            for hand in game.hands.values():
                if card in hand:
                    cards.append(card)

        deck.cards = cards
    game._deck = deck
    print("game hands", game.hands)

    while game.is_hand_running():
        if gui:
            gui = TextGUI(game=game)
            gui.display_state()
            gui.wait_until_prompted()

        try:
            
            player_id, action_type, total = player_actions.pop(0)
            print("player_id : ", player_id)
            print("current_player : ", game.current_player)
            game.take_action(action_type=action_type, total=total)
        except:
            action, total = random_agent(game)
            print("current_player : ", game.current_player)
            game.take_action(action_type=action, total=total)

    """
    num_players = len(history.prehand.player_chips)
    game = TexasHoldEm(
            buyin=1,
            big_blind=history.prehand.big_blind,
            small_blind=history.prehand.small_blind,
            max_players=num_players,
        )
    
    gui = TextGUI(game=game)

        # button placed right before 0
    game.btn_loc = num_players - 1

        # read chips
    for i in game.player_iter(0):
        game.players[i].chips = history.prehand.player_chips[i]

        # stack deck
    deck = Deck()
    if history.settle:
        deck.cards = list(history.settle.new_cards)


        # player actions in a stack
    player_actions  = []
    for bet_round in (history.river, history.turn, history.flop, history.preflop):
        if bet_round:
            deck.cards = bet_round.new_cards + deck.cards
            for action in reversed(bet_round.actions):
                player_actions.insert(
                    0, (action.player_id, action.action_type, action.total)
                )

    # start hand (deck will deal)
    game.start_hand()

    # give players old cards
    for i in game.player_iter():
        game.hands[i] = history.prehand.player_cards[i]

        # swap decks
    game._deck = deck

    while game.is_hand_running():
        gui.display_state()
        gui.wait_until_prompted()
        try:
            player_id, action_type, total = player_actions.pop(0)
            game.take_action(action_type=action_type, total=total)
        except:
            action, total = random_agent(game)
            game.take_action(action_type=action, total=total)

        gui.display_action()

    gui.display_win()
    

    
    
            


def cloneTexasHoldem(actions, Blinds, mains_player, cards_boards, buyin, big_blind, small_blind, nb_players, num_MCTS):
    game = TexasHoldEm(buyin, big_blind, small_blind, nb_players)
    num_partie = 0
    gui = TextGUI(game=game)
    

    while game.is_game_running():
        num_partie += 1
        game.start_hand()
        game.hands = mains_player[num_partie]
        game.sb_loc = Blinds[num_partie][0]
        game.bb_loc = Blinds[num_partie][1]
        num_action = 0
        while game.is_hand_running():

            action_type, total = actions[num_partie][num_action][0], actions[num_partie][num_action][1]
            game.take_action(action_type=action_type, total=total)
            num_action += 1

            #Terminer la partie avec du random
            
            #mains_player[num_partie] = (game.current_player, game.hands[game.current_player])
            if len(game.board) != 0:
                game.board = cards_boards[num_partie][0:len(game.board)]


        #Score : 
        #Nombre de jetons gagné 
        #Et ensuite return le score à la fin de la main



def cloneTexasHoldem2(actions, Blinds, mains_player, cards_boards, buyin, big_blind, small_blind, nb_players, num_MCTS, btn_loc, next_action):
    #TODO virer le gui
    game = TexasHoldEm(buyin, big_blind, small_blind, nb_players)

    while (game.btn_loc != btn_loc): #Pour avoir le même croupier
        game = TexasHoldEm(buyin, big_blind, small_blind, nb_players)
    
    num_partie = 0
    #gui = TextGUI(game=game)

    # on regarde cb de partie on a dans actions
    num_partie_save = len(actions)
    print(f" on  a {num_partie_save} parties")
    ok = True
    while game.is_game_running():
        num_partie += 1

        game.start_hand()

        #TODO : vérifier que les cartes du tableau ou du joueur MCTS ne sont pas distribuées
        if num_partie == num_partie_save:
            game.sb_loc = Blinds[num_partie][0]
            game.bb_loc = Blinds[num_partie][1]
            print("game hands", game.hands)
            print("num partie : ", num_partie)
             
            for id in game.hands:
                print("id :", id)
                
                while num_partie in cards_boards and (game.hands[id][0] in cards_boards[num_partie] or game.hands[id][1] in cards_boards[num_partie]):
                    #Changer la carte 

                    
                    if game.hands[id][0] in cards_boards[num_partie]:

                        game.hands[id][0] = game._deck.draw(num=1)

                    if game.hands[id][1] in cards_boards[num_partie]:
                        game.hands[id][1] = game._deck.draw(num=1)

                while game.hands[id][0] in mains_player[num_partie][num_MCTS] or game.hands[id][1] in mains_player[num_partie][num_MCTS]:
                    #Changer la carte 
                    
                    if game.hands[id][0] in mains_player[num_partie][num_MCTS]:

                        game.hands[id][0] = game._deck.draw(num=1)

                    if game.hands[id][1] in mains_player[num_partie][num_MCTS]:
                        game.hands[id][1] = game._deck.draw(num=1)

            game.hands[num_MCTS] = mains_player[num_partie][num_MCTS]
            index = 0
            for hand in game._deck.cards:
                if hand in game.hands[num_MCTS]:
                    game.hands[num_MCTS][0] = hand 
                    game._deck.cards.remove(hand)
                    index += 1

            print("game hands : ", game.hands)
            


        if num_partie < num_partie_save:
            
            game.hands = mains_player[num_partie]
            game.sb_loc = Blinds[num_partie][0]
            game.bb_loc = Blinds[num_partie][1]
        num_action = 0
        while game.is_hand_running():
            #gui.display_state()
            #gui.wait_until_prompted()
            print("state :", game.hand_phase)

            #Problème : évaluation causé par l'évaluation des bits
            # Remplacer les cartes stockées par les "même" cartes venant du deck.
            for id in game.hands:
                if game.hands[id][0] in game.board or game.hands[id][1] in game.board:
                    
                    print("erreur. cartes : ", game.hands[id])

                if game.hands[id][0] in game.board or game.hands[id][1] in game.board:
                    print("erreur. cartes : ", game.hands[id])

                

                #print("evaluate : ", evaluate(game.hands[id], game.board))

            

            #print("deck  : ", game._deck)
            print("game hands : ", game.hands)
            #print("cards boards : ", cards_boards)
            #print("game board : ", game.board)

           


            #on refait la game 
            #print(f"num_p = {num_partie}, num_a = {num_action}")
            if num_partie in actions.keys() and num_action in actions[num_partie].keys():
                action_type, total = actions[num_partie][num_action][0], actions[num_partie][num_action][1]
                game.take_action(action_type=action_type, total=total)
                num_action += 1
                if len(game.board) != 0:
                    print("ecrase tableau")
                    game.board = cards_boards[num_partie][0:len(game.board)]

            #Terminer la partie avec du random
            elif ok == True:
                action_type, total = next_action
                game.take_action(action_type=action_type, total=total)
                ok = False
            else:
                #
                action, total = game.get_available_moves().sample()
                #print(f"action : {action}")
                game.take_action(action_type=action, total=total)
            #mains_player[num_partie] = (game.current_player, game.hands[game.current_player])
            

            #gui.display_action()

        #gui.display_win()

        

        #Score : 
        #Nombre de jetons gagné a la fin de la partie
        if ok ==False:
            for p in game.players:
                if p.player_id == num_MCTS:
                    print(f"fin de la partie simule avec le coup {next_action}, on retourne {p.chips}")
                    return p.chips

        #Et ensuite return le score à la fin de la main

def choix_MCTS(nbr_de_simu_par_action,game, actions, Blinds, mains_player, cards_boards, buyin, big_blind, small_blind, nb_players, num_MCTS, btn_loc):
    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips
    
    
    score = {}
    available_moves = game.get_available_moves()
    for i in range(nbr_de_simu_par_action):
        #action du type fold, call, allin,check avec none ou raise avec min_raise
        #print(f"nbr : {len(available_moves)}")
        
        #TODO trop long avec les affichages
        """
        for action,total in available_moves:
            if action == ActionType.RAISE:
                if (max_raise > min_raise):
                    total = random.randint(min_raise, max_raise)
                else:
                    action = ActionType.ALL_IN
                    total = None
            else:
                total = None
        """
        action_ok =[a for a in available_moves if a[0] != ActionType.RAISE]
        for action in action_ok:
            print(f"        simu : {i} |action : {action[0]}, total : {action[1]}")
            next_action = action
            if next_action not in score.keys():
                score[next_action] = [cloneTexasHoldem2(actions, Blinds, mains_player, cards_boards, buyin, big_blind, small_blind, nb_players, num_MCTS, btn_loc,next_action)]
            score[next_action].append(cloneTexasHoldem2(actions, Blinds, mains_player, cards_boards, buyin, big_blind, small_blind, nb_players, num_MCTS, btn_loc,next_action))
            #print(f"        score : {score}")
    print(f"\n\nscore : {score}")
    dico_moy = {}
    for action in score.keys():
        dico_moy[action] = sum(score[action])/len(score[action])
    print(f"dico_moy : {dico_moy}")

    #on prend le max
    max = 0
    for action in dico_moy.keys():
        if dico_moy[action] > max:
            max = dico_moy[action]
            action_max = action
    return action_max


def MainGame(buyin,big_blind, small_blind, nb_players, num_MCTS):
    game = TexasHoldEm(buyin, big_blind, small_blind, nb_players)
    gui = TextGUI(game=game, visible_players=[])
    actions = {} #Dictionnaire qui contiendra pour chaque partie un dictionnaire avec les infos sur les actions des joueurs. La clé sera le num de la main / partie. La valeur un dictionnaire des actions. Pour chaque action, la clé sera l'ordre de l'action. La valeur sera un tuple avec l'action, le total puis le joueur.
    Blinds = {} #Dictionnaire pour stocker les blinds. La clé sera le num de la main/partie. Et la valeur sera un tuple avec les joueurs ayant payé les blinds.
    mains_player = {} #Dictionnaire pour stocker les mains des joueurs. La clé sera le num de la main/partie. Et la valeur sera un dictionnaire avec les joueurs et leurs mains.
    cards_boards = {} #Dictionnaire pour stocker les boards. La clé sera le num de la main/partie. Et la valeur sera un tuple avec les cartes.
    
    num_partie = 0
    
    while game.is_game_running():
        num_partie += 1
        game.start_hand()
        num_action = 0
        Blinds[num_partie] = (game.sb_loc, game.bb_loc)
        actions[num_partie] = {}
        print("mains player", mains_player)
        print("game hands :", game.hands)
        mains_player[num_partie] = {i:game.hands[i] for i in game.hands}
        while game.is_hand_running():
            gui.display_state()
            gui.wait_until_prompted()
            if game.current_player == num_MCTS:
                pass

                #MCTS joue
            else:
                action_type, total = random_agent(game)

            actions[num_partie][num_action] = (action_type, total, game.current_player)
            
            game.take_action(action_type=action_type, total=total)
            num_action += 1
            
            #mains_player[num_partie] = (game.current_player, game.hands[game.current_player])
            if len(game.board) != 0:
                cards_boards[num_partie] = game.board

            print("actions : ", actions)
            print("Blinds : ", Blinds)
            print("mains_player : ", mains_player)
            print("cards_boards : ", cards_boards)
            
            gui.display_action()
        gui.display_win()
        return actions, Blinds, mains_player, cards_boards

def MainGame2(buyin,big_blind, small_blind, nb_players, num_MCTS, nbr_parties):
    game = TexasHoldEm(buyin, big_blind, small_blind, nb_players)
    gui = TextGUI(game=game)
    actions = {} #Dictionnaire qui contiendra pour chaque partie un dictionnaire avec les infos sur les actions des joueurs. La clé sera le num de la main / partie. La valeur un dictionnaire des actions. Pour chaque action, la clé sera l'ordre de l'action. La valeur sera un tuple avec l'action, le total puis le joueur.
    Blinds = {} #Dictionnaire pour stocker les blinds. La clé sera le num de la main/partie. Et la valeur sera un tuple avec les joueurs ayant payé les blinds.
    mains_player = {} #Dictionnaire pour stocker les mains des joueurs. La clé sera le num de la main/partie. Et la valeur sera un dictionnaire avec les joueurs et leurs mains.
    cards_boards = {} #Dictionnaire pour stocker les boards. La clé sera le num de la main/partie. Et la valeur sera un tuple avec les cartes.
    btn_loc = game.btn_loc
    num_partie = 0
    
    while game.is_game_running():
        num_partie += 1
        game.start_hand()
        num_action = 0
        Blinds[num_partie] = (game.sb_loc, game.bb_loc)
        print("Blinds : ", Blinds)
        actions[num_partie] = {}
        #print("mains player", mains_player)
        #print("game hands :", game.hands)
        mains_player[num_partie] = {i:game.hands[i] for i in game.hands}
        while game.is_hand_running():
            gui.display_state()
            gui.wait_until_prompted()
            if game.current_player == num_MCTS:
                #TODO temp
                #return actions, Blinds, mains_player, cards_boards, btn_loc
                print("Fin partie")
                return game.hand_history, [game.sb_loc, game.bb_loc]
                action_type, total = random_agent(game)
                #cloneTexasHoldem3(game.hand_history, None)
                #return
                #action_type, total = choix_MCTS(20,game, actions, Blinds, mains_player, cards_boards, buyin, big_blind, small_blind, nb_players, num_MCTS, btn_loc)
                #action_type, total = ActionType.FOLD, None
                print(f"MCTS joue : {action_type} {total}")
                #return actions, Blinds, mains_player, cards_boards, btn_loc

                #MCTS joue
            else:
                action_type, total = random_agent(game)

            actions[num_partie][num_action] = (action_type, total, game.current_player)
            
            game.take_action(action_type=action_type, total=total)
            num_action += 1
            
            #mains_player[num_partie] = (game.current_player, game.hands[game.current_player])
            if len(game.board) != 0:
                cards_boards[num_partie] = game.board

            #print("actions : ", actions)
            #print("Blinds : ", Blinds)
            #print("mains_player : ", mains_player)
            #print("cards_boards : ", cards_boards)
            
            gui.display_action()
        gui.display_win()
    
        
        return game.hand_history

    
    

class Node:
    def __init__(self, state : dict):
        #print("State : ", state)
        #Deepcopy à faire manuellement
        self.state = state
        #print("State : ", self.state)
        self.parent = None
        self.children = []
        self.visits = 0
        self.wins = 0

class MCTS:
    def __init__(self, state, num_iterations : int, num_player : int):
        self.num_iterations = num_iterations
        self.num_player = num_player #Pour savoir quel joueur est MCTS
        self.state = state #Dictionnaire avec toutes les actions, blinds, mains, cartes du joueur MCTS, buyin, big blind, small blind, nb_players de chaque partie du tournoi


    def select(self, node):
        while not node.state.is_hand_running():
            if len(node.children) == 0:
                return self.expand(node)
            else:
                node = self.uct_select(node)
        return node

    def expand(self, node):
        possible_actions = node.state.get_available_moves()
        for action in possible_actions:
            new_node = Node(node.state)
            print("Action : ", action)
            new_node.state.take_action(*action)
            #new_node = Node(new_state)
            new_node.parent = node
            node.children.append(new_node)
        return random.choice(node.children)

    def uct_select(self, node):
        selected_node = None
        best_uct = float("-inf")
        total_visits = math.log(node.visits or 1)  # Avoid division by zero

        for child in node.children:
            uct_value = (child.wins / (child.visits or 1)) + 1.4 * math.sqrt(total_visits / (child.visits or 1))
            if uct_value > best_uct:
                selected_node = child
                best_uct = uct_value

        return selected_node

    def simulate(self, node):
        current_state = cloneTexasHoldem(node.state["actions"], node.state["Blinds"], node.state["mains_player"], node.state["cards_boards"])
        print("Current state : ", current_state)
        while current_state.is_hand_running():
            print("hand running")
            action, total = current_state.get_available_moves().sample()
            print("action : ", action, "total : ", total)
            current_state.take_action(action_type=action, total=total)
            print("Current state : ", current_state)
        
        print("Settle : ", current_state.hand_history.settle)

        gagnant = str(current_state.hand_history.settle)[7]
        gagnant = int(gagnant)
        if gagnant == self.num_player:
            return 1
        return -1

    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            if result == 1:
                node.wins += 1
            node = node.parent

    def get_best_action(self, node):
        best_child = None
        best_wins = float("-inf")

        for child in node.children:
            if child.wins > best_wins:
                best_child = child
                best_wins = child.wins

        return best_child.state._action

    def search(self, initial_state, num_player : int):
        root_node = Node(initial_state)
        self.num_player = num_player

        for _ in range(self.num_iterations):
            selected_node = self.select(root_node)
            simulation_result = self.simulate(selected_node)
            self.backpropagate(selected_node, simulation_result)

        return self.get_best_action(root_node)




