from texasholdem.game.game import TexasHoldEm, Pot
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.agents.basic import random_agent
#from agents import agent_naif,agent_alln, agent_saboteur
import sys
from pathlib import Path
#sys.path.append(str(Path(__file__).parent.parent.parent))
from PokerPlus.Agents.agents_bots import agent_naif, agent_allIn, agent_saboteur
from PokerPlus.Agents.agent_outs import agent_outs
from PokerPlus.Agents.Good_Agents import agent_SA
import matplotlib.pyplot as plt
import random

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
    ax.set_title(f"Nombre d'actions pour chaque joueur, {n} parties jouées")
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
    plt.bar(stats["nbrWin"].keys(), stats["nbrWin"].values())

    for i, v in enumerate(stats["nbrWin"].values()):
        plt.annotate(f"{joueurs_bots_noms[i]} \n {v}", xy=(i, v), ha='center', va='bottom')

    # Ajouter un titre et des étiquettes d'axe
    plt.title(f"Nombre de tournois gagné pour chaque joueur, {n} tournois jouées")
    plt.xlabel("Joueurs")
    plt.ylabel("Nombre de tournois gagné ")

    plt.show()
    print(stats["nbrWin"])



def pool_random(max_players, bots = [agent_outs().choix,agent_SA().action, agent_naif, agent_allIn, random_agent,agent_saboteur], bots_noms = ["agent_out", "agent_serre_agressif", "agent_naif", "agent_allIn", "random_agent","agent_saboteur"]):
    
    joueurs_bots = {}
    joueurs_bots_noms = {}
    for joueur in range(max_players): 
        num = random.randint(0,len(bots)-1)
        joueurs_bots[joueur] = bots[num]
        joueurs_bots_noms[joueur] = bots_noms[num]
    return joueurs_bots, joueurs_bots_noms

def pool_1(max_players, bots = [agent_outs().choix,agent_SA().action, agent_naif, agent_allIn, random_agent,agent_saboteur], bots_noms = ["agent_out", "agent_serre_agressif", "agent_naif", "agent_allIn", "random_agent","agent_saboteur"]):
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
        # TODO: prendre en compte les blind
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

def get_stat_tournoi(nmax = 200, save=False, cles = ["nbrWin"], path='./res', plot=False, poolrandom = False):
    max_players = 5
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
    stats = {cle:{i:0 for i in range(max_players)} for cle in cles}
    n=0
    while(n<nmax):
        game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
        n+=1
        nbr_partie=0
        while game.is_game_running():
            game.start_hand()
            nbr_partie+=1
            while game.is_hand_running():

                current_bot = joueurs_bots[game.current_player]
                if(current_bot==agent_allIn):
                    action, total = current_bot(game,seuil)
                else:
                    action, total = current_bot(game)
                #print(f"Player {game.current_player}({joueurs_bots_noms[game.current_player]}) {action} {total}")
                game.take_action(action, total=total)

            #print(f"{nbr_partie}:{game.hand_history.settle}\n")
            last_gagnant=str(game.hand_history.settle)[7]
            last_gagnant = int(last_gagnant)
        stats["nbrWin"][last_gagnant] += 1
        print(f"tournoi {n} de {nbr_partie} parties gagné par joueur{last_gagnant} ({joueurs_bots_noms[last_gagnant]})")
    
    if plot:
        plot_stat_tournois(stats, n, joueurs_bots_noms)

    return stats
