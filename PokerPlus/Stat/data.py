import os
import csv
from PokerPlus.Stat.stat import get_stat
from PokerPlus.Comportement.comportement import vpip, ratio_large

def get_data(m: int=500) -> dict:
    """
    Fonction qui récupère les stats de m simulations.
    """
    data_dict = {}

    for i in range(m):
        data_dict[i] = get_stat()

    return data_dict

def write_data(data_dict: dict, filename: str = "data.csv", path: str = ""):
    nb_max_players = len(data_dict[0]['nbrCall'])
    simu = 0
    simu_print = f"simu : {simu}"
    with open(path+filename, 'w') as csvfile:

        fieldnames = ['vpip', 'ratio action']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for simu in data_dict.values():

            print(simu_print, end="\r")

            vpip_ = vpip(simu["nbrCall"], simu["nbrRaise"], simu["nbrAction"], nb_max_players)
            ratio_large_ = ratio_large(simu["nbrFold"], simu["nbrAction"], nb_max_players)
            for val, val2 in zip(vpip_.values(), ratio_large_.values()):
                writer.writerow({fieldnames[0]: val, fieldnames[1]: val2})

            simu += 1
