from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI

class FHP:
    """
    
    Simple class to play heads-up flop hold’em poker (FHP).
    
    
    """

    def __init__(self, buyin=1000, small_blind=10, big_blind=20, gui=False):
        self.game = None
        self.nb_players = 2
        self.buyin = buyin
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.gui = gui


    def play(self):
        """
        
        Play a game of FHP.
        
        """
        if not self.game:
            self.game = TexasHoldEm(self.nb_players, self.buyin, self.small_blind, self.big_blind)
            if self.gui:
                

        
        self.game.reset()
        self.game.deal()
        self.game.flop()
        self.game.bet()
        self.game.turn()
        self.game.bet()
        self.game.river()
        self.game.bet()
        self.game.showdown()
        self.game.reset()