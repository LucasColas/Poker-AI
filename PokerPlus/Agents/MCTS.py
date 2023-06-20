import random
import time
import math
from copy import deepcopy, copy
from texasholdem.game.game import TexasHoldEm, Pot
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




def simulation(game : TexasHoldEm, num_MCTS : int, next_action : any, gui=False) -> float:
    if gui:
        gui = TextGUI(game=game)
    ok = True
    #TODO MARCHE PAS
    """
    print(f"\nhands 1: {game.hands}")

    # On remet les mains des joueurs dans la pioche 
    for p in game.players:
        if p.player_id != num_MCTS:
            
            game._deck.cards.append(game.hands[p.player_id])
            game.hands[p.player_id] = []
    #on melange
    game._deck.shuffle()

    # On pioche 2 carte pour tt le monde sauf MCTS
    for p in game.players:
        if p.player_id != num_MCTS:
            game.hands[p.player_id] += game._deck.draw(2)

    print(f"\nhands 2: {game.hands}")
    """
    while game.is_game_running():

        
        while game.is_hand_running():
            if gui:
                gui.display_state()
                gui.wait_until_prompted()
                
            if ok and game.current_player == num_MCTS:
                action_type, total = next_action
                ok = False
                if action_type == ActionType.RAISE:
                    print(f"on joue l'action choisi pour cett simu {next_action}")

            else:
                action_type, total = random_agent(game)
                #print(f"{game.current_player} joue l'action random {action_type, total}")

            game.take_action(action_type=action_type, total=total)
            if gui:
                gui.display_action()

        if gui:
            gui.display_win()

        #TODO : renvoyer les chips qu'a gagné le joueur en sachant que s'il gagne les 
        #jetons ne sont pas encore dans sa poche, donc il faut regarder dans le pot
        #et pas que que l'attribut chips.
        for p in game.players:
            if p.player_id == num_MCTS:
                #print(f"chips : {p.chips}")
                return p.chips

        

def choix_MCTS(nbr_de_simu_par_action,game, num_MCTS):

    score = {}
    available_moves = game.get_available_moves()
    action_ok = []
     # je veux choisir 10 actions au hasard parmi les actions possible qui raise:
    available_moves_raise = [a for a in available_moves if a[0] == ActionType.RAISE and a[1] !=None]
    if len(available_moves_raise) > 10:
        # jen prend 10 au hasard
        action_ok  += random.sample(available_moves_raise, 10)
    elif len(available_moves_raise) > 0:
        action_ok += random.sample(available_moves_raise, 1)
    print(f"\n\ntaille action_ok : {len(action_ok)}")
    action_ok +=[a for a in available_moves if a[0] != ActionType.RAISE]

    for i in range(nbr_de_simu_par_action):
        for action in action_ok:
            print(f"        simu : {i} |action : {action[0]}, total : {action[1]}")
            if action not in score.keys():
                score[action] = [simulation(deepcopy(game), num_MCTS, action, gui=False) ]
            else:
                score[action].append(simulation(deepcopy(game), num_MCTS, action, gui=False))

    #print(f"score : {score}")
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


def MainGame(buyin,big_blind, small_blind, nb_players, num_MCTS, nbr_de_simu_par_action = 1000):
    game = TexasHoldEm(buyin, big_blind, small_blind, nb_players)
    gui = TextGUI(game=game)
    
    
    while game.is_game_running():
        game.start_hand()


        while game.is_hand_running():
            gui.display_state()
            gui.wait_until_prompted()
            if game.current_player == num_MCTS:
                #Test de 1 simulation
                action_type, total = choix_MCTS(nbr_de_simu_par_action,deepcopy(game), num_MCTS)
                print(f"action_type : {action_type}") 
            else:
                action_type, total = random_agent(game)


            
            game.take_action(action_type=action_type, total=total)
            
            
            gui.display_action()
        gui.display_win()


    

class Node:
    def __init__(self, state : dict):
        #print("State : ", state)
        #Deepcopy à faire manuellement
        self.state = deepcopy(state)
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




