from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.agents.basic import random_agent
from agents import agent_naif,agent_Sacha

max_players = 6
big_blind = 150
small_blind = big_blind // 2
buyin = 1000


nbrCall ={i:0 for i in range(max_players)}
nbrCheck={i:0 for i in range(max_players)}
nbrRaise={i:0 for i in range(max_players)}
nbrFold ={i:0 for i in range(max_players)}
nbrWin  ={i:0 for i in range(max_players)}
nbrAllin={i:0 for i in range(max_players)}

n=0
nmax=100000
seuil=0.8

while(n<nmax):
    game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
    while game.is_game_running():
        game.start_hand()
        n+=1
        #le joueur 0 et 1 sont les joueurs random
        #le joueur 2 et 3 sont les joueurs naif
        #le joueur 4 et 5 sont les joueurs allIN(seuil)
        while game.is_hand_running():
            if(game.current_player in [0,1]):
                action, total = random_agent(game)
            elif(game.current_player in [2,3]):
                action, total = agent_naif(game)
            else:
                action, total = agent_Sacha(game,seuil)

            #print(f"Player {game.current_player} {action} {total}")
            if (action == ActionType.CALL):
                nbrCall[game.current_player]+=1
            elif (action == ActionType.CHECK):
                nbrCheck[game.current_player]+=1
            elif(action == ActionType.RAISE):
                nbrRaise[game.current_player]+=1
            elif(action == ActionType.FOLD):
                nbrFold[game.current_player]+=1
            elif(action == ActionType.ALL_IN):
                nbrAllin[game.current_player]+=1
            game.take_action(action, total=total)

        gagnant=str(game.hand_history.settle)[7]
        nbrWin[int(gagnant)]+=1

        # print(game.hand_history.settle),"\n\n\n")
    print(n, end="\r")
print("call:",nbrCall,"check:",nbrCheck,"raise:",nbrRaise,"fold:",nbrFold,"\n",sep="\n")
print(nbrWin,n)
