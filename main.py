from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI

game = TexasHoldEm(buyin=500, big_blind=5, small_blind=2, max_players=6)
gui = TextGUI(game=game)

while game.is_game_running():
    game.start_hand()

    while game.is_hand_running():
        gui.run_step()

    path = game.export_history('./pgns')     # save history
    gui.replay_history(path)                 # replay history
