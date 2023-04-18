import os
import csv
from PokerPlus.Stat.stat import get_stat
from PokerPlus.Comportement.comportement import vpip, ratio_large

def get_data(m: int=500) -> dict:
    """
    Fonction qui récupère les stats de m simulations.
    Exemple de return :
    {0: {'nbrCall': {0: 219, 1: 175, 2: 180, 3: 154, 4: 239}, 'nbrCheck': {0: 363, 1: 348, 2: 58, 3: 124, 4: 51}, 'nbrRaise': {0: 26, 1: 16, 2: 0, 3: 317, 4: 38}, 'nbrFold': {0: 322, 1: 377, 2: 492, 3: 295, 4: 446}, 'nbrWin': {0: 147, 1: 98, 2: 8, 3: 196, 4: 51}, 'nbrAllin': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, 'nbrAction': {0: 930, 1: 916, 2: 730, 3: 890, 4: 774}, 'profit': {0: 106894, 1: 34521, 2: -26025, 3: 214397, 4: 10236}}, 1: {'nbrCall': {0: 195, 1: 177, 2: 190, 3: 169, 4: 227}, 'nbrCheck': {0: 398, 1: 428, 2: 75, 3: 140, 4: 45}, 'nbrRaise': {0: 26, 1: 19, 2: 0, 3: 282, 4: 36}, 'nbrFold': {0: 344, 1: 337, 2: 489, 3: 292, 4: 447}, 'nbrWin': {0: 110, 1: 130, 2: 11, 3: 197, 4: 52}, 'nbrAllin': {0: 0, 1: 0, 2: 2, 3: 0, 4: 0}, 'nbrAction': {0: 963, 1: 961, 2: 756, 3: 883, 4: 755}, 'profit': {0: 60383, 1: 51123, 2: -22652, 3: 216912, 4: 3787}}, 2: {'nbrCall': {0: 202, 1: 191, 2: 184, 3: 125, 4: 248}, 'nbrCheck': {0: 416, 1: 393, 2: 56, 3: 137, 4: 64}, 'nbrRaise': {0: 34, 1: 9, 2: 0, 3: 271, 4: 43}, 'nbrFold': {0: 313, 1: 357, 2: 486, 3: 308, 4: 450}, 'nbrWin': {0: 152, 1: 97, 2: 14, 3: 187, 4: 50}, 'nbrAllin': {0: 0, 1: 0, 2: 1, 3: 0, 4: 0}, 'nbrAction': {0: 965, 1: 950, 2: 727, 3: 841, 4: 805}, 'profit': {0: 100961, 1: 34390, 2: -22250, 3: 201928, 4: -2060}}, 3: {'nbrCall': {0: 207, 1: 173, 2: 186, 3: 154, 4: 252}, 'nbrCheck': {0: 421, 1: 418, 2: 75, 3: 130, 4: 58}, 'nbrRaise': {0: 19, 1: 11, 2: 0, 3: 289, 4: 37}, 'nbrFold': {0: 324, 1: 360, 2: 489, 3: 296, 4: 442}, 'nbrWin': {0: 131, 1: 103, 2: 11, 3: 200, 4: 55}, 'nbrAllin': {0: 0, 1: 0, 2: 1, 3: 0, 4: 0}, 'nbrAction': {0: 971, 1: 962, 2: 751, 3: 869, 4: 789}, 'profit': {0: 86124, 1: 35496, 2: -26000, 3: 214545, 4: 10983}}, 4: {'nbrCall': {0: 212, 1: 178, 2: 203, 3: 141, 4: 244}, 'nbrCheck': {0: 361, 1: 371, 2: 61, 3: 132, 4: 76}, 'nbrRaise': {0: 15, 1: 9, 2: 0, 3: 257, 4: 39}, 'nbrFold': {0: 328, 1: 363, 2: 483, 3: 301, 4: 443}, 'nbrWin': {0: 137, 1: 100, 2: 17, 3: 191, 4: 55}, 'nbrAllin': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, 'nbrAction': {0: 916, 1: 921, 2: 747, 3: 831, 4: 802}, 'profit': {0: 78126, 1: 39722, 2: -23523, 3: 193427, 4: 8352}}}
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
