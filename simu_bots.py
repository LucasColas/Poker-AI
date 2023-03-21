from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
from agent import agent_naif

game = TexasHoldEm(buyin=500, big_blind=5, small_blind=2, max_players=6)
gui = TextGUI(game=game)

while game.is_game_running():
    game.start_hand()

    while game.is_hand_running():
        gui.display_state()
        gui.wait_until_prompted()

        game.take_action(*agent_naif(game))
        gui.display_action()

    gui.display_win()
