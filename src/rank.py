import json
import random


class BigTwoRank:

    LARGEST = 1
    SMALLEST = 2
    CONFIG_FILE = '../config/rank.json'


class RankSet:

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
        return _Rank(self._data[index])

    def list(self):
        return [_Rank(n) for n in self._data]

    def length(self):
        return len(self._data)

    def get_next(self, rank):
        for i, n in enumerate(self._data):
            if n['name'] == rank._name:
                s = self._data[(i+1)%self.length()]
                return _Rank(s)
            
    def get_random(self):
        s = random.choice(self._data)
        return _Rank(s)


class _Rank:
    data = None
    config = '../config/rank.json'

    def __init__(self, rank):
        self._name = rank['name']
        self._power = rank['power']
        self._emoji = rank['discord_icon']
    
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
    bigtwo_rank = RankSet(BigTwoRank.CONFIG_FILE)
    print(bigtwo_rank.length())
    print(bigtwo_rank.list())
    print(bigtwo_rank.get_random())
    print(bigtwo_rank.create(1) < bigtwo_rank.create(4))
    print(bigtwo_rank.create(1) > bigtwo_rank.create(4))
    print(bigtwo_rank.create(3) == bigtwo_rank.create(3))
    print(bigtwo_rank.get_next(bigtwo_rank.create(12)))
