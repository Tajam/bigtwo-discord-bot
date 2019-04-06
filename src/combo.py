from card import Deck

#Not so generic class
class Combo():

    def __init__(self, card_list):
        self.card_list = card_list.sort()

    def _detect_combo(self):
        pass

    
