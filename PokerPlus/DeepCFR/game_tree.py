from texasholdem.game.game import TexasHoldEm
from copy import deepcopy

class Node:
    """

        Node for GameTree.
    
    """

    def __init__(self, state : TexasHoldEm) -> None:
        self.state = deepcopy(state)
        self.parent = None
        self.children = {}

class GameTree():
    """
    
        GameTree for Head's up Texas Hold'em No Limit.
        This game tree is used to compute the Nash equilibrium with Deep CFR.
        We have a traversal function to collect data for the CFR algorithm.
    
    """

    def __init__(self, state : TexasHoldEm) -> None:
        self.root = Node(state)

    def add_node(self, action : int, state : TexasHoldEm) -> None:
        """
        
            Add a node to the tree.
        
        """
        pass



