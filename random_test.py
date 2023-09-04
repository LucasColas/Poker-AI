from texasholdem.game.game import TexasHoldEm

from texasholdem.gui.text_gui import TextGUI

game = TexasHoldEm(buyin=500, big_blind=5, small_blind=2, max_players=6)
gui = TextGUI(game=game)

while game.is_game_running():
    game.start_hand()

    while game.is_hand_running():
        print("game available_moves : ", game.get_available_moves())
        print("game available moves slicing : ", game.get_available_moves()[:5])
        for move in game.get_available_moves():
            print("move : ", move)

        gui.run_step()
