class Player():

    def __init__(self, player_name):
        self.player_name = player_name
        self._cards = []

    def give_card(self, card):
        self._cards.append(card)
        self._cards.sort()
    
    def give_cards(self, cards):
        self._cards = sorted(cards)

    def throw_cards(self, indexes):
        out, left = [], []
        for i, n in enumerate(self._cards):
            if i in indexes:
                out.append(n)
            else:
                left.append(n)
        self._cards = left
        return out

    def have_card(self, card):
        return card in self._cards
