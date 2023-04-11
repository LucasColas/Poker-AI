from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
from agents import agent_naif, agent_allIn
from agent_outs import agent_outs
from fonctions_auxiliaires import obtenir_cote

max_players = 6
big_blind = 150
small_blind = big_blind // 2
buyin = 1000
game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
gui = TextGUI(game=game)

while game.is_game_running():
    game.start_hand()

    while game.is_hand_running():
        print(f"Player : {game.current_player} : {game._action}")
        if game.current_player in [0,1,2,3,4]:
            game.take_action(*random_agent(game))
        gui.run_step()
        
    gui.display_win()
