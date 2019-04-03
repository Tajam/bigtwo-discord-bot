import json
import random

class Suit():
    data = None
    config = '../config/suit.json'
    #=====
    SPADES = 'spades'
    HEARTS = 'hearts'
    CLUBS = 'clubs'
    DIAMONDS = 'diamonds'
    #=====
    def __init__(self, name):
        d = Suit.data
        if not d:
            raise Exception('Please read config!')
        self._name = name
        self._power = d[name]['power']
        self._emoji = d[name]['discord_icon']
    
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
    
    @classmethod
    def get_all(cls):
        d = cls.data
        if not d:
            raise Exception('Please read config!')
        return [
            Suit(Suit.SPADES),
            Suit(Suit.HEARTS),
            Suit(Suit.CLUBS),
            Suit(Suit.DIAMONDS)
        ]
        
    @classmethod
    def get_random(cls):
        d = cls.data
        if not d:
            raise Exception('Please read config!')
        r = random.choice(list(d.keys()))
        return Suit(r)
        
    @classmethod
    def load_config(cls):
        with open(cls.config, 'r') as f:
            cls.data = json.loads(f.read())

if __name__ == '__main__':
    Suit.load_config()
    print(Suit.get_random())
    print(Suit.get_all())
    print(Suit(Suit.CLUBS) < Suit(Suit.HEARTS))
    print(Suit(Suit.CLUBS) > Suit(Suit.HEARTS))
    print(Suit(Suit.CLUBS) == Suit(Suit.HEARTS))
