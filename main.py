# TexasHoldEm
from time import sleep
from texasholdem.agents.basic import random_agent, call_agent
from texasholdem.evaluator.evaluator import *


# PokerPlus
from PokerPlus.Stat.stat import get_stat_tournoi
from PokerPlus.Simulation.simu_bots_humains import (
    plot_gagnant_from_csv,
    tournoi_avec_humain,
)
from PokerPlus.Agents.MCTS import MainGame
from PokerPlus.Stat.odds_calculator import odds_calculator

from Variants.NLHP.nlhp import NLHP
import time


def main():
    Odds_calculator = odds_calculator()
    start = time.time()

    print("Hello World !")
    choice = 999

    while choice != 0:
        print("0 : leave")
        print("1 : simulation")
        print("2 : winners of tournaments")
        print("3 : watch MCTS play")
        print("4 : odds calculator")
        print("5 : tournament with agents")
        print("6 : heads-up hold’em poker")
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
            get_stat_tournoi(
                nmax=nmax,
                buyin=buyin,
                big_blind=big_blind,
                save=save,
                path="./res",
                plot=plot,
                poolrandom=poolrandom,
                max_players=nb_players,
            )

        elif choice == 2:
            print("Winners of tournaments")
            plot_gagnant_from_csv(filename="./data_gagnant.csv")

        elif choice == 3:
            print("MCTS")
            buyin = int(input("Buyin ? "))
            big_blind = int(input("Big blind ? "))
            small_blind = int(input("Small blind ? "))
            nb_players = int(input("How many players ? "))
            num_MCTS = int(input("num of player MCTS ? "))
            MainGame(buyin, big_blind, small_blind, nb_players, num_MCTS)

        elif choice == 4:
            print("Odds calculator")
            Odds_calculator.main_print()

        elif choice == 5:
            tournoi_avec_humain()

        elif choice == 6:
            new_nlhp = NLHP(buyin=1000, small_blind=10, big_blind=20, gui=False)
            new_nlhp.create_game()
            new_nlhp.play()

    end = time.time()
    print(f"Time : {end-start} secondes")


if __name__ == "__main__":
    main()
