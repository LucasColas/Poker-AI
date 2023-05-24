

from texasholdem.game.action_type import ActionType

import random
from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
from PokerPlus.Agents.agents_bots import agent_naif, agent_allIn, agent_saboteur, agent_serre_non_agressif, agent_large_non_agressif
from PokerPlus.Agents.agent_outs import agent_outs
from PokerPlus.Agents.Good_Agents import agent_SA
from PokerPlus.Comportement.comportement import vpip, getRatioLarge, getVpip, ratio_large
from sklearn.cluster import KMeans
import pickle


def simu_bots_humains():
    #Mettre menu pour choisir les agents, et nombre de personnes
    #Stats pour avoir Nb Fold / Nb Parties et VPIP.
    #Stocker dans un fichier les comportements des joueurs.
    #Stocker dans un autre fichier vainqueurs des tournois.
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
            if game.current_player == 0:
                gui.set_visible_players([game.current_player])

            if game.current_player != 0:
                #Agent.setGame(game)
                game.take_action(*Agent.choix(game))
            else:
                gui.run_step()
                gui.set_visible_players([])

            #game.take_action(*random_agent(game))
            
            print("action, total : ", game._action)
            gui.display_action()
            

        #path = game.export_history('./pgns')
        gui.display_win()


def getComportements(stats : dict, cluster):
    """
    Donne le comportement pour chaque joueur. A partir du cluster.
    Renvoie une liste le comportement. 
    """

    with open('model.pkl', 'rb') as file:
        kmeans = pickle.load(file)
        

def pool_bots_min_max(nummin,maxplayer, 
                      bots = [random_agent, agent_outs().choix,agent_SA().action, agent_naif, agent_allIn, agent_saboteur, agent_serre_non_agressif, agent_large_non_agressif], 
                      bots_noms = ["random_agent", "agent_out", "agent_serre_agressif", "agent_naif", "agent_allIn", "agent_saboteur", "agent_serre_non_agressif", "agent_large_non_agressif"]): 
    """
    Crée un pool de bots aléatoires de taille nummin à maxplayer.
    """
    joueurs_bots = {}
    joueurs_bots_noms = {}
    deja_all_in = False
    for i in range(nummin, maxplayer):
        num = random.randint(0,len(bots)-1)
        joueurs_bots[i] = bots[num]
        joueurs_bots_noms[i] = bots_noms[num]
    return joueurs_bots, joueurs_bots_noms 

def getRatio(stats_Fold : dict, nb_joueurs : int): 
    """
    Renvoie la somme des Fold pour chaque joueur.
    """
    somme_fold = {i:0 for i in range(nb_joueurs)}
    nb_parties = {i:0 for i in range(nb_joueurs)}
    for i in stats_Fold.keys():
        for p in stats_Fold[i].keys():
            somme_fold[p] += stats_Fold[i][p]
            nb_parties[p] += 1

    return {i: getRatioLarge(somme_fold[i], nb_parties[i]) for i in somme_fold.keys()}

def VPIP(stats_Call : dict, stats_Raise : dict, stats_Fold : dict, nb_actions : dict, nb_joueurs : int):
    """
    Renvoie le VPIP pour chaque joueur.
    """
    somme_fold = {i:0 for i in range(nb_joueurs)}
    nb_call = {i:0 for i in range(nb_joueurs)}
    nb_raise = {i:0 for i in range(nb_joueurs)}
    VPIP = {i:0 for i in range(nb_joueurs)}
    somme_actions = {i:0 for i in range(nb_joueurs)}
    for i in stats_Fold.keys():
        for p in stats_Fold[i].keys():
            somme_fold[p] += stats_Fold[i][p]
    
    for i in stats_Call.keys():
        for p in stats_Call[i].keys():
            nb_call[p] += stats_Call[i][p] + nb_raise[i][p]

    for i in stats_Raise.keys():
        for p in stats_Raise[i].keys():
            nb_raise[p] += stats_Raise[i][p]

    for i in nb_actions.keys():
        for p in nb_actions[i].keys():
            somme_actions[p] += nb_actions[i][p]

    return {i: getVpip(nb_call[i], nb_raise[i], somme_fold[i], somme_actions[i]) for i in somme_fold.keys()}
    

def tournoi_avec_humain():
    """
    Faire un tournoi avec des humains.
    """
    #Mettre menu pour choisir les agents, et nombre de personnes
    min = 2
    max = 9
    print("Bienvenue dans le tournoi de PokerPlus !")
    print(f"Veuillez choisir le nombre de joueurs (entre {min} et {max}) : ")
    max_players = int(input())
    print("Veuillez choisir le nombre d'humains qui joueront dans ce tournoi (entre 1 et {}) : ".format(max_players))
    nb_humains = int(input())


    big_blind = 50
    small_blind = big_blind // 2
    buyin = 1000

    #Choix des agents
    joueurs_bots, joueurs_bots_noms = pool_bots_min_max(nummin=nb_humains, maxplayer=max_players)
    #print(joueurs_bots_noms)
    game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
    gui = TextGUI(game=game, visible_players=[])
    stats ={i:{} for i in ["nbrCall", "nbrCheck", "nbrRaise", "nbrFold", "nbrAllin", "nbrActions"]}
    nb_partie = 0
    while game.is_game_running():
        game.start_hand()
        nb_partie += 1
        for j in stats.keys():
            stats[j][f"partie {nb_partie}"] = {i:0 for i in range(max_players)}
        
        while game.is_hand_running():
            gui.display_state()
            gui.wait_until_prompted()
            if game.current_player in range(nb_humains):
                gui.set_visible_players([game.current_player])
               

            if game.current_player in joueurs_bots:
                print("Le joueur {} joue.".format(joueurs_bots_noms[game.current_player]))
                current_bot = joueurs_bots[game.current_player]
                action, total = current_bot(game)
                game.take_action(action, total=None)
            else:
                gui.run_step()
                gui.set_visible_players([])

            action, total = game._action

            if (action == ActionType.CALL):
                stats["nbrCall"][f"partie {nb_partie}"][game.current_player]+=1
            elif (action == ActionType.CHECK):
                stats["nbrCheck"][f"partie {nb_partie}"][game.current_player]+=1
            elif (action == ActionType.RAISE):
                stats["nbrRaise"][f"partie {nb_partie}"][game.current_player]+=1
            elif (action == ActionType.FOLD):
                stats["nbrFold"][f"partie {nb_partie}"][game.current_player]+=1
            elif (action == ActionType.ALL_IN):
                stats["nbrAllin"][f"partie {nb_partie}"][game.current_player]+=1
            stats["nbrActions"][f"partie {nb_partie}"][game.current_player]+=1
            gui.display_action()
            
        #path = game.export_history('./pgns')
        gui.display_win()
        print(stats["nbrCall"])

        
    pass