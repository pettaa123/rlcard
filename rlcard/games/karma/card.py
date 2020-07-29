class KarmaCard(object):

    info = {'type':  ['number', 'wild'],
            'trait': ['4', '5', '6', '7', '8', '9', 'J', 'Q', 'K', 'A', '2', '3', '10']
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
