
"""

Code qui ne devrait plus être utilisée

"""


from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
from PokerPlus.Agents.agents_bots import agent_naif, agent_allIn
from PokerPlus.Agents.agent_outs import agent_outs

def simu_bots_humains():
    max_players = 2
    big_blind = 50
    small_blind = big_blind // 2
    buyin = 1000
    game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
    gui = TextGUI(game=game, visible_players=[])
    Agent = agent_outs()
    while game.is_game_running():
        game.start_hand()

        while game.is_hand_running():
            gui.display_state()
            #print([player. player_id for player in game.players])
            #print("Button", game.btn_loc)
            #print("SB", game.sb_loc)
            #print("BB", game.bb_loc)
            #obtenir_cote(game)

            gui.wait_until_prompted()
            if game.current_player % 2 != 0:
                gui.set_visible_players([game.current_player])

            

            if game.current_player % 2 == 0:
                #Agent.setGame(game)
                game.take_action(*Agent.choix(game))
            else:
                gui.run_step()
                gui.set_visible_players([])

            #game.take_action(*random_agent(game))
            gui.display_action()
            

        #path = game.export_history('./pgns')
        gui.display_win()
