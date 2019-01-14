class Card:
    #Note: Zero value represent NULL
    S_RANKING = {1:4,2:3,3:2,4:1}
    S_NAME = {1:'Spade',2:'Heart',3:'Club',4:'Diamond'}
    V_RANKING = dict()
    for n in range(1,14):
        V_RANKING[n] = n

    @classmethod
    def offset_gen(cls, val = 13):
        count = 0
        number = val + 1
        if val > 13:
            val = 1
        while(count < 13):
            count += 1
            yield number
            number += 1
            if number > 13:
                number = 1

    @classmethod
    def set_bossval(cls ,val = 13):
        cls.V_RANKING = dict()
        new_gen = cls.offset_gen(val)
        for n in range(1,14):
            cls.V_RANKING[new_gen.__next__()] = n
        #print(cls.V_RANKING)
    
    @staticmethod
    def largest_card(cards):
        largest = cards[0]
        for n in cards:
            if Card.fight_against(n, largest):
                largest = n
        return n

    @staticmethod
    def sort_card(cards, byrank = True):
        sort_done = False
        while(not sort_done):
            sort_done = True
            for n in range(len(cards)-1):
                if byrank:
                    if Card.fight_against(cards[n],cards[n+1]):
                        sort_done = False
                        cards[n],cards[n+1] = cards[n+1],cards[n]
                else:
                    if cards[n].value > cards[n+1].value:
                        sort_done = False
                        cards[n],cards[n+1] = cards[n+1],cards[n]
            

    def cards_value_sum(cards):
        val = 0
        for n in cards:
            val += n.value
        #print(len(cards),val)
        return val

    @classmethod
    def fight_against(cls ,you, opponent, pattern = False):
        value_res = 0
        symbl_res = 0
        
        if cls.V_RANKING[you.value] > cls.V_RANKING[opponent.value]:
            value_res = 1
        elif cls.V_RANKING[you.value] < cls.V_RANKING[opponent.value]:
            value_res = -1
        else:
            value_res = 0
            
        if cls.S_RANKING[you.symbol] > cls.S_RANKING[opponent.symbol]:
            symbl_res = 1
        elif cls.S_RANKING[you.symbol] < cls.S_RANKING[opponent.symbol]:
            symbl_res = -1
        else:
            symbl_res = 0

        if pattern:
            symbl_res *= 2
        else:
            value_res *= 2

        return (value_res+symbl_res > 0)
    
    def __init__(self, value):
        self.symbol = int(value/13) + 1
        self.value = value % 13 + 1

class Skill:
    type_name = dict()
    type_name[1] = 'Single'
    type_name[2] = 'Pair'
    type_name[3] = 'Set'
    type_name[5] = 'skill'

    @staticmethod
    def check_same(cards):
        if len(cards) == 1:
            return True
        check_num = Card.cards_value_sum(cards)/cards[0].value
        #print(check_num, cards[0].value)
        if check_num == len(cards):
            return True
        else:
            print('Check same invalid!')
            return False
            
    @staticmethod
    def check_skill(cards):
        IsFlush = True
        IsStraight = True
        Card.sort_card(cards, False)
        return_list = list()
        conser_list = list()
        symbol_list = list()
        combin_dict = dict()
        last_val = 0
        leader_card = Card.largest_card(cards)
        temp_list = list()
        #======Ranking======#
        #Straight:          1
        #Flush:             2
        #Full House:        3
        #Four of a Kind:    4
        #Straight Flush:    5
        for n in cards:
            #Consecutive-ness of cards
            if last_val == 0:
                last_val = n.value
            if last_val == n.value:
                temp_list.append(n.value)
                last_val += 1
            else:
                conser_list.append(list(temp_list))
                temp_list = list()
                temp_list.append(n.value)
                last_val = n.value + 1
            #Symbols of cards
            if not n.symbol in symbol_list:
                symbol_list.append(n.symbol)
            #Combination of cards
            if n.value in combin_dict:
                combin_dict[n.value].append(n)
            else:
                combin_dict[n.value] = [n]
        #Check if Straight
        if (len(temp_list) > 0):
            conser_list.append(list(temp_list))
            temp_list = list()
        if (len(conser_list) > 2):
            IsStraight = False
            print('Not Straight', end=',')
        elif len(conser_list) == 2:
            if (min(conser_list[0]) != 1)|(max(conser_list[1]) != 13):
                IsStraight = False
                print('Not Straight', end=',')
        #Check if Flush
        if len(symbol_list) > 1:
            IsFlush = False
            print('Not Flush', end=',')
        #Either Full House or Four of a Kind
        if not (IsFlush|IsStraight):
            if len(combin_dict) <= 2:
                leader_val = 0
                number_val = 0
                for n in combin_dict:
                    if len(combin_dict[n]) > number_val:
                        leader_val = n
                        number_val = len(combin_dict[n])
                leader_card = Card.largest_card(combin_dict[leader_val])
                return_list = [True, leader_card, number_val]
            else:
                return_list = [False, leader_card, 0]
                print('Not FH or FoaK', end=',')
        #Or it is a Straight Flush
        elif (IsFlush&IsStraight):
            return_list = [True, leader_card, 5]
        elif IsStraight:
            return_list = [True, leader_card, 1]
        elif IsFlush:
            return_list = [True, leader_card, 2]
        print(leader_card.value, end=',')
        print(Card.S_NAME[leader_card.symbol])
        return return_list
    
    def __init__(self, cards):
        length = len(cards)
        if length in Skill.type_name:
            self.type = Skill.type_name[length]
            if length != 5:
                self.valid = Skill.check_same(cards)
                self.leader = Card.largest_card(cards)
            else:
                self.valid, self.leader, self.srank = Skill.check_skill(cards)
        else:
            self.valid = False
        

if __name__ == '__main__':
    pass
