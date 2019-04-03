import json
import random

class Rank():
    data = None
    config = '../config/rank.json'
    def __init__(self, rank):
        d = Rank.data
        if not d:
            raise Exception('Please read config!')
        self._name = d[rank]['name']
        self._power = d[rank]['power']
        self._emoji = d[rank]['discord_icon']
    
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
        return [Rank(n) for n in range(len(d))]
        
    @classmethod
    def get_random(cls):
        d = cls.data
        if not d:
            raise Exception('Please read config!')
        r = random.randint(0,len(d)-1)
        return Rank(r)
        
    @classmethod
    def load_config(cls):
        with open(cls.config, 'r') as f:
            cls.data = json.loads(f.read())

if __name__ == '__main__':
    Rank.load_config()
    print(Rank.get_random())
    print(Rank.get_all())
    print(Rank(1) < Rank(4))
    print(Rank(1) > Rank(4))
    print(Rank(3) == Rank(3))
