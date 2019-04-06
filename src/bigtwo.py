from card import Deck
from rank import RankSet, BigTwoRank
from suit import SuitSet, PokerSuit

class BigTwo():
    RANKSET = RankSet(BigTwoRank.CONFIG_FILE)
    SUITSET = SuitSet(PokerSuit.CONFIG_FILE)
    DECK = Deck(RANKSET, SUITSET)
