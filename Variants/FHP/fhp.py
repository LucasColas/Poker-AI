from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents import random_agent


class fhp:
    """

    heads-up flop hold’em poker (FHP).
    FHP is similar to heads-up limit Texas hold’em (HULH) poker,
    but ends after the second betting round rather than the fourth,
    with only three community cards ever dealt.

    """

    def __init__(self, buyin=10000, big_blind=100, small_blind=50, gui=False) -> None:
        self.__game = None
        self.__nb_players = 2
        self.__buyin = buyin
        self.__small_blind = small_blind
        self.__big_blind = big_blind
        self.__gui_ = gui
        self.__gui = None

    def play(self):
        if not self.__game:
            self.__game = TexasHoldEm(
                buyin=self.__buyin,
                small_blind=self.__small_blind,
                big_blind=self.__big_blind,
                max_players=self.__nb_players,
            )
            if self.__gui:
                self.__gui = TextGUI(self.__game)
        while self.__game and self.__game.is_game_running():
            self.__game.start_hand()
            while self.__game.is_hand_running():
                if self.__gui:
                    self.__gui.display_state()
                    self.__gui.wait_until_prompted()
                self.__game.take_action(*random_agent(self.__game))
