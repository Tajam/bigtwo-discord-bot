from player import Player
from bigtwo import BigTwo
from suit import PokerSuit
from rank import BigTwoRank
from combo import BigTwoCombo
import random
import math


class Server:
    
    def __init__(self, name):
        self._name = name
        self.lobby_list = {}

    def add_lobby(self, server_id, channel_id):
        l = '{}-{}'.format(server_id, channel_id)
        if l in self.lobby_list:
            return False
        self.lobby_list[l] = Lobby(Server.generate_hash(10))
        return True

    def remove_lobby(self, server_id, channel_id):
        l = '{}-{}'.format(server_id, channel_id)
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


class Lobby:
    MAX_PLAYER = 4

    def __init__(self, refid):
        self._refid = refid
        self.player_pool = {}
        self.player_turn = []
        self.started = False
        self.host_id = None
        self.current_owner = None
        self.current_combo = None

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
            self.player_pool[author.id] = Player(author)
            return True
        return False

    def leave(self, author):
        self.player_pool.pop(author.id, None)
        if len(self.player_pool) == 0:
            return True
        return False

    def stop(self):
        if not self.started: return False
        self.started = False
        for i in self.player_pool:
            self.player_pool[i].cards = []
        return True

    def start(self):
        if self.started: return False
        self.started = True
        shuffled_cards = BigTwo.DECK.list_random()
        x = math.floor(len(shuffled_cards)/len(self.player_pool))
        for _ in range(x):
            for i in self.player_pool:
                self.player_pool[i].give_card(shuffled_cards.pop())
        #Give the extra card to the player who owns the smallest card
        if len(self.player_pool) == 3:
            smallest_card = BigTwo.DECK.get_card(BigTwoRank.SMALLEST, PokerSuit.DIAMONDS)
            for i in self.player_pool:
                if self.player_pool[i].have_card(smallest_card):
                    self.player_pool[i].throw_cards(0)
                    self.player_pool[i].give_card(shuffled_cards.pop())
                    break
        self.player_turn = [n for n in self.player_pool]
        random.shuffle(self.player_turn)
        return True

    def attack(self, player_id, cards):
        # Code
        # 0 - Success
        # 1 - Not your turn
        # 2 - Invalid combo
        # 3 - Opponent is stronger
        if player_id != self.whos_turn():
            return 1
        combo = BigTwoCombo(cards)
        if not combo.is_valid():
            return 2
        if self.current_combo == None:
            self.current_owner = player_id
            self.current_combo = combo
            self.next_turn()
            return 0
        if not self.current_combo == combo:
            return 2
        if self.current_combo > combo:
            return 3
        self.current_owner = player_id
        self.current_combo = combo
        self.next_turn()
        return 0

    def whos_turn(self):
        return self.player_turn[0]

    def next_turn(self):
        self.player_turn = self.player_turn[1:] + [self.player_turn[0]]
        if self.whos_turn() == self.current_owner:
            self.current_combo = None