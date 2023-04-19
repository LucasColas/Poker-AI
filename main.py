#TexasHoldEm
from texasholdem.game.game import TexasHoldEm
from texasholdem.agents.basic import random_agent, call_agent
from texasholdem.evaluator.evaluator import *
from texasholdem.card.deck import Deck
from texasholdem.gui.text_gui import TextGUI


#PokerPlus
from PokerPlus.Stat.stat import get_stat
from PokerPlus.Stat.data import get_data
from PokerPlus.Simulation.simu_bots import simu
from PokerPlus.Stat.data import get_data, write_data
from PokerPlus.Simulation.simu_bots_humains import simu_bots_humains


def main():
    #get_stat(plot=True)
    #stats_dict = get_data(m=500)
    #write_data(stats_dict)
    #simu_bots_humains()
    #print(stats_dict)




if __name__ == "__main__":
    main()
