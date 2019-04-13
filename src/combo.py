from bigtwo import BigTwo
from suit import PokerSuit

#Not so generic class
class BigTwoCombo():
    NONE = 'invalid'
    SINGLE = 'single'
    DOUBLE = 'double'
    TRIPLE = 'triple'
    STRAIGHT = 'straight'
    FLUSH = 'flush'
    HOUSE = 'house'
    FOUR_OF_A_KIND = 'four of a kind'
    ROYAL_FLUSH = 'royal flush'

    def __init__(self, card_list):
        self.card_list = sorted(card_list)
        self.length = len(self.card_list)
        self._leader = max(card_list)
        self._type = None
        self._combo_power = 0
        #Start detect everything
        self._detect_combo()

    def __str__(self):
        return self._type.capitalize()

    def __repr__(self):
        return self.__class__.__name__+'(\''+str(self)+'\')'

    def __eq__(self, other):
        if other == None:
            return False
        return self.length == other.length

    def __gt__(self, other):
        if self == other:
            if self.length == 5:
                if self._type == other._type:
                    if self._type in [BigTwoCombo.FLUSH, BigTwoCombo.ROYAL_FLUSH]:
                        if self._leader.suit == other._leader.suit:
                            return self._leader > other._leader
                        else:
                            return self._leader.suit > other._leader.suit
                    else:
                        return self._leader > other._leader
                else:
                    return self._combo_power > other._combo_power
            elif self.length in range(1, 4):
                return self._leader > other._leader
            else:
                raise Exception('Comparing invalid combos')
        raise Exception('Invalid comparison of combo with different card numbers')

    def __lt__(self, other):
        raise Exception('Please use greater than comparison')

    def _detect_combo(self):
        if self.length == 1:
            self._type = BigTwoCombo.SINGLE
            return
        if self.length == 5:
            s = self._is_straight()
            f = self._is_flush()
            if s&f:
                self._type = BigTwoCombo.ROYAL_FLUSH
                self._combo_power = 5
                return
            if s:
                self._type = BigTwoCombo.STRAIGHT
                self._combo_power = 1
                return
            if f:
                self._type = BigTwoCombo.FLUSH
                self._combo_power = 2
                return
            if self._detect_grouping(): return
        if self._is_same_rank():
            if self.length == 3:
                self._type = BigTwoCombo.TRIPLE
                return
            if self.length == 2:
                self._type = BigTwoCombo.DOUBLE
                return
        self._type = BigTwoCombo.NONE

    def _detect_grouping(self):
        d = {}
        for n in self.card_list:
            if str(n.rank) not in d:
                d[str(n.rank)] = [n]
                continue
            d[str(n.rank)].append(n)
        if len(d) == 2:
            dd = d[max(d, key=lambda x: len(d[x]))]
            self._leader = max(dd)
            if len(dd) == 4:
                self._type = BigTwoCombo.FOUR_OF_A_KIND
                self._combo_power = 4
            if len(dd) == 3:
                self._type = BigTwoCombo.HOUSE
                self._combo_power = 3
            return True
        return False
                
    def _is_same_rank(self):
        for i, n in enumerate(self.card_list):
            if self.card_list[(i+1)%self.length].rank != n.rank:
                return False
        return True
    
    def _is_straight(self):
        valid = 4
        for i, n in enumerate(self.card_list):
            next_rank = BigTwo.RANKSET.get_next(n.rank)
            if self.card_list[(i+1)%self.length].rank == next_rank:
                valid -= 1
        return valid == 0

    def _is_flush(self):
        for i, n in enumerate(self.card_list):
            if self.card_list[(i+1)%self.length].suit != n.suit:
                return False
        return True

    def is_valid(self):
        return self._type != BigTwoCombo.NONE

if __name__ == '__main__':
    sample = [
            [
            BigTwo.DECK.get_card(3,PokerSuit.SPADES),
            BigTwo.DECK.get_card(4,PokerSuit.SPADES),
            BigTwo.DECK.get_card(5,PokerSuit.SPADES),
            BigTwo.DECK.get_card(6,PokerSuit.SPADES),
            BigTwo.DECK.get_card(2,PokerSuit.SPADES)
            ],
            [
            BigTwo.DECK.get_card(7,PokerSuit.SPADES),
            BigTwo.DECK.get_card(4,PokerSuit.HEARTS),
            BigTwo.DECK.get_card(1,PokerSuit.SPADES),
            BigTwo.DECK.get_card(6,PokerSuit.HEARTS),
            BigTwo.DECK.get_card(2,PokerSuit.SPADES)
            ],
            [
            BigTwo.DECK.get_card(7,PokerSuit.SPADES),
            BigTwo.DECK.get_card(7,PokerSuit.HEARTS),
            BigTwo.DECK.get_card(7,PokerSuit.CLUBS),
            BigTwo.DECK.get_card(1,PokerSuit.HEARTS),
            BigTwo.DECK.get_card(1,PokerSuit.SPADES)
            ],
            [
            BigTwo.DECK.get_card(2,PokerSuit.SPADES),
            BigTwo.DECK.get_card(2,PokerSuit.HEARTS),
            BigTwo.DECK.get_card(2,PokerSuit.CLUBS),
            BigTwo.DECK.get_card(2,PokerSuit.DIAMONDS),
            BigTwo.DECK.get_card(0,PokerSuit.SPADES)
            ],
            [
            BigTwo.DECK.get_card(10,PokerSuit.SPADES),
            BigTwo.DECK.get_card(10,PokerSuit.HEARTS),
            BigTwo.DECK.get_card(10,PokerSuit.CLUBS),
            BigTwo.DECK.get_card(9,PokerSuit.HEARTS),
            BigTwo.DECK.get_card(6,PokerSuit.SPADES)
            ],
            [
            BigTwo.DECK.get_card(3,PokerSuit.SPADES),
            BigTwo.DECK.get_card(3,PokerSuit.HEARTS)
            ],
            [
            BigTwo.DECK.get_card(5,PokerSuit.SPADES),
            BigTwo.DECK.get_card(5,PokerSuit.HEARTS),
            BigTwo.DECK.get_card(5,PokerSuit.CLUBS)
            ],
            [
            BigTwo.DECK.get_card(7,PokerSuit.SPADES),
            BigTwo.DECK.get_card(3,PokerSuit.HEARTS),
            BigTwo.DECK.get_card(7,PokerSuit.CLUBS)
            ]
        ]
    print([BigTwoCombo(n) for n in sample])
