from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.agents.basic import random_agent
from agents import agent_naif,agent_Sacha
from agent_outs import agent_outs
import matplotlib.pyplot as plt
import random

max_players = 6
big_blind = 150
small_blind = big_blind // 2
buyin = 1000




#TODO : ajouter profit
cles = ["nbrCall", "nbrCheck", "nbrRaise", "nbrFold", "nbrWin", "nbrAllin"]
stats = {cle:{i:0 for i in range(max_players)} for cle in cles}

n=0
nmax=100000
seuil=0.8

# Définir les fonctions des bots
bots = [random_agent, agent_naif, agent_outs, agent_Sacha, random_agent, agent_naif]
bots_noms = ["random_agent", "agent_naif", "agent_outs", "agent_Sacha", "random_agent", "agent_naif"]
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
    while game.is_game_running():
        game.start_hand()
        n+=1

        while game.is_hand_running():
            # Utiliser le bot sélectionné pour le joueur actuel attention au bot agent_Sacha qui a 2 paramètres
            current_bot = joueurs_bots[game.current_player]
            if(current_bot==agent_Sacha):
                action, total =current_bot(game,seuil)
            else:
                action, total = current_bot(game)
            #print(f"Player {game.current_player} {action} {total}")

            # Mettre à jour les statistiques
            if (action == ActionType.CALL):
                stats["nbrCall"][game.current_player]+=1
            elif (action == ActionType.CHECK):
                stats["nbrCheck"][game.current_player]+=1
            elif(action == ActionType.RAISE):
                stats["nbrRaise"][game.current_player]+=1
            elif(action == ActionType.FOLD):
                stats["nbrFold"][game.current_player]+=1
            elif(action == ActionType.ALL_IN):
                stats["nbrAllin"][game.current_player]+=1
            game.take_action(action, total=total)

        gagnant=str(game.hand_history.settle)[7]
        stats["nbrWin"][int(gagnant)]+=1

        # print(game.hand_history.settle),"\n\n\n")
    # afficher le nombre de parties jouées
    print(n, end="\r")

# Afficher les statistiques
print("call:",stats["nbrCall"],"check:",stats["nbrCheck"],"raise:",stats["nbrRaise"],"fold:",stats["nbrFold"],"\n",sep="\n")
print(stats["nbrWin"],n)
#print(joueurs_bots)

# Créer un diagramme à barres avec les valeurs de victoires
plt.bar(joueurs_bots_noms.values(), stats["nbrWin"].values())

# Ajouter des légendes pour chaque barre
for i, v in enumerate(stats["nbrWin"].values()):
    #plt.text(i, v, str(v), ha='center')
    # Ajouter des informations supplémentaires
    plt.annotate(joueurs_bots[i].__name__, xy=(i, v), ha='center', va='bottom')

# Ajouter un titre et des étiquettes d'axe
plt.title("Nombre de victoires pour chaque joueur")
plt.xlabel("Joueur")
plt.ylabel("Nombre de victoires")

# Afficher le diagramme
plt.show()
