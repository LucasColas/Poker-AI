from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
from agents import agent_naif, agent_Sacha
from agent_outs import agent_outs
from fonctions_auxiliaires import obtenir_cote

max_players = 6
big_blind = 150
small_blind = big_blind // 2
buyin = 1000
game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
gui = TextGUI(game=game)
agent_outs = agent_outs()
while game.is_game_running():
    game.start_hand()

    while game.is_hand_running():
        agent_outs.setGame(game)
        gui.display_state()
        #obtenir_cote(game)

        gui.wait_until_prompted()
        if game.current_player == 0:
            game.take_action(*agent_outs.choix())
        if game.current_player % 2 == 0 and game.current_player != 0:
            game.take_action(*agent_naif(game))
        else:
            game.take_action(*agent_Sacha(game,seuil = 0.2))
        gui.display_action()
        #gui.set_visible_players([game.current_player])

    path = game.export_history('./pgns')
    gui.display_win()
