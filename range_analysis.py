from texasholdem.card.deck import Deck

"""
"A" -> Ace : as
"T" -> 10
"J" -> Jack : valet
"Q" -> Queen : Reine
"K" -> King : Roi
"s" -> Space : pique
"h" -> Heart : coeur
"c" -> Clover : trèfle
"d" -> Diamond : carreau

"""
nb_cards = 52
d = Deck()
cards = d.draw(num=nb_cards) #Every card is created
print(len(cards))

def range_analysis_preflop():
    pass
