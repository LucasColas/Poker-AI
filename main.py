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
    print("Hello World !")
    choice = 999
    
    while choice != 0:
        print("0 : leave")
        print("1 : simulation")
        print("2 : winners of tournaments")
        print("3 : watch MCTS play")
        choice = int(input("What do you want to do ? "))
        if choice == 0:
            print("Bye !")
            return 
        
        elif choice == 1:
            print("Simulation")
            nmax = int(input("How many simulations ? "))
            buyin = int(input("Buyin ? "))
            big_blind = int(input("Big blind ? "))
            
            nb_players = int(input("How many players ? "))
            poolrandom = input("Pool random ? (Y/N) ")
            if poolrandom == "Y":
                poolrandom = True
            else:
                poolrandom = False

            save = input("Save ? (Y/N) ")
            if save == "Y":
                save = True
            else:
                save = False
            plot = input("Plot ? (Y/N) ")
            if plot == "Y":
                plot = True
            else:
                plot = False
            get_stat_tournoi(nmax=nmax, buyin=buyin, big_blind=big_blind, save=save, path='./res',plot=plot,poolrandom=poolrandom, max_players=nb_players)
        
        elif choice == 2:
            print("Winners of tournaments")
            plot_gagnant_from_csv(filename = "./data_gagnant.csv" )

        elif choice == 3:
            print("MCTS")
            buyin = int(input("Buyin ? "))
            big_blind = int(input("Big blind ? "))
            small_blind = int(input("Small blind ? "))
            nb_players = int(input("How many players ? "))
            num_MCTS = int(input("num of player MCTS ? "))
            MainGame(buyin, big_blind, small_blind, nb_players, num_MCTS)

    end = time.time()
    print(f"Time : {end-start} secondes")
    
    
 
    

if __name__ == "__main__":
    main()
