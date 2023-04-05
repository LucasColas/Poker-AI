from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
from agents import agent_naif, agent_allIn
from agent_outs import agent_outs
max_players = 2
big_blind = 150
small_blind = big_blind // 2
buyin = 1000
game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
gui = TextGUI(game=game)
Agent = agent_outs()
while game.is_game_running():
    game.start_hand()

    while game.is_hand_running():
        gui.display_state()
        #obtenir_cote(game)

        gui.wait_until_prompted()

        if game.current_player % 2 == 0:
            Agent.setGame(game)
            game.take_action(*Agent.choix())
        else:
            game.take_action(*random_agent(game))
        gui.display_action()
        #gui.set_visible_players([game.current_player])

    #path = game.export_history('./pgns')
    gui.display_win()
