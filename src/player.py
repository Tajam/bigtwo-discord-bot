import discord


class Player:
    def __init__(self, player_object):
        self.player_object = player_object
        self.cards = []

    def give_card(self, card):
        self.cards.append(card)
        self.cards.sort()

    def give_cards(self, cards):
        self.cards += cards
        self.cards.sort()

    def throw_cards(self, indexes):
        out, left = [], []
        for i, n in enumerate(self.cards):
            if i in indexes:
                out.append(n)
            else:
                left.append(n)
        self.cards = left
        return out

    def peek_cards(self, indexes):
        out = []
        for i, n in enumerate(self.cards):
            if i in indexes:
                out.append(n)
        return out

    def have_card(self, card):
        return card in self.cards

    def get_card_discord_format(self):
        return [f"{card.rank._name}{card.suit._name}" for card in self.cards]

