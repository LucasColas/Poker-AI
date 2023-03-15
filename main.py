from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent, call_agent
from texasholdem.evaluator.evaluator import *
from texasholdem.card.deck import Deck
from agent import agent_naif

max_players = 3
big_blind = 150
small_blind = big_blind // 2
buyin = 1000
game = TexasHoldEm(buyin=buyin, big_blind=big_blind, small_blind=small_blind, max_players=max_players)
gui = TextGUI(game=game, visible_players=[])

while game.is_game_running():

    game.start_hand()
    while game.is_hand_running():
        if game.current_player == 0:
            game.take_action(*agent_naif(game))
        gui.set_visible_players([game.current_player])
        #cards = Deck(num=52)
        #cards = [card for card in cards if card not in game.hands[game.current_player]]
        gui.run_step()
