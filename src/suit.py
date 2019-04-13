import json
import random


class PokerSuit:
    SPADES = 0
    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3
    CONFIG_FILE = '../config/suit.json'


class SuitSet:

    def __init__(self, config):
        with open(config, 'r') as f:
            self._rawdata = json.loads(f.read())
            self._name = self._rawdata['name']
            self._data = self._rawdata['data']
    
    def __str__(self):
        return self._name.capitalize()

    def __repr__(self):
        return self.__class__.__name__+'(\''+str(self)+'\')'

    def create(self, index):
        return _Suit(self._data[index])
    
    def list(self):
        return [_Suit(n) for n in self._data]

    def length(self):
        return len(self._data)
    
    def get_random(self):
        s = random.choice(self._data)
        return _Suit(s)


class _Suit():

    def __init__(self, suit):
        self._name = suit['name']
        self._power = suit['power']
        self._emoji = suit['discord_icon']
    
    def __str__(self):
        return self._name.capitalize()

    def __repr__(self):
        return self.__class__.__name__+'(\''+str(self)+'\')'

    def __gt__(self, other):
        return self._power > other._power

    def __lt__(self, other):
        return self._power < other._power

    def __eq__(self, other):
        return self._power == other._power


if __name__ == '__main__':
    poker_set = SuitSet(PokerSuit.CONFIG_FILE)
    print(poker_set.length())
    print(poker_set.list())
    print(poker_set.get_random())
    print(poker_set.create(PokerSuit.CLUBS) < poker_set.create(PokerSuit.HEARTS))
    print(poker_set.create(PokerSuit.CLUBS) > poker_set.create(PokerSuit.HEARTS))
    print(poker_set.create(PokerSuit.CLUBS) == poker_set.create(PokerSuit.HEARTS))
