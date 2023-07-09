from PokerPlus.Agents.fonctions_auxiliaires import *
from PokerPlus.Agents.agent_outs import *
from PokerPlus.Agents.Good_Agents import *
from PokerPlus.Agents.agents_bots import *


def agent_comportement(
    game: TexasHoldEm, pred: dict, num_bot: int, agent_outs: agent_outs
):
    # On regarde ce quon a dans prediction sauf nous
    if pred:
        nb_Tight = 0
        nb_Loose = 0

        nb_Aggressive = 0
        nb_Passive = 0

        for i, val in pred.items():
            if i != num_bot:
                # on compte le nombre:
                if val == "Tight-Passive":
                    nb_Tight += 1
                    nb_Passive += 1
                elif val == "Loose-Passive":
                    nb_Loose += 1
                    nb_Passive += 1
                elif val == "Tight-Aggressive":
                    nb_Loose += 1
                    nb_Passive += 1
                elif val == "Loose-Aggressive":
                    nb_Loose += 1
                    nb_Passive += 1
        # print(pred)
        # print(nb_Tight,nb_Loose,nb_Aggressive,nb_Passive)

        # Si on a beaoucp de large pas trop agressif : agent_naif
        if nb_Loose > nb_Tight and nb_Loose > nb_Aggressive:
            return agent_naif(game)
        # Si on a beaucoup de tight pas trop agressif : agent_SA
        elif nb_Tight > nb_Loose and nb_Tight > nb_Aggressive:
            return agent_SA.action(game)

        else:
            return agent_outs.choix(game)

    else:
        return agent_outs.choix(game)
