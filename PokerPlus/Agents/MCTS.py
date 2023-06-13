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
import time
from PokerPlus.Agents.fonctions_auxiliaires import obtenir_cote,cote_en_pourcentage


def HandPotentiel(ourcards, boardcards):
    oppcards = Deck().draw(num=52)
    ahead = 0
    tied = 1
    behind = 2

    oppcards = [card for card in oppcards if card not in ourcards and card not in boardcards]
    ourrank = evaluate(ourcards, boardcards)
    HP = [[0,0,0],[0,0,0],[0,0,0]]
    HPTotal = [0,0,0]
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
                    #print(ourcards, board)
                ourbest = evaluate(ourcards, board)
                    #print(list(set_), board)
                oppbest = evaluate(list(set_), board)
                if ourbest > oppbest:
                    HP[index][ahead] += 1
                elif ourbest == oppbest:
                    HP[index][tied] += 1
                else:
                    HP[index][behind] += 1
                HPTotal[index] += 1
    Ppot = (HP[behind][ahead] + (HP[behind][tied]/2) + (HP[tied][ahead]/2)) / (HPTotal[behind] + HPTotal[tied])
    Npot = (HP[ahead][behind] + (HP[tied][behind]/2) + (HP[ahead][tied]/2)) / (HPTotal[ahead] + HPTotal[tied])
    return [Ppot, Npot]

def HandStrength(ourcards, boardcards):
    ahead = 0
    tied = 0
    behind = 0
    ourrank = evaluate(ourcards, boardcards)
    oppcards = Deck().draw(num=52)
    oppcards = [card for card in oppcards if card not in ourcards and card not in boardcards]
    for set_ in combinations(oppcards, 2):
        opprank = evaluate(list(set_), boardcards)
        if ourrank > opprank:
            ahead += 1
        elif ourrank == opprank:
            tied += 1
        else:
            behind += 1
    handstrength = (ahead + tied/2) / (ahead + tied + behind)
    return handstrength

def proba_win(game : TexasHoldEm):
    ts = time.time()
    HS = HandStrength(game.hands[game.current_player], game.board)
    print("HS : ", HS)
    HP = HandPotentiel(game.hands[game.current_player], game.board)
    print("HP : ", HP)
    res = time.time() - ts
    print("Time : ", res)
    return HS * (1 - HP[1]) + (1 - HS) * HP[0]
    
def agent_proba(game : TexasHoldEm):
    bet_amount = game.player_bet_amount(game.current_player)
    chips =  game.players[game.current_player].chips
    min_raise =  game.value_to_total(game.min_raise(),game.current_player)
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
        print("p win * 100 : ", p_win*100)
        if p_win*100 > cote_en_pourcentage(obtenir_cote(game)):
            move, total = game.get_available_moves().sample()
            
            print("on sample une action")
            return move, total
    

    return ActionType.FOLD, None


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


