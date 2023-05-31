import random
import time
import math
from copy import deepcopy, copy
from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.agents.basic import random_agent
from texasholdem.evaluator.evaluator import *
from texasholdem.card.deck import Deck
from itertools import combinations 
import time
"""

HandPotential(ourcards, boardcards) {
    // Hand potential array, each index represents ahead, tied, and behind
    integer array HP[3][3] // initialize to 0
    integer array HPTotal[3] // initialize to 0
    ourrank = Rank(ourcards, boardcards)

    // Consider all two card combinations of the remaining cards for the opponent
    for each case(oppcards) {
        opprank = Rank(oppcards, boardcards)
        if (ourrank > opprank) index = ahead
        else if (ourrank == opprank) index = tied
        else index = behind
        HPTotal[index] += 1

        // All possible board cards to come
        for each case(turn, river) {
            // Final 5-card board
            board = [boardcards, turn, river]
            ourbest = Rank(ourcards, board)
            oppbest = Rank(oppcards, board)
            if (ourbest > oppbest) HP[index][ahead] += 1
            else if (ourbest == oppbest) HP[index][tied] += 1
            else HP[index][behind] += 1
        }
    }

    // Ppot: were behind but moved ahead
    Ppot = (HP[behind][ahead] + HP[behind][tied] / 2 + HP[tied][ahead] / 2) / (HPTotal[behind] + HPTotal[tied])
    // Npot: were ahead but fell behind
    Npot = (HP[ahead][behind] + HP[tied][behind] / 2 + HP[ahead][tied] / 2) / (HPTotal[ahead] + HPTotal[tied])

    return [ Ppot, Npot ]
}
HandStrength(ourcards, boardcards) {
    ahead = tied = behind = 0
    ourrank = Rank(ourcards, boardcards)

    for each case(oppcards) {
        opprank = Rank(oppcards, boardcards)
        if (ourrank > opprank) ahead += 1
        else if (ourrank == opprank) tied += 1
        else behind += 1
    }

    handstrength = (ahead + tied / 2) / (ahead + tied + behind)

    return handstrength
}
"""

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
    if len(game.board) == 0:
        return random_agent(game)
    
    elif len(game.board) != 0:
        p_win = proba_win(game)
        print("p_win : ", p_win)
        if p_win > 0.5:
            available_moves = game.get_available_moves()
            
            return game.get_available_moves().sample()
    

    return ActionType.FOLD, None


def simu(g : TexasHoldEm, num_player : int):
    
    while g.is_hand_running():
        print("hand running")
        action_type, total = random_agent(g)
        g.take_action(action_type=action_type, total=total)

class Node:
    def __init__(self, state : TexasHoldEm):
        #print("State : ", state)
        #Deepcopy à faire manuellement
        self.state = copy(state)
        #print("State : ", self.state)
        self.parent = None
        self.children = []
        self.visits = 0
        self.wins = 0

class MCTS:
    def __init__(self, num_iterations : int, num_player : int):
        self.num_iterations = num_iterations
        self.num_player = num_player #Pour savoir quel joueur est MCTS


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
        current_state = copy_game(node.state)
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


