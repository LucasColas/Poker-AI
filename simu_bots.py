from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
from agent import agent_naif

max_players = 6
big_blind = 150
small_blind = big_blind // 2
buyin = 1000
game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
gui = TextGUI(game=game, visible_players=[])

while game.is_game_running():
    game.start_hand()

    while game.is_hand_running():
        gui.display_state()
        
        gui.wait_until_prompted()
        gui.set_visible_players([game.current_player])
        game.take_action(*agent_naif(game))
        gui.display_action()

    gui.display_win()
