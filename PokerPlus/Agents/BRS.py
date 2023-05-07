from texasholdem.game.game import TexasHoldEm


class BestReplySearch:
    def __init__(self, *args):
        self._opponents = None
        self._game = None

    @property
    def opponents(self):
        return self._opponents
    
    @opponents.setter
    def opponents(self, val):
        self._opponents = val

    def eval(self):
        pass

    def GenerateMoves(self, MaxPlayer: int):
        pass

    def doMove(self):
        pass


    def BRS(self, alpha : float, beta : float, depth : int, turn : bool, game : TexasHoldEm) -> float:
        """
            Implémentation de BRS.
            
        """
        Moves = []
        if depth <= 0:
            return self.eval()
        
        if turn: #root player’s turn
            Moves = self.GenerateMoves(len(game.players))
            turn = False #Min

        else:
            for o in self._opponents:
                Moves = self.GenerateMoves(o)
            turn = True #Max

        for m in Moves:
            self.doMove(m)
            v = -self.BRS(-alpha, -beta, depth-1, turn, game)
            self.undoMove(m)
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return alpha

        

        