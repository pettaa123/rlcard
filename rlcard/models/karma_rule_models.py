''' Karma rule models
'''

import numpy as np
import random

import rlcard
from rlcard.models.model import Model
from rlcard.games.karma.card import KarmaCard

class KarmaRuleAgentV1(object):
    ''' Karma Rule agent version 1
    '''

    def __init__(self):
        self.use_raw = True
        #self.use_raw = False

    def step(self, state):
        ''' Predict the action given raw state. A naive rule. Choose the lowest value
            that appears in the hand from legal actions. Try to keep wild
            cards as long as it can.
            
            

        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''
        
        # choose card with lowest value in action list
        lowest_val=999
        
        if 'raw_legal_actions' in state:
            legal_actions = state['raw_legal_actions']
            state = state['raw_obs']
            
        else:
            legal_actions = state['legal_actions']
            state = state['obs']

        if 'draw' in legal_actions:
            return 'draw'
        
        if random.random() < 0.3:     
            return random.choice(legal_actions)
        
        #specialities
        sames=0
        target=''
        played_cards = state['played_cards']
        if played_cards:
            sames = played_cards.count(played_cards[-1])
            target = played_cards[-1]
        
        #lowest value
        for iter_action in legal_actions:
            val,count = iter_action.split(':')
            if val == target and int(count) + sames == 4:
                return iter_action
            else:
                val = KarmaCard.info['order'].index(str(iter_action))
                if val < lowest_val:
                    lowest_val = val
                    action = iter_action
            
        return action
                

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []

    @staticmethod
    def filter_wild(hand):
        ''' Filter the wild cards. If all are wild cards, we do not filter

        Args:
            hand (list): A list of Karma card string

        Returns:
            filtered_hand (list): A filtered list of Karma string
        '''
        filtered_hand = []
        for card in hand:
            if not card[2:6] == 'wild':
                filtered_hand.append(card)

        if len(filtered_hand) == 0:
            filtered_hand = hand

        return filtered_hand

    @staticmethod
    def count_colors(hand):
        ''' Count the number of cards in each color in hand

        Args:
            hand (list): A list of Karma card string

        Returns:
            color_nums (dict): The number cards of each color
        '''
        color_nums = {}
        for card in hand:
            color = card[0]
            if color not in color_nums:
                color_nums[color] = 0
            color_nums[color] += 1

        return color_nums

class KarmaRuleModelV1(Model):
    ''' Karma Rule Model version 1
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('karma')

        rule_agent = KarmaRuleAgentV1()
        self.rule_agents = [rule_agent for _ in range(env.player_num)]

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.rule_agents

    @property
    def use_raw(self):
        ''' Indicate whether use raw state and action

        Returns:
            use_raw (boolean): True if using raw state and action
        '''
        return True



