#TexasHoldEm
from texasholdem.game.game import TexasHoldEm
from texasholdem.agents.basic import random_agent, call_agent
from texasholdem.evaluator.evaluator import *
from texasholdem.card.deck import Deck
from texasholdem.gui.text_gui import TextGUI


#PokerPlus
from PokerPlus.Stat.stat import get_stat
from PokerPlus.Simulation.simu_bots import simu
from PokerPlus.Simulation.simu_bots2 import simu2




def main():
    get_stat()
    #simu()

if __name__ == "__main__":
    main()
