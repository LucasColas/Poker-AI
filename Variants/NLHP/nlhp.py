from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents import random_agent


class NLHP:
    """

    Simple class to play No Limit heads-up hold’em poker (NLHP).


    """

    def __init__(self, buyin=1000, small_blind=10, big_blind=20, gui=True):
        self.__game = None
        self.__nb_players = 2
        self.__buyin = buyin
        self.__small_blind = small_blind
        self.__big_blind = big_blind
        self.__gui_ = gui
        self.__gui = None

    def create_game(self):
        if not self.__game:
            self.__game = TexasHoldEm(
                buyin=self.__buyin,
                small_blind=self.__small_blind,
                big_blind=self.__big_blind,
                max_players=self.__nb_players,
            )
            if self.__gui_:
                self.__gui = TextGUI(self.__game)

    def is_game_running(self):
        """

        Check if a game is running.

        """
        print(self.__game is not None)
        return self.__game is not None

    def play(self):
        """

        Play a game of NLHP.

        """
        print("start")
        print("game", self.__game)
        print("game running", self.__game.is_game_running())

        while self.__game and self.__game.is_game_running():
            self.__game.start_hand()
            while self.__game.is_hand_running():
                if self.__gui_:
                    self.__gui.display_state()
                    self.__gui.wait_until_prompted()
                    self.__gui.run_step()
                # self.__game.take_action(*random_agent(self.__game))

        print("end")
