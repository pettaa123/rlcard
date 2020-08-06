class KarmaCard(object):

    info = {'type':  ['number', 'wild'],
            'trait': ['4', '5', '6', '7', '8', '9', 'J', 'Q', 'K', 'A', '2', '3', '10', 'draw'],
            'order': ['4:4', '4:3', '4:2', '4:1', '5:4', '5:3', '5:2', '5:1', '6:4', '6:3', '6:2', '6:1',
                      '7:4', '7:3', '7:2', '7:1', '8:4', '8:3', '8:2', '8:1', '9:4', '9:3', '9:2', '9:1',
                      'J:4', 'J:3', 'J:2', 'J:1', 'Q:4', 'Q:3', 'Q:2', 'Q:1', 'K:1', 'K:2', 'K:3', 'K:4',
                      'A:1', 'A:2', 'A:3', 'A:4', '2:1', '2:2', '2:3', '2:4', '3:1', '3:2', '3:3', '3:4',
                      '10:1', '10:2', '10:3', '10:4', 'draw:1'],
            'order_start': ['4:4', '4:3', '4:2', '4:1', '5:4', '5:3', '5:2', '5:1', '6:4', '6:3', '6:2', '6:1',
                      '7:4', '7:3', '7:2', '7:1', '8:4', '8:3', '8:2', '8:1', '9:4', '9:3', '9:2', '9:1',
                      'J:1', 'J:2', 'J:3', 'J:4', 'Q:1', 'Q:2', 'Q:3', 'Q:4', 'K:1', 'K:2', 'K:3', 'K:4',
                      'A:1', 'A:2', 'A:3', 'A:4', '2:1', '2:2', '2:3', '2:4', '3:1', '3:2', '3:3', '3:4',
                      '10:1', '10:2', '10:3', '10:4', 'draw:1']
                      }

    def __init__(self, card_type, trait):
        ''' Initialize the class of UnoCard

        Args:
            card_type (str): The type of card
            trait (str): The trait of card
        '''
        
        self.type = card_type
        self.trait = trait
        self.str = self.get_str()

    def get_str(self):
        ''' Get the string representation of card

        Return:
            (str): The string of card's trait
        '''
        return self.trait
    
    def get_index(self):
        ''' Get the index of trait

        Return:
            (int): The index of card's trait (value)
        '''


        return self.info['trait'].index(self.trait)
        


    @staticmethod
    def print_cards(cards):
        ''' Print out card in a nice form

        Args:
            card (str or list): The string form or a list of a Karma card
        '''
        if isinstance(cards, str):
            cards = [cards]
        for i, card in enumerate(cards):
            print(card, end='')
                            
            if i < len(cards) - 1:
                print(', ', end='')
