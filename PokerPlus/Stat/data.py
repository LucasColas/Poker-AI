import os
import csv
from PokerPlus.Stat.stat import get_stat, get_stat_tournoi
from PokerPlus.Comportement.comportement import vpip, ratio_large

def get_data(m: int=2, max_players=6) -> dict:
    """
    Fonction qui récupère les stats de m simulations de tournois.
    """
    data_dict = {}

    for i in range(m):
        data_dict[i] = get_stat_tournoi(nmax=1, poolrandom=True, max_players=max_players, verbose=True)

    return data_dict

def write_data(m:int, max_players: int = 6, filename: str = "data.csv", path: str = ""):
    max_players = max_players
    simu = 0
    nb_tournoi = 0
    simu_print = f"simu : {simu}"
    fieldnames = ['vpip', 'ratio action']
    data_dict = get_data(m=m, max_players=max_players)
    with open(path+filename, 'w') as csvfile:

        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(m):

            #print(data_dict[i]["nbrCall_p"][f"tournoi {nb_tournoi}"])
            #print(data_dict[i]["nbrRaise_p"][f"tournoi {nb_tournoi}"])
            #print(data_dict[i]["nbrAction_p"][f"tournoi {nb_tournoi}"])
            #print(data_dict[i]["nbrFold_p"][f"tournoi {nb_tournoi}"])
            print("nb partie : ",data_dict[i]["nbrPartie"][f"tournoi {nb_tournoi}"])
            

            vpip_ = vpip(data_dict[i]["nbrCall"][f"tournoi {nb_tournoi}"], 
                         data_dict[i]["nbrRaise"][f"tournoi {nb_tournoi}"], 
                         data_dict[i]["nbrAction"][f"tournoi {nb_tournoi}"], 
                         data_dict[i]["nbrFold"][f"tournoi {nb_tournoi}"], max_players)
            ratio_large_ = ratio_large(data_dict[i]["nbrFold"][f"tournoi {nb_tournoi}"], data_dict[i]["nbrPartie"][f"tournoi {nb_tournoi}"], max_players)
            for vpip_v, ratio in zip(vpip_.values(), ratio_large_.values()):
                writer.writerow({fieldnames[0]: vpip_v, fieldnames[1]: ratio})
                