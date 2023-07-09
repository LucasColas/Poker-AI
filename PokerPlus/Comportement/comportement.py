# un joueur sera considéré comme agressif s'il son nombre de call et de raise est grand par rapport au nombre d'action jouer


# vpip Voluntarily Put In Pot,tracks the percentage of hands in which a particular player voluntarily puts money into the pot
def vpip(
    nbr_call_p: dict,
    nbr_raise_p: dict,
    nbr_action_p: dict,
    nbr_fold_p: dict,
    max_player: int,
) -> dict:
    """retourne un dictionnaire avec le joueur comme clé et le vpip comme valeur"""

    return {
        i: getVpip(nbr_call_p[i], nbr_raise_p[i], nbr_fold_p[i], nbr_action_p[i])
        for i in nbr_call_p.keys()
    }


def getVpip(
    nb_call: int, nb_raise: int, nb_fold: int, nb_action: int, alpha: int = 0.3
) -> float:
    # print("nb call : ", nb_call, "nb raise : ", nb_raise, "nb fold : ", nb_fold, "nb action : ", nb_action)
    if (nb_action - nb_fold) != 0:
        return round(
            ((1 - alpha) * nb_call + (1 + alpha) * nb_raise) / (nb_action - nb_fold), 2
        )
    return 0


def getRatioLarge(nb_fold: int, nb_partie: int) -> float:
    if nb_partie != 0:
        # print("nb fold : ", nb_fold, "nb partie : ", nb_partie, nb_fold/nb_partie > 1)
        return round((1 - (nb_fold / nb_partie)), 2)
    return 0


def list_agressif_vpip(
    nbr_call: dict, nbr_raise: dict, nbr_action: dict, max_player: int, seuil: int = 0.5
) -> dict:
    """retourne un dictionnaire avec la cle le joueur et la valeur True si il est agressif et False sinon selon seuil donné"""
    vpips = vpip(nbr_call, nbr_raise, nbr_action, max_player)
    agressif = {}
    for i in range(max_player):
        if vpips[i] > seuil:
            print(f"le joueur {i} est agressif")
            agressif[i] = True
        else:
            print(f"le joueur {i} est faible")
            agressif[i] = False
    return agressif


def ratio_large(nbr_fold: dict, nbr_partie: dict, max_player: int):
    print("nbr fold : ", nbr_fold, "nbr partie : ", nbr_partie)
    return {i: getRatioLarge(nbr_fold[i], nbr_partie[i]) for i in nbr_fold.keys()}


# un joueur sera considéré comme large si son nombre de fold est petit par rapport au nombre d'action jouer
def list_large(
    nbr_fold: dict, nbr_action: dict, max_player: int, seuil: int = 0.5
) -> dict:
    """retourne un dictionnaire avec la cle le joueur et la valeur True si il est large et False sinon selon seuil donné"""
    large = {}
    for i in range(max_player):
        if nbr_fold[i] / nbr_action[i] < seuil:
            print(f"le joueur {i} est large")
            large[i] = True
        else:
            print(f"le joueur {i} est serré")
            large[i] = False
    return large


###test
"""
nbr_call = {0: 232, 1: 182, 2: 195, 3: 131, 4: 227}
nbr_raise ={0: 0, 1: 7, 2: 0, 3: 266, 4: 27}
nbr_action = {0: 926, 1: 905, 2: 740, 3: 855, 4: 765}
max_player = 5
seuil = 0.40

print(vpip(nbr_call,nbr_raise,nbr_action,max_player))
print(list_agressif_vpip(nbr_call,nbr_raise,nbr_action,max_player,seuil))

nbr_fold = {0: 373, 1: 390, 2: 396, 3: 295, 4: 457}
print(list_large(nbr_fold,nbr_action,max_player,seuil))

# aggressif : le joueur fait call ou raise + de seuil % du temps
# faible : le joueur fait call ou raise - de seuil % du temps
# large : le joueur fait fold - de seuil % du temps
# serré : le joueur fait fold + de seuil % du temps

"""
