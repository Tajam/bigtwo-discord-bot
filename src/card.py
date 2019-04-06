import json
import random
from rank import RankSet, BigTwoRank
from suit import SuitSet, PokerSuit

class Deck():

    def __init__(self, rankset, suitset):
        self.rankset = rankset
        self.suitset = suitset

    def get_card(self, rank_i, suit_i):
        rank_o = self.rankset.create(rank_i)
        suit_o = self.suitset.create(suit_i)
        return Card(rank_o, suit_o)

    def get_random(self):
        r = self.rankset.get_random()
        s = self.suitset.get_random()
        return Card(r,s)

    def list(self):
        r = self.rankset.list()
        s = self.suitset.list()
        return [Card(i,j) for j in s for i in r]

    def list_random(self):
        r = self.list()
        random.shuffle(r)
        return r

class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return str(self.rank) + ' of ' + str(self.suit)

    def __repr__(self):
        return self.__class__.__name__+'(\''+str(self)+'\')'

    def __gt__(self, other):
        r = self.rank > other.rank
        e = self.rank == other.rank
        s = self.suit > other.suit
        return r|(e&s)

    def __lt__(self, other):
        r = self.rank < other.rank
        e = self.rank == other.rank
        s = self.suit < other.suit
        return r|(e&s)

    def __eq__(self, other):
        r = self.rank == other.rank
        s = self.suit == other.suit
        return r&s

    def emoji(self):
        return  self.suit._emoji + self.rank._emoji

if __name__ == '__main__':
    bigtwo_deck = Deck(
        RankSet(BigTwoRank.CONFIG_FILE),
        SuitSet(PokerSuit.CONFIG_FILE)
        )
    print(bigtwo_deck.get_random())
    print(bigtwo_deck.list())
    print(bigtwo_deck.list_random())
    c1 = bigtwo_deck.get_card(BigTwoRank.LARGEST,PokerSuit.SPADES)
    c2 = bigtwo_deck.get_card(BigTwoRank.SMALLEST,PokerSuit.DIAMONDS)
    print(c1 > c2)
    print(c1 < c2)
    print(c1 == c2)
    
