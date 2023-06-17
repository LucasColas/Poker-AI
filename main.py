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
from PokerPlus.Agents.MCTS import MainGame, MainGame2, generate_game

def main():
    
    #tournoi_avec_humain()
    #plot_gagnant_from_csv(filename = "./data_gagnant.csv" )
    
    buyin = 1000
    big_blind = 150
    small_blind = 75
    nb_players = 6
    num_MCTS = 3
    #actions, Blinds, mains_player, cards_boards, btn_loc = MainGame2(buyin, big_blind, small_blind, nb_players, num_MCTS,1)
    hand_history, Blinds = MainGame2(buyin, big_blind, small_blind, nb_players, num_MCTS,1)
    print(hand_history)
    #generate_game(hand_history, Blinds, gui=True)
    
    """
    game = TexasHoldEm(buyin=500, big_blind=5, small_blind=2, max_players=6)
    gui = TextGUI(game=game)

    while game.is_game_running():
        game.start_hand()

        while game.is_hand_running():
            gui.run_step()

        path = game.export_history('./pgns')     # save history
        gui.replay_history(path)   
    """


if __name__ == "__main__":
    main()
