 #TexasHoldEm
from time import sleep
from texasholdem.game.game import TexasHoldEm
from texasholdem.agents.basic import random_agent, call_agent
from texasholdem.evaluator.evaluator import *
from texasholdem.card.deck import Deck
from texasholdem.gui.text_gui import TextGUI
from texasholdem.game.action_type import ActionType


#PokerPlus
from PokerPlus.Stat.stat import get_stat, get_stat_tournoi
from PokerPlus.Simulation.simu_bots import simu
from PokerPlus.Stat.data import get_data, write_data
from PokerPlus.Simulation.simu_bots_humains import simu_bots_humains, tournoi_avec_humain, plot_gagnant_from_csv
from PokerPlus.Comportement.simu_comportement import simu_comportement, write_data_comportement, write_data_comportement2
from PokerPlus.Agents.MCTS import MainGame
import time

def main():
    start = time.time()
    #tournoi_avec_humain()

    #plot_gagnant_from_csv(filename = "./data_gagnant.csv" )
    
    get_stat_tournoi(nmax = 50, buyin=1000, big_blind=100, save=False, path='./res', plot=True, poolrandom = False, max_players=6, verbose=False)

    
    
    """
    buyin = 1000
    big_blind = 150
    small_blind = 75
    nb_players = 6
    num_MCTS = 3
    
    
    MainGame(buyin, big_blind, small_blind, nb_players, num_MCTS)
    """
    end = time.time()
    print(f"Temps d'execution : {end-start} secondes")
    
    
 
    

if __name__ == "__main__":
    main()
