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
    
    get_stat_tournoi(nmax=100,poolrandom=False,plot=True)

    #stats_tournoi = get_stat_tournoi(nmax=100,poolrandom=True,plot=True)
    #print(stats_tournoi)
    m = 40
    #stats_dict = get_data(m=m)
    #write_data(m=m,data_dict=stats_dict)
    #simu_bots_humains()
    #print(stats_dict)




if __name__ == "__main__":
    main()
