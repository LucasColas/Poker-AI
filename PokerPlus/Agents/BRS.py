from texasholdem.game.game import TexasHoldEm
def eval():
    pass

def GenerateMoves(MaxPlayer: int):
    pass

def doMove():
    pass


def BRS(alpha : float, beta : float, depth : int, turn : int, game : TexasHoldEm, MAX: int):
    """
        Implémentation de BRS.
        Pour déterminer les coups probables on se basera sur le type de joueurs.
        Pour avoir le type de joueurs : Kmeans qui labélise. Puis ensuite classifieur Bayesien qui
        détermine l'action la plus probable. Mais l'action doit aussi être l'action qui rapporte le plus.
        Donc on doit avoir une fonction permettant d'évaluer le gain du joueur pour chaque action qu'il peut faire. 
    """
    Moves = []
    if depth <= 0:
        return eval()
    
    if turn == MAX: #root player’s turn
        Moves = GenerateMoves(len(game.players))

     