# TexasHoldEm
from time import sleep
from copy import deepcopy


from texasholdem.agents.basic import random_agent, call_agent
from texasholdem.evaluator.evaluator import *
from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI


# PokerPlus
from PokerPlus.Stat.stat import get_stat_tournoi
from PokerPlus.Simulation.simu_bots_humains import (
    plot_gagnant_from_csv,
    tournoi_avec_humain,
)
from PokerPlus.Agents.MCTS import MainGame
from PokerPlus.Stat.odds_calculator import odds_calculator
from PokerPlus.DeepCFR.deep_cfr import deep_cfr, save_deep_cfr
from Variants.NLHP.nlhp import NLHP
import time


def main():
    nb_players = 2
    nb_iterations = 1000
    nb_game_tree_traversals = 100
    n_actions, n_card_types, n_bets = 3, 4, 2

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
        print("7 : Train Deep CFR")
        print("8 : Play against Deep CFR in Heads-up hold’em poker")
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
            game = TexasHoldEm(buyin=1500, big_blind=80, small_blind=40, max_players=2)
            gui = TextGUI(game=game)
            while game.is_game_running():
                game.start_hand()

                while game.is_hand_running():
                    gui.run_step()

        elif choice == 7:
            # Train Deep CFR
            game = TexasHoldEm(buyin=1500, big_blind=80, small_blind=40, max_players=2)
            game.start_hand()
            save_deep_cfr(
                path="",
                name_file="DeepCFR",
                nb_iterations=nb_iterations,
                nb_players=nb_players,
                nb_game_tree_traversals=nb_game_tree_traversals,
                game=deepcopy(game),
                n_actions=n_actions,
                n_card_types=n_card_types,
                n_bets=n_bets,
            )

        elif choice == 8:
            # heads-up hold’em poker with Deep CFR
            pass

    end = time.time()
    print(f"Time : {end-start} secondes")


if __name__ == "__main__":
    main()
