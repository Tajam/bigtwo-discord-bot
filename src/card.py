import json
import random
from rank import Rank
from suit import Suit

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

    @classmethod
    def get_random(cls):
        r = Rank.get_random()
        s = Suit.get_random()
        return Card(r,s)
        
    @staticmethod
    def load_config():
        Rank.load_config()
        Suit.load_config()

if __name__ == '__main__':
    Card.load_config()
    print(Card.get_random())
