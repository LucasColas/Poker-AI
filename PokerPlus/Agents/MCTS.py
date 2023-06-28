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
    
    #print(f"\nhands 1: {game.hands}")

    # On remet les mains des joueurs dans la pioche 
    for p in game.players:
        if p.player_id != num_MCTS and p.player_id in game.hands.keys():
            
            game._deck.cards.extend(game.hands[p.player_id])
            game.hands[p.player_id] = []
    #on melange
    game._deck.shuffle()

    # On pioche 2 carte pour tout le monde sauf MCTS
    for p in game.players:
        if p.player_id != num_MCTS and p.player_id in game.hands.keys():
            if len(game.hands[p.player_id]) != 0:
                print("erreur")
                game.hands[p.player_id] = []
            
            game.hands[p.player_id] = game._deck.draw(2)

            #print("game hands : ", game.hands[p.player_id])

    #print(f"\nhands 2: {game.hands}")
    
    while game.is_game_running():

        
        while game.is_hand_running():
            if gui:
                gui.display_state()
                gui.wait_until_prompted()
                
            if ok and game.current_player == num_MCTS:
                action_type, total = next_action
                ok = False
                #if action_type == ActionType.RAISE:
                    #print(f"on joue l'action choisi pour cett simu {next_action}")

            else:
                action_type, total = random_agent(game)
                #print(f"{game.current_player} joue l'action random {action_type, total}")

            game.take_action(action_type=action_type, total=total)
            if gui:
                gui.display_action()

        if gui:
            gui.display_win()

        
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
    #on recupere le min raise en triant le tableau available_move par rapport a son 2 argument pour chaque tuple
    
    available_moves_raise = sorted(available_moves_raise, key=lambda x: x[1])
    #print(f"available_moves_raise : {available_moves_raise}")


    if len(available_moves_raise) > 10:
        
        min = available_moves_raise[0][1]
        max = available_moves_raise[-1][1]
        # on divise nos raises possibles en 10 et on prend le raise 1*h, 2*h, 3*h, 4*h, 5*h, 6*h, 7*h, 8*h, 9*h, 10*h
        h = (max-min)//game.big_blind
        #print(f"min : {min}, max : {max}, h : {h}, big_blind : {game.big_blind}")
        action_ok += [(ActionType.RAISE, min)]
        action_ok += [(ActionType.RAISE, max)]
        for i in range(1,h):
            action_ok += [(ActionType.RAISE, min + i*game.big_blind)]
            #print(f"action_ok : {action_ok}") 
        
    elif len(available_moves_raise) > 0:
        action_ok += random.sample(available_moves_raise, 1)
    #print(f"\n\ntaille action_ok : {len(action_ok)}")
    action_ok +=[a for a in available_moves if a[0] != ActionType.RAISE]

    for i in range(nbr_de_simu_par_action):
        for action in action_ok:
            #print(f"        simu : {i} |action : {action[0]}, total : {action[1]}")
            if action not in score.keys():
                score[action] = [simulation(deepcopy(game), num_MCTS, action, gui=False) ]
            else:
                score[action].append(simulation(deepcopy(game), num_MCTS, action, gui=False))

    #print(f"score : {score}")
    dico_moy = {}
    for action in score.keys():
        dico_moy[action] = sum(score[action])/len(score[action])
    #print(f"dico_moy : {dico_moy}")

    #on prend le max
    max = 0
    for action in dico_moy.keys():
        if dico_moy[action] > max:
            max = dico_moy[action]
            action_max = action
    return action_max


def MainGame(buyin,big_blind, small_blind, nb_players, num_MCTS, num_iterations = 50, nbr_de_simu_par_action = 50):
    game = TexasHoldEm(buyin, big_blind, small_blind, nb_players)
    gui = TextGUI(game=game)
    mctss = MCTS(deepcopy(game), num_iterations, nbr_de_simu_par_action, num_MCTS)
    while game.is_game_running():
        game.start_hand()


        while game.is_hand_running():
            gui.display_state()
            gui.wait_until_prompted()
            if game.current_player == num_MCTS:
                action = mctss.search(deepcopy(game),num_MCTS)
                print(f"action de MCTS: {action}")
                if type(action) == tuple:
                    action_type, total = action
                if type(action) == list:
                    action_type, total = action.pop(0)
                

                #Test de 1 simulation
                #action_type, total = choix_MCTS(nbr_de_simu_par_action,deepcopy(game), num_MCTS)
                #print(f"action_type : {action_type}") 
            else:
                action_type, total = random_agent(game)


            
            game.take_action(action_type=action_type, total=total)
            
            
            gui.display_action()
        gui.display_win()


    

class Node:
    def __init__(self, state : TexasHoldEm):
        #print("State : ", state)
        #Deepcopy à faire manuellement
        self.state = deepcopy(state)
        #print("State : ", self.state)
        self.parent = None
        self.children = []
        self.visits = 0
        self.wins = 0
        self.games_played = 0
        self.action = None

class MCTS:
    def __init__(self, state : TexasHoldEm, num_iterations : int, nb_simu : int, num_player : int):
        self.num_iterations = num_iterations
        self.num_player = num_player #Pour savoir quel joueur est MCTS
        self.state = state # Game
        self.root_node = Node(state)
        self.nb_simu = nb_simu

    def select(self, node):
        """
            Phase 1 : Selection
            TODO : prendre en compte qu'on peut atteindre une feuille avec état terminal (main terminée).
            Cela ne sert à rien de prendre ce noeud ni d'essayer d'ajouter des enfants.
        """
        while node:
            if len(node.children) == 0:
                
                return self.expand(node)
            else:
                new_node = self.uct_select(node)
                if not new_node:
                    return node
                node = new_node
                
        
        return node

    def expand(self, node):
        """
            Phase 2 : Expansion
        """
        
        #print("actions : ")
        actions = node.state.get_available_moves()
        #print("actions : ",actions)

        #print("EXPAND:")
        #print("     actions : ", actions)
        
        raises = [a for a in actions if a[0] == ActionType.RAISE and a[1] !=None]
                
        #print("     raises : ", raises)
        
        possible_actions = [a for a in actions if a[0] != ActionType.RAISE]
        if len(raises) > 10:
            raises.sort(key=lambda x: x[1])
            possible_actions += raises[0:10]
            #print("     possible_actions : ", possible_actions)
            
            for action in possible_actions:
                new_node = Node(node.state)
                
                #print (f" enfants : {node.children}")
                #print("     Action : ", action)
                new_node.action = action
                #print("state : ", new_node.state.hand_phase)
                new_node.state.take_action(*action)
                #new_node = Node(new_state)
                node.children.append(new_node)
                new_node.parent = node
        else:
            possible_actions += raises
            #print("     possible_actions : ", possible_actions)
            for action in possible_actions:
                new_node = Node(node.state)
                
                #print (f" enfants : {node.children}")
                #print("     Action : ", action)
                new_node.action = action
                #print("state : ", new_node.state.hand_phase)
                new_node.state.take_action(*action)
                #new_node = Node(new_state)

                node.children.append(new_node)
                new_node.parent = node
        return random.choice(node.children)

    def uct_select(self, node):
        selected_node = None
        best_uct = float("-inf")
        total_visits = math.log(node.visits or 1) 
        c = math.sqrt(2)

        for child in node.children:
            uct_value = (child.wins / (child.visits or 1)) + c * math.sqrt(total_visits / (child.visits or 1))
            #print("hand running in this child : ", child.state.is_hand_running())
            if uct_value > best_uct and child.state.is_hand_running():
                selected_node = child
                best_uct = uct_value

        return selected_node

    def simulate(self, node):
        """
            Phase 3 : Simulation
        """
        current_state = deepcopy(node.state)
        #TODO : changer les cartes des joueurs
        #print("SIMULATE : ")
        while current_state.is_hand_running():
            #print("     hand running")
            action, total = current_state.get_available_moves().sample()
            #print("     action : ", action, "total : ", total)
            current_state.take_action(action_type=action, total=total)
            #print("     Current state : ", current_state)
        
        #print("     Settle : ", current_state.hand_history.settle)

        if current_state.hand_history == None:
            return 0
        gagnant = str(current_state.hand_history.settle)[7]
        gagnant = int(gagnant)
        if gagnant == self.num_player:
            return 1
        return -1

    def backpropagate(self, node : Node, result):
        """
            Phase 4 : Backpropagation
        """
        
        if not node:
            return
        
        if node.parent is None:
            node.visits += 1
            node.wins += 1 if result == 1 else 0
            
            return
        
        node.visits += 1
        node.wins += 1 if result == 1 else 0
        self.backpropagate(node.parent, result)

    def get_best_action(self, node):
        best_child = None
        best_wins = float("-inf")

        for child in node.children:
            if child.wins > best_wins:
                best_child = child
                best_wins = child.wins
        return best_child.action
    
    def PrintTree(self, node):
        """
            Depth First Search
        """
        if node:
            print("info node : " ,"node visits : ", node.visits," node wins : " ,node.wins, node.action)
            for child in node.children:
                self.PrintTree(child)

    def search(self, new_state, num_player : int):
        """
        
            search
        
        """
        self.root_node = Node(new_state)
        self.num_player = num_player

        for i in range(self.num_iterations):
            #print("Iteration : ", i)
            #print("Root node : ", self.root_node.state.get_available_moves())
            selected_node = self.select(self.root_node)
            #print("Selected node : ", selected_node)
            #for action_child in self.root_node.children:
                #print("Action child : ", action_child.action)
            for i in range(self.nb_simu):
                #print("Simulation : ", i)
                simulation_result = self.simulate(selected_node)
                #print("Simulation result : ", simulation_result)
                self.backpropagate(selected_node, simulation_result)
                #print("Backpropagate : ", selected_node)

        #on affiche toutes les infos du noeud root
        #print(f"root_node : {self.num_iterations} {self.root_node.children}, {self.root_node.visits}, {self.root_node.wins} ")
        #self.PrintTree(self.root_node)
        return self.get_best_action(self.root_node)




