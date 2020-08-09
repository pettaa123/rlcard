from rlcard.games.karma.card import KarmaCard
from rlcard.games.karma.utils import cards2list, WILD


class KarmaRound(object):

    def __init__(self, dealer, num_players, np_random):
        ''' Initialize the round class

        Args:
            dealer (object): the object of UnoDealer
            num_players (int): the number of players in game
        '''
        self.np_random = np_random
        self.dealer = dealer
        self.target = ''
        self.current_player = 0
        self.num_players = num_players
        self.direction = 1
        self.played_cards = []
        self.removed_cards = []
        self.is_over = False
        self.winner = None
        
        self.skipped = False

    def flip_top_card(self):
        ''' Flip the top card of the card pile

        Returns:
            (object of KarmaCard): the top card in game

        '''
        top = self.dealer.flip_top_card()
        self.target = top 
        self.played_cards.append(top)
        
    def _draw_played_cards(self, players):
        #add knowledge about who has cards in which cards in his hand
         
        players[self.current_player].hand.extend(self.played_cards)
        self.played_cards.clear()
        self.target = ''
        
        self.current_player = (self.current_player + self.direction) % self.num_players


    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            player (object): object of UnoPlayer
            action (str): string of legal action
        '''
        if action == 'draw:1':
            #self._perform_draw_action(players)
            self._draw_played_cards(players)
            return None
        player = players[self.current_player]
        #card_info = action.split('-')
        action_info = action.split(':')
        #number_of_cards_to_play = card_info[1]
        #card_info=action
        trait = action_info[0]
        # remove corresponding card
        #remove_index = None
        #if trait == 'wild' or trait == 'wild_draw_4':
            
        number = 0
        
            
        while number < int(action_info[1]):
            
            number += 1
            
            if player.china_hidden_accessible:                      
                for card in player.china_hidden:
                    if trait == card.trait:
                        player.china_hidden.remove(card)
                        break
                           
            elif player.china_accessible:
                for card in player.china:
                    if trait == card.trait:
                        player.china.remove(card)
                        break
                                              
            else: 
                for card in player.hand:
                    if trait == card.trait:
                        player.hand.remove(card)
                        break
                        
            self.played_cards.append(card)
        
        self._refill_hand(players)
              
            
        if not player.hand and not player.china_hidden:
            self.is_over = True
            self.winner = [self.current_player]
        #last 4 played cards
        sum = 1
        for p in self.played_cards[-4:]:
            if p.trait == self.played_cards[-1]:
                sum += 1
        if sum == 4:
            self._perform_four_sames(players)
            
        #if sum([1 for p in self.played_cards[-4:] if p.trait == '2']) == 4:
        #    self._perform_four_sames(players)


        # perform the non special or wild action
        elif (trait != '8' or self.skipped) and trait != '10':
            self.skipped = False
            #next player_id
            self.current_player = (self.current_player + self.direction) % self.num_players
            if trait != '3':
                self.target = self.played_cards[-1]
            

        # perform non-number action
        else:
            self._perform_non_number_action(players, self.played_cards[-1]) #non number is 8 and 10
                
            
    def check_accesibility(self, player):
        if len(player.hand) > 0:
            player.china_hidden_accessible = False
            player.china_accessible = False
        elif len(player.hand) == 0 and len(player.china) > 0:
            player.china_accessible = True
            player.china_hidden_accessible = False
        elif len(player.hand) == 0 and len(player.china) == 0 and len(player.china_hidden):
            player.china_hidden_accessible = True
            player.china_accessible = False
            
    def get_legal_actions_dict(self, cards):
        ''' Get the corresponding dict representation of cards
        
        Args:
            cards (list): list of string of cards

        Returns:
            (dict): dict of cards
        '''

        cards_dict = {}
        if cards:
            for card in cards:
                if card.str not in cards_dict:
                    cards_dict[card.str] = 1
                else:
                    cards_dict[card.str] += 1
        return cards_dict
    
    def get_legal_actions_list(self, actions_dict):
        ''' Get the corresponding list representation of legal actions
        
        Args:
            cards (list): list of string of cards

        Returns:
            (dict): dict of cards
        '''
        
        actions_list = []
        for action, count in actions_dict.items():
            i=1
            while i <= count:
                actions_list.append(str(action) + ":" + str(i))
                i += 1
                                
        return actions_list

    def get_legal_actions(self, players, player_id):
        legal_actions_dict = {}
        
        target = self.target
        
        #moves accessible cards into hand
        self.check_accesibility(players[player_id])
        
        hand = players[player_id].hand
        
        if players[player_id].china_accessible == True:
            hand = players[player_id].china
            
        #if china hidden accessible, one chooses first and checks if it is feasable   
        if players[player_id].china_hidden_accessible == True and players[player_id].china_hidden:
            legal_actions_dict = {}
            legal_actions_dict[players[player_id].china_hidden[0].str] = 1
            lists = self.get_legal_actions_list(legal_actions_dict)
            lists.append('draw:1')
            return lists

        #target is None
        if not target:
            legal_actions_dict = self.get_legal_actions_dict(hand)
            lists =  self.get_legal_actions_list(self.get_legal_actions_dict(hand))
            lists.append('draw:1')
            return lists
                                

        for card in hand:
            #2,3,10 are wilds
            if card.type == 'wild':
                if card.str not in legal_actions_dict:
                    legal_actions_dict[card.str] = 1
                else:
                    legal_actions_dict[card.str] += 1
                    
            elif target.get_index() == KarmaCard.info['trait'].index('2'): # one can act every card on twos
                if card.str not in legal_actions_dict:
                    legal_actions_dict[card.str] = 1
                else:
                    legal_actions_dict[card.str] += 1
            # one can act every card on threes if it is first played card
            elif target.get_index() == KarmaCard.info['trait'].index('3'): 
                    if card.str not in legal_actions_dict:
                        legal_actions_dict[card.str] = 1
                    else:
                        legal_actions_dict[card.str] += 1     

                    
            elif target.get_index() == KarmaCard.info['trait'].index('7'): #value 7 -> lower
                if card.get_index() <= target.get_index():
                    if card.str not in legal_actions_dict:
                        legal_actions_dict[card.str] = 1
                    else:
                        legal_actions_dict[card.str] += 1

                    
            elif card.get_index() >= target.get_index():
                if card.str not in legal_actions_dict:
                    legal_actions_dict[card.str] = 1
                else:
                    legal_actions_dict[card.str] += 1
                
        # if not legal_actions_dict:
        #     return ['draw']
                

        lists = self.get_legal_actions_list(legal_actions_dict)
        lists.append('draw:1')
        return lists

                

    def get_state(self, players, player_id):
        ''' Get player's state

        Args:
            players (list): The list of KarmaPlayer
            player_id (int): The id of the player
        '''
        state = {}
        player = players[player_id]
        state['hand'] = cards2list(player.hand)
        state['china'] = cards2list(player.china)
        state['china_hidden'] = cards2list(player.china_hidden)
        state['target'] = self.target.str if self.target != '' else '' 
        state['played_cards'] = cards2list(self.played_cards)
        state['removed_cards'] = cards2list(self.removed_cards)
        
        others_hand = []
        others_china = []
        #others_china_accessible = False
        others_china_hidden = []
        for player in players:
            if player.player_id != player_id:
                others_hand.extend(player.hand)
                others_china.extend(player.china)
                others_china_hidden.extend(player.china_hidden)
                
        state['others_hand'] = cards2list(others_hand)
        state['others_china'] = cards2list(others_china)
        state['others_china_hidden'] = cards2list(others_china_hidden)
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        #state['card_num'] = []
        state['deck'] = str(len(self.dealer.deck))
        #for player in players:
        #    state['card_num'].append(len(player.hand)+len(player.china)+len(player.china_hidden))
        return state

    def replace_deck(self):
        ''' Add cards have been played to deck
        '''
        self.dealer.deck.extend(self.played_cards)
        self.dealer.shuffle()
        self.played_cards = []

        
    def _refill_hand(self, players):
        while len(players[self.current_player].hand) < 3 and self.dealer.deck:
            card = self.dealer.deck.pop()
            players[self.current_player].hand.append(card)
    
    def _perform_four_sames(self,players):
        
        self.removed_cards.extend(self.played_cards)
        self.played_cards.clear()
        self.target = ''

    def _perform_non_number_action(self, players, card):

        # perform reverse card
        #if card.trait == 'reverse':
        #    self.direction = -1 * direction

        # perform skip card
        if card.trait == '8':
            self.skipped = True
            self.target = card
            
        # perform wild-10 card
        elif card.trait == '10':
            self.removed_cards.extend(self.played_cards)
            self.played_cards.clear()
            self.target = ''
            #current = current

