
from texasholdem.game.game import TexasHoldEm, Pot
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.agents.basic import random_agent
#from agents import agent_naif,agent_alln, agent_saboteur
import sys
from pathlib import Path
#sys.path.append(str(Path(__file__).parent.parent.parent))
from PokerPlus.Agents.agents_bots import agent_naif, agent_allIn, agent_saboteur, agent_serre_non_agressif, agent_large_non_agressif
from PokerPlus.Agents.agent_outs import agent_outs
from PokerPlus.Agents.Good_Agents import agent_SA
import matplotlib.pyplot as plt
import random
from time import sleep
from pprint import pprint

def plot_stat(stats, n, joueurs_bots_noms, max_players):
    plt.bar(stats["nbrWin"].keys(), stats["nbrWin"].values())

    # Ajouter des informations quel agent + nombre de victoires
    for i, v in enumerate(stats["nbrWin"].values()):
        plt.annotate(f"{joueurs_bots_noms[i]} \n {v}", xy=(i, v), ha='center', va='bottom')

    # Ajouter un titre et des étiquettes d'axe
    plt.title(f"Nombre de victoires pour chaque joueur, {n} parties jouées")
    plt.xlabel("Joueurs")
    plt.ylabel("Nombre de victoires")



    #plot de bar en fonction des valeurs de stats
    width = 0.35
    fig = plt.figure(2)
    ax = fig.add_axes([0,0,1,1])
    ind = [i for i in range(max_players)]

    #afficher les barres
    bottom = [0 for i in range(max_players)]
    for a,b in stats.items():
        if (a not in ["nbrWin", "profit", "nbrAction"]):
            t= ax.bar(ind,list(b.values()) , width, label=a, bottom=bottom)
            ax.bar_label(t, label_type='center')
            bottom = [x + y for x, y in zip(bottom, list(b.values()))]
    ax.set_title(f"Nombre d'actions pour chaque joueur, {n} parties joués")
    ax.legend()

    #plot bar du profit des joueurs
    fig = plt.figure(3)
    plt.bar(stats["profit"].keys(), stats["profit"].values())

    for i, v in enumerate(stats["profit"].values()):
        plt.annotate(f"{joueurs_bots_noms[i]} \n {v}", xy=(i, v), ha='center', va='bottom')

    # Ajouter un titre et des étiquettes d'axe
    plt.title(f"Profit de chaque joueur, {n} parties jouées")
    plt.xlabel("Joueurs")
    plt.ylabel("Profit (en $)")


    #plot bar du profit des joueurs / nbr de parties gagnées
    fig = plt.figure(4)
    #creation d'un dictionnaire avec des 0 pour les joueurs qui n'ont pas gagné et sinon on divise le profit par le nombre de victoires
    profit_par_victoire = {i:round(stats["profit"][i]/stats["nbrWin"][i],2) if stats["nbrWin"][i]!=0 else 0 for i in range(max_players)}
    plt.bar(profit_par_victoire.keys(),profit_par_victoire.values() ) # type: ignore

    for i,v in (profit_par_victoire.items()):
        plt.annotate(f"{joueurs_bots_noms[i]} \n {v}", xy=(i, v), ha='center', va='bottom')

    # Ajouter un titre et des étiquettes d'axe
    plt.title("Profit moyen par victoire pour chaque joueur")
    plt.xlabel("Joueur")
    plt.ylabel("Profit par victoire (en $)")

    plt.show()

    print(stats["nbrCall"])
    print(stats["nbrRaise"])
    print(stats["nbrAction"])
    print(stats["nbrFold"])

def plot_stat_tournois(stats, n, joueurs_bots_noms):
    plt.bar(stats["nbrWin tournoi"].keys(), stats["nbrWin tournoi"].values())

    for i, v in enumerate(stats["nbrWin tournoi"].values()):
        plt.annotate(f"{joueurs_bots_noms[i]} \n {v}", xy=(i, v), ha='center', va='bottom')

    # Ajouter un titre et des étiquettes d'axe
    plt.title(f"Nombre de tournois gagné pour chaque joueur, {n} tournois joués")
    plt.xlabel("Joueurs")
    plt.ylabel("Nombre de tournois gagné ")

    plt.show()
    print(stats["nbrWin tournoi"])

    # pour les autres stats on afiche au hasard 1 stats de tournois
    # Générer 5 indices aléatoires distincts
    indices_t = random.sample(range(n), 1)
    print(indices_t)
    for i in indices_t:
        print(f"nbr de partie win tournoi {i} :{stats['nbrWin partie'][f'tournoi {i}']}")
        print(f"nbrCall tournoi {i} :{stats['nbrCall'][f'tournoi {i}']}")
        print(f"nbrCheck tournoi {i} :{stats['nbrCheck'][f'tournoi {i}']}")
        print(f"nbrFold tournoi {i} :{stats['nbrFold'][f'tournoi {i}']}")

        print(f"Les raises du tournois {i}:\n{stats['raise'][f'tournoi {i}']}\n")
        indices_p = random.sample(range(len(stats['position'][f'tournoi {i}'])),3)
        for k in indices_p:
            print(f"Position partie {k}:{stats['position'][f'tournoi {i}'][f'partie {k}']}")
        print()



def pool_random(max_players, bots = [agent_outs().choix,agent_SA().action, agent_naif, agent_allIn, agent_saboteur, agent_serre_non_agressif, agent_large_non_agressif], bots_noms = ["agent_out", "agent_serre_agressif", "agent_naif", "agent_allIn", "agent_saboteur", "agent_serre_non_agressif", "agent_large_non_agressif"]):
    
    joueurs_bots = {}
    joueurs_bots_noms = {}
    deja_all_in = False
    for joueur in range(max_players): 
        num = random.randint(0,len(bots)-1)
        if bots_noms[num] == "agent_allIn" and deja_all_in:
            joueurs_bots[joueur] = bots[0]
            joueurs_bots_noms[joueur] = bots_noms[0]
        else:
            joueurs_bots[joueur] = bots[num]
            joueurs_bots_noms[joueur] = bots_noms[num]
        if bots_noms[num] == "agent_allIn":
            deja_all_in = True

    return joueurs_bots, joueurs_bots_noms

def pool_1(max_players, bots = [random_agent, agent_outs().choix, random_agent, random_agent, random_agent, agent_outs().choix], bots_noms = ["random_agent", "agent_out","random_agent", "random_agent", "random_agent", "random_agent"]):
    #pour chaque joueur, on lui attribue le bot avec le numéro de joueur
    joueurs_bots = {}
    joueurs_bots_noms = {}
    for joueur in range(max_players): 
        joueurs_bots[joueur] = bots[joueur]
        joueurs_bots_noms[joueur] = bots_noms[joueur]
    return joueurs_bots, joueurs_bots_noms

def get_stat(nmax=500, save=False, cles = ["nbrCall", "nbrCheck", "nbrRaise", "nbrFold", "nbrWin", "nbrAllin","nbrAction", "profit"], path='./res', plot=False, poolrandom = False):

    max_players = 5
    big_blind = 150
    small_blind = big_blind // 2
    buyin = 1000
    # Définir les statistiques à suivre

    stats = {cle:{i:0 for i in range(max_players)} for cle in cles}

    n=0
    seuil = 0.8
    if(poolrandom):
        joueurs_bots, joueurs_bots_noms = pool_random(max_players)
    else:
        joueurs_bots, joueurs_bots_noms = pool_1(max_players)
        
    #print(joueurs_bots)
    while(n<nmax):
        game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
        game.start_hand()
        n+=1
        mises = {i:0 for i in range(max_players)}
        while game.is_hand_running():
            # Utiliser le bot sélectionné pour le joueur actuel
            current_bot = joueurs_bots[game.current_player]
            if(current_bot==agent_allIn):
                action, total = current_bot(game,seuil)
            else:
                #print(current_bot(game), current_bot)
                action, total = current_bot(game)
            #print(f"Player {game.current_player} {action} {total}")

            # Met à jour les statistiques
            if (action == ActionType.CALL):
                stats["nbrCall"][game.current_player]+=1
            elif (action == ActionType.CHECK):
                stats["nbrCheck"][game.current_player]+=1
            elif (action == ActionType.RAISE):
                stats["nbrRaise"][game.current_player]+=1
            elif (action == ActionType.FOLD):
                stats["nbrFold"][game.current_player]+=1
            elif(action == ActionType.ALL_IN):
                stats["nbrAllin"][game.current_player]+=1
            
            game.take_action(action, total=total)
            mises[game.current_player] += game.player_bet_amount(game.current_player)

        gagnant=str(game.hand_history.settle)[7]
        
        gagnant = int(gagnant)
        stats["nbrWin"][gagnant] += 1
        stats["profit"][gagnant]= stats["profit"][gagnant] + game.pots[-1].get_total_amount() - mises[gagnant]
        for k,v in stats["profit"].items():
            if k != gagnant:
                stats["profit"][k] -= mises[k]

        # print(game.hand_history.settle,"\n\n\n")
        # afficher le nombre de parties jouées
        if save:
            path = game.export_history('./res')
        print("partie : ", n, end="\r")


    stats["nbrAction"]= {i:stats["nbrCall"][i]+stats["nbrCheck"][i]+stats["nbrRaise"][i]+stats["nbrFold"][i]+stats["nbrAllin"][i] for i in range(max_players)}
    stats_moy={cle:{i:stats[cle][i]/n for i in range(max_players)} for cle in cles}
    # Afficher les statistiques
    #print("call:",stats["nbrCall"],"check:",stats["nbrCheck"],"raise:",stats["nbrRaise"],"fold:",stats["nbrFold"],"profit",stats["profit"],"\n",sep="\n")
    #print(stats["nbrWin"],n)
    #print(stats_moy["profit"],n)


    if plot:
        plot_stat(stats, n, joueurs_bots_noms, max_players)
    # Créer un diagramme à barres avec les valeurs de victoires

    return stats

def get_stat_tournoi(nmax = 1, save=False, path='./res', plot=False, poolrandom = False, max_players=6):
    max_players = max_players
    big_blind = 150
    small_blind = big_blind // 2
    buyin = 1000 


    seuil = 0.8
    if(poolrandom):
        joueurs_bots, joueurs_bots_noms = pool_random(max_players)
    else:
        joueurs_bots, joueurs_bots_noms = pool_1(max_players) 
        #joueurs_bots, joueurs_bots_noms = pool_1(max_players,bots = [agent_outs().choix, agent_naif, agent_allIn, random_agent,agent_saboteur], bots_noms = ["agent_out", "agent_naif", "agent_allIn", "random_agent","agent_saboteur"])
    
    print(joueurs_bots_noms)

    stats={}
    stats["nbrWin tournoi"] ={i:0 for i in range(max_players)} #Nombre de tournois gagnés par chaque joueur

    #Nombre de parties gagnées par chaque joueur à chaque tournoi
    stats["nbrWin partie"] ={f"tournoi {k}":{i:0 for i in range(max_players)} for k in range(nmax)} 

    #Nombre de call, check, fold fait à chaque tournoi
    stats["nbrCall"] = {f"tournoi {k}":{i:0 for i in range(max_players)} for k in range(nmax)}
    stats["nbrCheck"] = {f"tournoi {k}":{i:0 for i in range(max_players)} for k in range(nmax)}
    stats["nbrFold"] = {f"tournoi {k}":{i:0 for i in range(max_players)} for k in range(nmax)}
    stats["nbrRaise"] = {f"tournoi {k}":{i:0 for i in range(max_players)} for k in range(nmax)}
    stats["nbrAction"] = {f"tournoi {k}":{i:0 for i in range(max_players)} for k in range(nmax)}


    #Raise fait par chaque joueur 
    stats["raise"] = {f"tournoi {k}":{i:[] for i in range(max_players)} for k in range(nmax)}
    
    stats["position"] = {f"tournoi {k}":{} for k in range(nmax)}

    stats["elimine"] =  {f"tournoi {k}":{i:0 for i in range(max_players)} for k in range(nmax)}
    #stats {
    #     "nbrWin tournoi":{0:0,1:0,2:0,3:0,4:0,5:0}
    #     "nbrcall":{tournoi 1:{0:0,1:0,2:0,3:0,4:0,5:0} tournoi_2:{0:0,1:0,2:0,3:0,4:0,5:0} ...}
    #     "nbrcheck":{tournoi 1:{0:0,1:0,2:0,3:0,4:0,5:0} tournoi_2:{0:0,1:0,2:0,3:0,4:0,5:0} ...}
    #     "nbrfold":{tournoi 1:{0:0,1:0,2:0,3:0,4:0,5:0} tournoi_2:{0:0,1:0,2:0,3:0,4:0,5:0} ...}
    #     "raise":{tournoi 1:{0:[mise1, mise2 ... mise,n],1:[mise1, mise2 ... mise,n],2:[mise1, mise2 ... mise,n],..,5:[mise1, mise2 ... mise,n]} {tournoi_1:{0:[mise1, mise2 ... mise,n],1:[mise1, mise2 ... mise,n],2:[mise1, mise2 ... mise,n],..,5:[mise1, mise2 ... mise,n]} ...}
    #     "position" : {tournoi 1}:{partie 1 : [01245], partie 2: [12045]...}
    nbr_tournoi=0
    while(nbr_tournoi<nmax):
        game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
        nbr_partie=0
        pos_avant=[]
        num_eliminé = 0

        while game.is_game_running():
            #print("hand")
            game.start_hand()
            nbr_partie+=1
            
            # les personnes dans le tournois 
            pos =[]
            for i in game.in_pot_iter():
                pos.append(i)

            if pos_avant:
                if(len(pos_avant)!= len(pos)):
                    for k in pos:
                        pos_avant.remove(k)
                    elimine = pos_avant[0]
                    num_eliminé += 1
                    stats["elimine"][f"tournoi {nbr_tournoi}"][elimine]+=num_eliminé
                    print(f"    le joueur {elimine} est éliminé")
                    

            
            if[nbr_partie != 1]:
                pos_avant = pos
            #print(pos, pos_avant)  


            stats["position"][f"tournoi {nbr_tournoi}"][f"partie {nbr_partie}"]=pos
            
                
            while game.is_hand_running():
                #print("hand running")
                current_bot = joueurs_bots[game.current_player]
                if(current_bot==agent_allIn):
                    action, total = current_bot(game,seuil)
                else:
                    #print("action")
                    action, total = current_bot(game)
                #print(f"Player {game.current_player}({joueurs_bots_noms[game.current_player]}) {action} {total}")

                try:
                    #print(current_bot, action, total)
                    game.take_action(action, total=total)
                    #print("action in try")
                except:
                    
                    if game.players[game.current_player].state == PlayerState.IN:
                        action = ActionType.CHECK

                    
                    action = ActionType.FOLD
                    game.take_action(action, total=None)

                if action == ActionType.CALL:
                    stats["nbrCall"][f"tournoi {nbr_tournoi}"][game.current_player]+=1
                    stats["nbrAction"][f"tournoi {nbr_tournoi}"][game.current_player]+=1
                elif action == ActionType.CHECK:
                    stats["nbrCheck"][f"tournoi {nbr_tournoi}"][game.current_player]+=1
                    stats["nbrAction"][f"tournoi {nbr_tournoi}"][game.current_player]+=1
                elif action == ActionType.FOLD:
                    stats["nbrFold"][f"tournoi {nbr_tournoi}"][game.current_player]+=1
                    stats["nbrAction"][f"tournoi {nbr_tournoi}"][game.current_player]+=1
                elif action == ActionType.RAISE:
                    stats["raise"][f"tournoi {nbr_tournoi}"][game.current_player].append(total)
                    stats["nbrRaise"][f"tournoi {nbr_tournoi}"][game.current_player]+=1
                    stats["nbrAction"][f"tournoi {nbr_tournoi}"][game.current_player]+=1
                elif action == ActionType.ALL_IN:
                    stats["raise"][f"tournoi {nbr_tournoi}"][game.current_player].append(total)
                    stats["nbrRaise"][f"tournoi {nbr_tournoi}"][game.current_player]+=1
                    stats["nbrAction"][f"tournoi {nbr_tournoi}"][game.current_player]+=1

            
            last_gagnant=str(game.hand_history.settle)[7]
            last_gagnant = int(last_gagnant)
            stats["nbrWin partie"][f"tournoi {nbr_tournoi}"][last_gagnant] += 1

        stats["nbrWin tournoi"][last_gagnant] += 1
        print(f"tournoi {nbr_tournoi} de {nbr_partie} parties gagné par joueur{last_gagnant} ({joueurs_bots_noms[last_gagnant]})")
        print(f"eliminé : {stats['elimine'][f'tournoi {nbr_tournoi}']}\n")
        nbr_tournoi+=1

    if plot:
        plot_stat_tournois(stats, nbr_tournoi, joueurs_bots_noms)

    return stats
