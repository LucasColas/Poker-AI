#un joueur sera considéré comme agressif s'il son nombre de call et de raise est grand par rapport au nombre d'action jouer

#vpip Voluntarily Put In Pot,tracks the percentage of hands in which a particular player voluntarily puts money into the pot
def vpip(nbr_call : dict,nbr_raise : dict, nbr_action : dict , max_player: int) -> dict:
    """retourne un dictionnaire avec la cle le joueur et la valeur le vpip"""
    vpip={}
    for i in range(max_player):
        if (nbr_action[i]!=0):
            vpip[i]=round((nbr_call[i]+nbr_raise[i])/nbr_action[i],2)
        else:
            vpip[i]=0
    return vpip


def list_agressif_vpip(nbr_call : dict,nbr_raise : dict, nbr_action: dict, max_player: int, seuil : int) -> dict:
    """rretourne un dictionnaire avec la cle le joueur et la valeur True si il est agressif et False sinon selon seuil donné"""
    vpips = vpip(nbr_call,nbr_raise,nbr_action,max_player)
    agressif={}
    for i in range(max_player):
        if (vpips[i] > seuil):
            print(f"le joueur {i} est agressif")
            agressif[i]=True
        else:
            print(f"le joueur {i} est faible")
            agressif[i]=False
    return agressif

#un joueur sera considéré comme large s'il son nombre de fold est petit par rapport au nombre d'action jouer
def list_large(nbr_fold : dict, nbr_action: dict, max_player: int, seuil : int) -> dict:
    """retourne un dictionnaire avec la cle le joueur et la valeur True si il est large et False sinon selon seuil donné"""
    large={}
    for i in range(max_player):
        if (nbr_fold[i]/nbr_action[i] < seuil):
            print(f"le joueur {i} est large")
            large[i]=True
        else:
            print(f"le joueur {i} est serré")
            large[i]=False
    return large

###test
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