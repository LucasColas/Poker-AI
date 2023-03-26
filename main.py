
from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent, call_agent
from texasholdem.evaluator.evaluator import *
from texasholdem.card.deck import Deck
from agents.agent import agent_naif

max_players = 6
big_blind = 150
small_blind = big_blind // 2
buyin = 1000
game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
gui = TextGUI(game=game, visible_players=[])
while game.is_game_running():
    game.start_hand()

    while game.is_hand_running():

        gui.set_visible_players([game.current_player])
        gui.run_step()
    gui.display_win()
