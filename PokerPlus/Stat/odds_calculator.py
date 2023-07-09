from texasholdem.card.deck import Deck
from texasholdem.evaluator.evaluator import *
from itertools import combinations


class odds_calculator:
    def __init__(self):
        self.__deck = Deck()
        self.__hands = []
        self.__board = []

    def newGame(self):
        self.__deck = Deck()
        self.__hands = []
        self.__board = []

    def getCard(self, n: int, v: str):
        for i in range(len(self.__deck.cards)):
            if str(self.__deck.cards[i])[0] == n and str(self.__deck.cards[i])[1] == v:
                print(self.__deck.cards[i])
                return self.__deck.cards.pop(i)

    def main_print(self):
        # print("Deck : ", self.__deck)
        self.newGame()
        print("suits : ")
        print("clubs (c) : ♣")
        print("diamonds (d) : ♦")
        print("hearts (h) : ♥")
        print("spades (s) : ♠")
        print("Your cards are : ")

        for i in range(2):
            n = input("Card number ? ")
            v = input("Card suit ? ")
            self.__hands.append(self.getCard(n, v))

        print("Board : ")
        for i in range(3):
            n = input("Card number ? ")
            v = input("Card suit ? ")
            self.__board.append(self.getCard(n, v))

        print("Your cards : ", self.__hands)
        print("Board : ", self.__board)
        betting = int(input("betting : "))
        pot_size = int(input("pot size : "))

        print("Outs : ")
        outs, outs_hands = self.getOuts()
        print("outs : ", outs)
        for key in outs_hands:
            print(key, " : ", outs_hands[key])

        print("Probability to get : ")
        for key in outs_hands:
            print(key, " : ", self.Probability(outs_hands[key], outs) * 100, "%")

        print(
            "Probability outs : ",
            self.Probability(outs, len(self.__deck.cards)) * 100,
            "%",
        )
        # get odd_ration of betting and pot_size
        odd_ratio = pot_size / betting
        print("Odd pot ratio : ", odd_ratio)
        print("Odd pot : ", 1 / (odd_ratio + 1) * 100, "%")

        if len(self.__board) == 3:
            outs_pairs, outs_hands_pairs = self.getOuts_2cards()
            len_pairs = len(list(combinations(self.__deck.cards, 2)))
            print("outs pairs : ", (outs_pairs / len_pairs) * 100, "%")
            for key in outs_hands_pairs:
                print(
                    key,
                    " : ",
                    self.Probability(outs_hands_pairs[key], outs_pairs) * 100,
                    "%",
                )

        print("card turn :")
        n = input("Card number ? ")
        v = input("Card suit ? ")
        self.__board.append(self.getCard(n, v))

        outs, outs_hands = self.getOuts()
        print("Probability to get : ")
        for key in outs_hands:
            print(key, " : ", self.Probability(outs_hands[key], outs) * 100, "%")

        betting = int(input("betting : "))
        pot_size = int(input("pot size : "))

        odd_ratio = pot_size / betting
        print("Odd pot ratio : ", odd_ratio)
        print("odd pot : ", 1 / (odd_ratio + 1) * 100, "%")

        print("card river :")
        n = input("Card number ? ")
        v = input("Card suit ? ")
        self.__board.append(self.getCard(n, v))

        betting = int(input("betting : "))
        pot_size = int(input("pot size : "))

        odd_ratio = pot_size / betting
        print("Odd pot ratio : ", odd_ratio)
        print("odd pot : ", 1 / (odd_ratio + 1) * 100, "%")

        print("best hand : ", rank_to_string(evaluate(self.__hands, self.__board)))

    def Probability(self, val, total):
        return val / total

    def getOuts(self):
        outs_hands = {
            "Straight Flush": 0,
            "Four of a Kind": 0,
            "Full House": 0,
            "Flush": 0,
            "Straight": 0,
            "Three of a Kind": 0,
            "Two Pair": 0,
            "Pair": 0,
            "High card": 0,
        }  # number of outs for each different hand
        outs = 0  # total number of outs
        actual_hand_rank = get_five_card_rank_percentage(
            evaluate(self.__hands, self.__board)
        )
        for card in self.__deck.cards:
            if card not in self.__hands and card not in self.__board:
                cards = self.__hands + [card] + self.__board
                # print(cards)
                new_hand_rank = get_five_card_rank_percentage(
                    evaluate(cards[:2], cards[2:])
                )
                if new_hand_rank > actual_hand_rank:
                    outs += 1
                    outs_hands[rank_to_string(evaluate(cards[:2], cards[2:]))] += 1

        return outs, outs_hands

    def getOuts_2cards(self):
        outs_hands = {
            "Straight Flush": 0,
            "Four of a Kind": 0,
            "Full House": 0,
            "Flush": 0,
            "Straight": 0,
            "Three of a Kind": 0,
            "Two Pair": 0,
            "Pair": 0,
            "High card": 0,
        }

        outs = 0
        actual_hand_rank = get_five_card_rank_percentage(
            evaluate(self.__hands, self.__board)
        )
        for two_cards in combinations(self.__deck.cards, 2):
            cards = self.__hands + list(two_cards) + self.__board
            new_hand_rank = get_five_card_rank_percentage(
                evaluate(cards[:2], cards[2:])
            )
            if new_hand_rank > actual_hand_rank:
                outs += 1
                outs_hands[rank_to_string(evaluate(cards[:2], cards[2:]))] += 1
        return outs, outs_hands
