from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from PokerPlus.DeepCFR.game_tree import print_card_mapping

game = TexasHoldEm(buyin=500, big_blind=5, small_blind=2, max_players=2)
gui = TextGUI(game=game)


def heads_up():
    print("Hello World !")
    choice = 999

    while choice != 0:
        print("0 - Quit")
        print("1 - Simulate a head's up game")
        choice = int(input("What do you want to do ? "))

        if choice == 1:
            game = TexasHoldEm(buyin=500, big_blind=5, small_blind=2, max_players=2)
            gui = TextGUI(game=game)

            while game.is_game_running():
                game.start_hand()

                while game.is_hand_running():
                    gui.run_step()

            print("end")


def main():
    print_card_mapping()


if __name__ == "__main__":
    main()
