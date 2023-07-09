import math


class GameMeta:
    OUTCOMES = {"loose": -1, "win": 1}
    INF = float("inf")


class MCTSMeta:
    EXPLORATION = math.sqrt(2)
