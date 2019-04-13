from player import Player
from bigtwo import BigTwo
import random
import math

class Server():
    
    def __init__(self, name):
        self._name = name
        self.lobby_list = {}

    def add_lobby(self, server_id, channel_id):
        l = '{}-{}'.format(server_id,channel_id)
        if l in self.lobby_list:
            return False
        self.lobby_list[l] = Lobby(Server.generate_hash(10))
        return True

    def remove_lobby(self, server_id, channel_id):
        l = '{}-{}'.format(server_id,channel_id)
        self.lobby_list.pop(l, None)
    
    @staticmethod
    def generate_hash(length):
        h = ''
        for _ in range(length):
            d = chr(random.randint(48,57))
            u = chr(random.randint(65,90))
            l = chr(random.randint(97,122))
            h += random.choice([d,u,l])
        return h

class Lobby():
    MAX_PLAYER = 4

    def __init__(self, refid):
        self._refid = refid
        self.player_pool = {}
        self.started = False

    def set_host(self, player_id):
        if player_id in self.player_pool:
            self.host_id = player_id
            return True
        return False

    def set_random_host(self):
        self.host_id = random.choice(list(self.player_pool.keys()))
        return self.host_id

    def join(self, author):
        if len(self.player_pool) < Lobby.MAX_PLAYER:
            self.player_pool[author.id] = Player(author.display_name)
            return True
        return False

    def leave(self, author):
        self.player_pool.pop(author.id,None)
        if len(self.player_pool) == 0:
            return True
        return False

    def start_game(self):
        shuffled_cards = BigTwo.DECK.list_random()
        x = math.floor(len(shuffled_cards)/len(self.player_pool))
        for _ in range(x):
            for i in self.player_pool:
                self.player_pool[i].give_card(shuffled_cards.pop())
        if len(self.player_pool) == 3:
            smallest_card = BigTwo.DECK.get_card(BigTwoRank.SMALLEST,PokerSuit.DIAMONDS)
            for i in self.player_pool:
                #HERE
        
