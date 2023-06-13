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
from PokerPlus.Simulation.simu_bots_humains import simu_bots_humains, tournoi_avec_humain, plot_gagnant_from_csv
from PokerPlus.Comportement.simu_comportement import simu_comportement, write_data_comportement, write_data_comportement2
from PokerPlus.Agents.MCTS import MainGame

def main():
    
    #tournoi_avec_humain()
    plot_gagnant_from_csv(filename = "./data_gagnant.csv" )
    """
    buyin = 1000
    big_blind = 150
    small_blind = 75
    nb_players = 6
    num_MCTS = 3
    actions, Blinds, mains_player, cards_boards = MainGame(buyin, big_blind, small_blind, nb_players, num_MCTS)
    print()
    print()

    print()
    print()
    print()
    print()

    print("actions : ", actions)
    print("Blinds : ", Blinds)
    print("mains players : ", mains_player)
    print("Cards boards : ", cards_boards)
    simu(actions, Blinds, mains_player, cards_boards, buyin,big_blind, small_blind, nb_players, num_MCTS)
    
    """



if __name__ == "__main__":
    main()
