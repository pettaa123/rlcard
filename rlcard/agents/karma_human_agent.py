from rlcard.games.karma.card import KarmaCard

class HumanAgent(object):
    ''' A human agent for Karma. It can be used to play against trained models
    '''

    def __init__(self, action_num):
        ''' Initilize the human agent

        Args:
            action_num (int): the size of the ouput action space
        '''
        self.use_raw = True
        self.action_num = action_num

    @staticmethod
    def step(state):
        ''' Human agent will display the state and make decisions through interfaces

        Args:
            state (dict): A dictionary that represents the current state

        Returns:
            action (int): The action decided by human
        '''
        print(state['raw_obs'])
        _print_state(state['raw_obs'], state['action_record'])
        action = int(input('>> You choose action (integer): '))
        while action < 0 or action >= len(state['legal_actions']):
            print('Action illegel...')
            action = int(input('>> Re-choose action (integer): '))
        return state['raw_legal_actions'][action]

    def eval_step(self, state):
        ''' Predict the action given the curent state for evaluation. The same to step here.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        return self.step(state), []

def _print_state(state, action_record):
    ''' Print out the state of a given player

    Args:
        player (int): Player id
    '''
    _action_list = []
    for i in range(1, len(action_record)+1):
        if action_record[-i][0] == state['current_player']:
            break
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print('>> Player', pair[0], 'chooses ', end='')
        _print_action(pair[1])
        print('')
    print('\n=============== Others Hand ===============')
    KarmaCard.print_cards(state['others_hand'])
    print('\n=============== Your Hand ===============')
    KarmaCard.print_cards(state['hand'])
    print('\n=============== Your China ===============')
    KarmaCard.print_cards(state['china'])
    print('\n=============== Others China ===============')
    KarmaCard.print_cards(state['others_china'])
    print('\n========= China Hidden remaining =========')
    print(len(state['china_hidden']))
    print('============== Played Cards ==============')
    KarmaCard.print_cards(state['played_cards'])
    print('')
    print('========== Players Card Number ===========')
    # for i in range(state['player_num']):
    #     if i != state['current_player']:
    #         print('Player {} has {} cards.'.format(i, state['card_num'][i]))
            
    print('======== Actions You Can Choose =========')
    for i, action in enumerate(state['legal_actions']):
        print(str(i)+': ', end='')
        KarmaCard.print_cards(action)
        if i < len(state['legal_actions']) - 1:
            print(', ', end='')
    print('\n')

def _print_action(action):
    ''' Print out an action in a nice form

    Args:
        action (str): A string a action
    '''
    KarmaCard.print_cards(action)
