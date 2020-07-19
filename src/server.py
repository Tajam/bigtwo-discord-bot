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
        l = "{}-{}".format(server_id, channel_id)
        if l in self.lobby_list:
            return False
        self.lobby_list[l] = Lobby(Server.generate_hash(10))
        return True

    def remove_lobby(self, server_id, channel_id):
        l = "{}-{}".format(server_id, channel_id)
        self.lobby_list.pop(l, None)

    @staticmethod
    def generate_hash(length):
        h = ""
        for _ in range(length):
            d = chr(random.randint(48, 57))
            u = chr(random.randint(65, 90))
            l = chr(random.randint(97, 122))
            h += random.choice([d, u, l])
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
        self._first_play = True
        self.winners = []

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

    def start(self):
        if self.started:
            return False
        num_players = len(self.player_pool)
        self.started = True
        shuffled_cards = BigTwo.DECK.list_random()

        # If we have two players, then deal only 13 cards
        if len(self.player_pool) <= 2:
            x = 13
        else:
            x = math.floor(len(shuffled_cards) / len(self.player_pool))

        for _ in range(x):
            for i in self.player_pool:
                self.player_pool[i].give_card(shuffled_cards.pop())

        # Give the extra card to the player who owns the smallest card
        smallest_card = sorted(
            [card for player in self.player_pool.values() for card in player.cards]
        )[0]
        if len(self.player_pool) == 3:
            for i in self.player_pool:
                if self.player_pool[i].have_card(smallest_card):
                    self.player_pool[i].give_card(shuffled_cards.pop())
                    break

        self.player_turn = [n for n in self.player_pool]
        random.shuffle(self.player_turn)
        player_id, _ = next(
            filter(lambda p: p[1].have_card(smallest_card), self.player_pool.items(),)
        )
        self.player_turn.remove(player_id)
        self.player_turn.insert(0, player_id)
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

        highest_card = sorted(
            [card for player in self.player_pool.values() for card in player.cards]
        )[-1]

        hand_sizes_check = [
            len(player.cards) < combo.length
            for player_id, player in self.player_pool.items()
            if player_id in self.player_turn[1:]
        ]

        force_pass = (
            any([card == highest_card for card in cards])
            and (combo._type == BigTwoCombo.SINGLE or combo._type == BigTwoCombo.DOUBLE)
            or all(hand_sizes_check)
        )

        if not combo.is_valid():
            return 2
        if self.current_combo == None:
            # If this is the first played card, enforce that it is the lowest card
            if self._first_play:
                smallest_card = sorted(
                    [
                        card
                        for player in self.player_pool.values()
                        for card in player.cards
                    ]
                )[0]
                if not any([card == smallest_card for card in cards]):
                    return 2
                self._first_play = False
            self.current_owner = player_id
            self.current_combo = combo
            self.next_turn(force_pass=force_pass)
            return 4 if force_pass else 0
        if self.current_owner != player_id and not self.current_combo == combo:
            return 2
        if self.current_owner != player_id and self.current_combo > combo:
            return 3
        self.current_owner = player_id
        self.current_combo = combo

        self.next_turn(force_pass=force_pass)
        return 4 if force_pass else 0

    def whos_turn(self):
        return self.player_turn[0]

    def next_turn(self, force_pass=False):
        # If 2S played as a single
        if force_pass == False:
            self.player_turn = self.player_turn[1:] + [self.player_turn[0]]
            if len(self.player_pool) > 1 and self.whos_turn() == self.current_owner:
                self.current_combo = None

    def add_winner(self, player_id):
        self.winners.append(player_id)
        self.player_turn.remove(player_id)
        self.current_combo = None
