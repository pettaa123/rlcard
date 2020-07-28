
from rlcard.games.karma.utils import init_deck


class KarmaDealer(object):
    ''' Initialize a karma dealer class
    '''
    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_deck()
        self.shuffle()

    def shuffle(self):
        ''' Shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_cards(self, player, num):
        ''' Deal some cards from deck to one player

        Args:
            player (object): The object of DoudizhuPlayer
            num (int): The number of cards to be dealed
        '''
        for _ in range(num):
            player.hand.append(self.deck.pop())
            player.china.append(self.deck.pop())
            player.china_hidden.append(self.deck.pop())
            player.china_hidden[-1].hidden = True
            

    def flip_top_card(self):
        ''' Flip top card when a new game starts

        Returns:
            (object): The object of KarmaCard at the top of the deck
        '''
        
        #game always starts with a 4. TODO: Let the player begin with most fours.
        
        index_of_four = 0
        
        for idx,entry in enumerate(self.deck):
            if entry.str == '4':
                index_of_four = idx
                break
        
        top_card = self.deck.pop(index_of_four)
        
        return top_card
