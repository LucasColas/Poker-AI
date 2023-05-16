

from PokerPlus.Agents.agents_bots import *
from texasholdem.game.game import TexasHoldEm
from PokerPlus.Agents.agent_outs import agent_outs
from PokerPlus.Agents.Good_Agents import agent_SA
from texasholdem.agents.basic import random_agent
from PokerPlus.Comportement.comportement import getVpip, getRatioLarge

import csv

def simu_comportement(nb_tournoi : int = 50, max_players : int = 8, big_blind : int = 150, small_blind : int = 150 // 2, buyin : int = 1000, 
         bots = [random_agent,agent_outs().choix,agent_SA().action, agent_naif, agent_allIn, agent_saboteur, agent_serre_non_agressif, agent_large_non_agressif], 
         bots_noms = ["random_agent","agent_out", "agent_serre_agressif", "agent_naif", "agent_allIn", "agent_saboteur", "agent_serre_non_agressif", "agent_large_non_agressif"],
         cles = ["nbrCall", "nbrCheck", "nbrRaise", "nbrFold", "nbrAction"]):
    stats = {key:{} for key in cles}
    for key in stats:
        stats[key] = {(i,bots_noms[i]):0 for i in range(max_players)}
    
    for n in range(nb_tournoi):
        game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
        game.start_hand()
        
        while game.is_hand_running():
            # Utiliser le bot sélectionné pour le joueur actuel
            current_bot = bots[game.current_player]
            
            action, total = current_bot(game)
            
            #print(f"Player {game.current_player} {action} {total}")
            if len(game.board) == 0:
                i = game.current_player
                if (action == ActionType.CALL):
                    stats["nbrCall"][(i, bots_noms[i])]+=1
                elif (action == ActionType.CHECK):
                    stats["nbrCheck"][(i, bots_noms[i])]+=1
                elif (action == ActionType.RAISE):
                    stats["nbrRaise"][(i, bots_noms[i])]+=1
                elif (action==ActionType.ALL_IN):
                    stats["nbrRaise"][(i, bots_noms[i])]+=1
                elif (action == ActionType.FOLD):
                    stats["nbrFold"][(i, bots_noms[i])]+=1
                stats["nbrAction"][(i, bots_noms[i])]+=1
            #print(bots[game.current_player])
            game.take_action(action, total=total)

    return stats
            
def write_data_comportement(data_dict: dict, max_players=8, filename: str = "data_comportement.csv", path: str = "", bots_noms = ["random_agent","agent_out", "agent_serre_agressif", "agent_naif", "agent_allIn", "agent_saboteur", "agent_serre_non_agressif", "agent_large_non_agressif"]):
    max_players = max_players
    simu = 0
    nb_tournoi = 0
    #simu_print = f"simu : {simu}"
    fieldnames = ['vpip', 'ratio action', 'bot']
    with open(path+filename, 'w') as csvfile:
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(max_players):

            #print("Call : ",data_dict["nbrCall"][(i, bots_noms[i])])
            #print("Raise : ",data_dict["nbrRaise"][(i, bots_noms[i])])
            #print("Action : ",data_dict["nbrAction"][(i, bots_noms[i])])
            vpip = getVpip(data_dict["nbrCall"][(i, bots_noms[i])], data_dict["nbrRaise"][(i, bots_noms[i])], data_dict["nbrFold"][(i, bots_noms[i])], data_dict["nbrAction"][(i, bots_noms[i])])
            ratio_large = getRatioLarge(data_dict["nbrFold"][(i, bots_noms[i])], data_dict["nbrAction"][(i, bots_noms[i])])
            writer.writerow({fieldnames[0]: vpip, fieldnames[1]: ratio_large, fieldnames[2]: bots_noms[i]})

def write_data_comportement2(data_dict: dict, nb_tournoi:int, filename: str = "data_comportement.csv", path: str = "", bots_noms = ["random_agent","agent_out", "agent_serre_agressif", "agent_naif", "agent_allIn", "agent_saboteur", "agent_serre_non_agressif", "agent_large_non_agressif"]):
    max_players = len(data_dict["nbrWin tournoi"])
    print("\n\n",max_players,"\n\n")


    vpip = {i:[] for i in range(max_players)}
    ratio_large = {i:[] for i in range(max_players)}


    for i in range(nb_tournoi):
        nb_r = {j:data_dict["nbrRaise"][f"tournoi {i}"][j] for j in range(max_players)}
        print(nb_r)
        nb_c = {j:data_dict["nbrCall"][f"tournoi {i}"][j] for j in range(max_players)}
        nb_f = {j:data_dict["nbrFold"][f"tournoi {i}"][j] for j in range(max_players)}
        nb_a = {j:data_dict["nbrAction"][f"tournoi {i}"][j] for j in range(max_players)}
        for j in range(max_players):
            vpip[j].append(getVpip(nb_c[j], nb_r[j], nb_f[j], nb_a[j]))
            ratio_large[j].append(getRatioLarge(nb_f[j], nb_a[j]))
       
    fieldnames = ['vpip', 'ratio action', 'bot']
    with open(path+filename, 'w') as csvfile:
       
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(max_players):
            for k in range(nb_tournoi):
                writer.writerow({fieldnames[0]: vpip[i][k], fieldnames[1]: ratio_large[i][k], fieldnames[2]: bots_noms[i]})    