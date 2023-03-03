from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
max_players = 6
big_blind = 150
small_blind = big_blind // 2
game = TexasHoldEm(buyin=500, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
gui = TextGUI(game=game)

while game.is_game_running():
    game.start_hand()

    while game.is_hand_running():
        if game.current_player % 2 == 0:
            game.take_action(*random_agent(game))

        gui.run_step()
