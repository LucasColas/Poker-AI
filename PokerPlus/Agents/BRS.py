from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState

class BestReplySearch:
    def __init__(self, *args):
        self._opponents = None
        self._game = None
        self._player = None
        self._simu = {}
        self._chips = {}

    def setter(self, game: TexasHoldEm):
        self._game = game
        self._opponents = [o for o in game.players if o != game.players[game.current_player]]
        self._player = game.players[game.current_player]
        self._chips = {player.player_id:0 for player in game.players}

    def eval(self, player: int, game: TexasHoldEm) -> int:
        """
        Se baser sur la main
        Se baser sur les outs 
        Se baser sur les jetons misés
        Peut-être se baser aussi sur la position
        """
        pass

    def GenerateMoves(self, player: int):
        return {player:[action for action in ActionType]}

    def doMove(self, p : int, m : ActionType):
        if m == ActionType.ALL_IN:
            pass
        elif m == ActionType.CALL:
            pass
        elif m == ActionType.CHECK:
            pass
        elif m == ActionType.FOLD:
            pass
        elif m == ActionType.RAISE:
            pass

    def undoMove(self, p : int, m : ActionType):
        pass

    def terminal_state(self) -> bool:
        pass


    def BRS(self, alpha : int, beta : int, depth : int, turn : bool, game : TexasHoldEm, player:int) -> float:
        """

            Implémentation de BRS.
            alpha = -infini
            beta = +infini
            
        """
        Moves = []
        if depth <= 0 or self.terminal_state():
            return self.eval(player)
        
        if turn: #root player’s turn
            Moves = self.GenerateMoves(self._player)
            turn = False #Min

        else:
            for o in self._opponents:
                Moves += self.GenerateMoves(o)
            turn = True #Max

        for p,m in Moves.items():
            self.doMove(p,m)
            v = -self.BRS(-alpha, -beta, depth-1, turn, game)
            self.undoMove(p,m)
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return alpha