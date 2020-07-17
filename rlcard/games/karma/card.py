from termcolor import colored

class KarmaCard(object):

    info = {'type':  ['number', 'action', 'wild'],
            'trait': ['2', '3', '4', '5', '6', '7', '8', '9','10'
                      'J', 'Q', 'K', 'A']
            }

    def __init__(self, card_type, color, trait):
        ''' Initialize the class of KarmaCard

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


    @staticmethod
    def print_cards(cards):
        ''' Print out card in a nice form

        Args:
            card (str or list): The string form or a list of a Karma card
        '''
        if isinstance(cards, str):
            cards = [cards]
        for i, card in enumerate(cards):
            trait = card

            print(trait, end='')


            if i < len(cards) - 1:
                print(', ', end='')
