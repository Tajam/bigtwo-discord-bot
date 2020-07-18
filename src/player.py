import discord


class Player:
    def __init__(self, player_object):
        self.player_object = player_object
        self.player_hand_messages = []
        self.player_status_message = None
        self.player_board_messages = []
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

    # Sort player's cards, s = suit, n = numbers 
    def sort_cards(self, sort='n'):
        if sort.startswith("s"):
            self.cards = sorted(self.cards, key=sort_by_suit)
        else:
            self.cards.sort()

# Sort by suit, function used in player's sort_cards method
def sort_by_suit(card):
    return card.suit
