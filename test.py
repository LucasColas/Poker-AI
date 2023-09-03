from PokerPlus.DeepCFR.deep_cfr import deep_cfr, save_deep_cfr
from texasholdem.game.game import TexasHoldEm

def main():
    print("create game")
    game = TexasHoldEm(buyin=1500, big_blind=80, small_blind=40, max_players=2)
    game.start_hand()
    save_deep_cfr("", "DeepCFR", nb_iterations=10000, nb_players=2, nb_game_tree_traversals=200, game=game, n_actions=3, n_card_types=4, n_bets=20)


if __name__ == "__main__":
    main()