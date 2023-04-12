from texasholdem.game.game import TexasHoldEm, Pot
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.agents.basic import random_agent
from agents import agent_naif,agent_allIn, agent_saboteur
from agent_outs import agent_outs
import matplotlib.pyplot as plt
import random

max_players = 5
big_blind = 150
small_blind = big_blind // 2
buyin = 1000



# Définir les statistiques à suivre
cles = ["nbrCall", "nbrCheck", "nbrRaise", "nbrFold", "nbrWin", "nbrAllin","nbrAction", "profit"]
stats = {cle:{i:0 for i in range(max_players)} for cle in cles}


n=0
nmax=500
seuil=0.8
agent_out = agent_outs()

# Définir les fonctions des bots
bots = [agent_out.choix, agent_naif, agent_allIn, random_agent,agent_saboteur]
#bot_nom = [i.__name__ for i in bots] sauf pour agent_out.choix devient "agent_out"
bots_noms = ["agent_out", "agent_naif", "agent_allIn", "random_agent","agent_saboteur"]
# Initialiser le dictionnaire pour stocker les bots de chaque joueur
joueurs_bots = {}
joueurs_bots_noms = {}
# Pour chaque joueur, choisir un bot aléatoire et stocker cette information dans le dictionnaire
for joueur in range(max_players):
    bot = random.choice(bots)
    joueurs_bots[joueur] = bots[joueur]
    joueurs_bots_noms[joueur] = bots_noms[joueur]

#print(joueurs_bots)
while(n<nmax):
    game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
    game.start_hand()
    n+=1
    mises = {i:0 for i in range(max_players)}
    while game.is_hand_running():
        # Utiliser le bot sélectionné pour le joueur actuel attention au bot agent_allIn qui a 2 paramètres
        agent_out.setGame(game)
        current_bot = joueurs_bots[game.current_player]
        if current_bot == agent_out.choix:
            action, total = current_bot(game)
        elif(current_bot==agent_allIn):
            action, total = current_bot(game,seuil)
        else:
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
    ## TODO: prendre en compte les blind
    gagnant = int(gagnant)
    stats["nbrWin"][gagnant] += 1
    stats["profit"][gagnant]= stats["profit"][gagnant] + game.pots[-1].get_total_amount() - mises[gagnant]
    for k,v in stats["profit"].items():
        if k != gagnant:
            stats["profit"][k] -= mises[k]

    # print(game.hand_history.settle),"\n\n\n")
    # afficher le nombre de parties jouées
    print(n, end="\r")


stats["nbrAction"]= {i:stats["nbrCall"][i]+stats["nbrCheck"][i]+stats["nbrRaise"][i]+stats["nbrFold"][i]+stats["nbrAllin"][i] for i in range(max_players)}
stats_moy={cle:{i:stats[cle][i]/n for i in range(max_players)} for cle in cles}
# Afficher les statistiques
#print("call:",stats["nbrCall"],"check:",stats["nbrCheck"],"raise:",stats["nbrRaise"],"fold:",stats["nbrFold"],"profit",stats["profit"],"\n",sep="\n")
#print(stats["nbrWin"],n)
#print(stats_moy["profit"],n)

# Créer un diagramme à barres avec les valeurs de victoires
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
plt.bar(profit_par_victoire.keys(),profit_par_victoire.values() )

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
