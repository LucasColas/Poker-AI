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
from PokerPlus.Comportement.simu_comportement import simu_comportement, write_data_comportement, write_data_comportement2


def main():
    m = 100
    write_data(m=m, max_players=6, filename="data.csv", path="")
    #get_stat_tournoi(nmax=20, poolrandom=True, max_players=6, verbose=True, plot=True)

    #simu_bots_humains()
    




if __name__ == "__main__":
    main()
