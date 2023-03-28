from texasholdem.game.game import TexasHoldEm 
from texasholdem.gui.text_gui import TextGUI
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.agents.basic import random_agent
from agent import agent_naif,agent_allIN
from time import sleep


max_players = 6
big_blind = 150
small_blind = big_blind // 2
buyin = 1000
game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
gui = TextGUI(game=game)



seuil=0.5

nbrCall ={0:[0],1:[0],2:[0],3:[0],4:[0],5:[0],6:[0]}
nbrCheck={0:[0],1:[0],2:[0],3:[0],4:[0],5:[0],6:[0]}
nbrRaise={0:[0],1:[0],2:[0],3:[0],4:[0],5:[0],6:[0]}
nbrFold ={0:[0],1:[0],2:[0],3:[0],4:[0],5:[0],6:[0]}
nbrWin  ={0:[0],1:[0],2:[0],3:[0],4:[0],5:[0],6:[0]}
nbrAllin={0:[0],1:[0],2:[0],3:[0],4:[0],5:[0],6:[0]}

n=0
while game.is_game_running():
    game.start_hand()
    n+=1
    #print("call:",nbrCall,"check:",nbrCheck,"raise:",nbrRaise,"fold:",nbrFold,"\n",sep="\n")
    while game.is_hand_running():
        
        action, total = agent_allIN(game,seuil)
        print(f"Player {game.current_player} {action} {total}")
        if (action == ActionType.CALL):
            nbrCall[game.current_player][0]+=1
        elif (action == ActionType.CHECK):
            nbrCheck[game.current_player][0]+=1
        elif(action == ActionType.RAISE):
            nbrRaise[game.current_player][0]+=1 
        elif(action == ActionType.FOLD):
            nbrFold[game.current_player][0]+=1 
        elif(action == ActionType.ALL_IN):
            nbrAllin[game.current_player][0]+=1
        game.take_action(action, total=total)
        # gui.display_state()
        # gui.wait_until_prompted()
        # gui.display_action()
        # gui.set_visible_players([game.current_player])
    #sleep(1)
    #print("n=",n,"call:",nbrCall,"check:",nbrCheck,"raise:",nbrRaise,"fold:",nbrFold,"allIn:",nbrAllin,"\n",sep="\n")
    gagnant=str(game.hand_history.settle)[7]
    nbrWin[int(gagnant)][0]+=1
    
    # print(game.hand_history.settle),"\n\n\n")
    #gui.display_win()
print(nbrWin,n)

