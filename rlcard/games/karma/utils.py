import os
import json
import numpy as np
from collections import OrderedDict

import rlcard

from rlcard.games.karma.card import KarmaCard as Card

# Read required docs
ROOT_PATH = rlcard.__path__[0]

# a map of abstract action to its index and a list of abstract action
with open(os.path.join(ROOT_PATH, 'games/karma/jsondata/action_space.json'), 'r') as file:
    ACTION_SPACE = json.load(file, object_pairs_hook=OrderedDict)
    ACTION_LIST = list(ACTION_SPACE.keys())

# a map of color to its index
# COLOR_MAP = {'d': 0, 'h': 1, 's': 2, 'c': 3} #diamonds,hearts,spades,clubs

COUNT_MAP = {'1': 0, '2': 1, '3': 2}  # one, two or three cards of a trait

# a map of trait to its index
TRAIT_MAP = {'4': 0, '5': 1, '6': 2, '7': 3, '8': 4, '9': 5, 'J': 6, 'Q': 7,
             'K': 8, 'A': 9, '2': 10, '3': 11, '10': 12}

WILD = ['2', '3', '10']


# WILD_DRAW_4 = ['r-wild_draw_4', 'g-wild_draw_4', 'b-wild_draw_4', 'y-wild_draw_4']


def init_deck():
    ''' Generate karma deck of 52 cards
    '''
    deck = []
    card_info = Card.info
    for i in range(4):

        # init number cards
        for num in card_info['trait'][:10]:
            deck.append(Card('number', num))

        # init wild cards
        for action in card_info['trait'][10:13]:
            deck.append(Card('wild', action))

    return deck


def cards2list(cards):
    ''' Get the corresponding string representation of cards

    Args:
        cards (list): list of KarmaCards objects

    Returns:
        (string): string representation of cards
    '''
    cards_list = []
    for card in cards:
        cards_list.append(card.get_str())
    return cards_list


def get_cards_dict(cards):
    ''' Get the corresponding dict representation of cards

    Args:
        cards (list): list of string of cards

    Returns:
        (dict): dict of cards
    '''

    cards_dict = {}
    if cards:
        for card in cards:
            if card not in cards_dict:
                cards_dict[card] = 1
            else:
                cards_dict[card] += 1
    return cards_dict


def encode_hand(plane, hand):
    ''' Encode hand and represerve it into plane

    Args:
        plane (array): 4*13 numpy array
        hand (list): list of string of hand's card

    Returns:
        (array): 4*13 numpy array
    '''

    # 1 card,2 cards ,3 cards, 4 cards

    hand_ = get_cards_dict(hand)
    for card, count in hand_.items():
        card_info = card
        trait = TRAIT_MAP[card_info]
        plane[count - 1][trait] = 1
    return plane


def encode_target(plane, target):
    ''' Encode target and represerve it into plane

    Args:
        plane (array): 4*13 numpy array
        target(str): string of target card

    Returns:
        (array): 4*13 numpy array 
    '''

    target = get_cards_dict(target)

    for card, count in target.items():
        card_info = card
        # color = COLOR_MAP[card_info[0]]
        trait = TRAIT_MAP[card_info]
        plane[count - 1][trait] = 1
    return plane
