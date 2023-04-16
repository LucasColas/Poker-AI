from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
from PokerPlus.Agents.agents_bots import *
from PokerPlus.Agents.agent_outs import agent_outs

def simu(max_players = 6, big_blind = 150, small_blind = 150 // 2, buyin = 1000, agents = [random_agent, agent_outs().choix, agent_naif, agent_naif, agent_allIn, agent_saboteur], seuils=[0.7], save=False, path='./res'):
    if len(agents) != max_players:
        raise Exception("Nombre d'agents invalide !")

    if agents.count(agent_allIn) != len(seuils):
        raise Exception("Nombre de seuils invalide !")

    if agents.count(agent_allIn) > 0:
        mapping = {}
        cmpt = 0
        for id, val in enumerate(agents):
            if val == agent_allIn:
                mapping[id] = cmpt
                cmpt += 1


    game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
    gui = TextGUI(game=game)

    while game.is_game_running():
        game.start_hand()

        while game.is_hand_running():
            gui.display_state()
            gui.wait_until_prompted()

            #game.take_action(*agents[game.current_player](game))
            #if game.current_player in [0,1,2,3,4]:
                #game.take_action(*random_agent(game))

            current_bot = agents[game.current_player]
            if(current_bot==agent_allIn):
                idx = agents.index(current_bot)
                action, total = current_bot(game,seuils[mapping[game.current_player]])
            else:

                action, total = current_bot(game)
                #print(f"Player {game.current_player} {action} {total}")

                # Met à jour les statistiques

            game.take_action(action, total=total)
            #gui.run_step()

        if save:
            path = game.export_history('./res')

        gui.display_win()
