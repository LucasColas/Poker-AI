from PokerPlus.Agents.fonctions_auxiliaires import *



class agent_comportement:
    """
    Stratégie :
    Avant chaque action trouver le comportement de chaque joueur grace au cluster.

    Plus il y a de serre, plus on peut jouer.
    Plus il y a de agressif, plus on fait attention a ce que l'on joue


    """
    
    def __init__(self) :
        self.cluster = None
        self.comportement = {}
        self.comportement["Serré agressif"] = 0
        self.comportement["Serré passif"] = 0
        self.comportement["Large agressif"] = 0
        self.comportement["Large passif"] = 0

