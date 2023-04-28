#TexasHoldEm
from texasholdem.game.game import TexasHoldEm
from texasholdem.agents.basic import random_agent, call_agent
from texasholdem.evaluator.evaluator import *
from texasholdem.card.deck import Deck
from texasholdem.gui.text_gui import TextGUI


#PokerPlus
from PokerPlus.Stat.stat import get_stat, get_stat_tournoi
from PokerPlus.Simulation.simu_bots import simu
from PokerPlus.Stat.data import get_data, write_data
from PokerPlus.Simulation.simu_bots_humains import simu_bots_humains


def main():
    #get_stat(plot=True)
    #stats_dict = get_data(m=500)
    #get_stat_tournoi(nmax=500,poolrandom=True,plot=True)

    stats_tournoi = get_stat_tournoi(nmax=5,poolrandom=True,plot=True)

    #write_data(stats_dict)
    #simu_bots_humains()
    #print(stats_dict)




if __name__ == "__main__":
    main()
