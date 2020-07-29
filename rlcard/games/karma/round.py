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
        self.target = []
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
        # if top.trait == 'wild':
        #     top.color = self.np_random.choice(UnoCard.info['color'])
        self.target.append(top)
        self.played_cards.append(top)


    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            player (object): object of UnoPlayer
            action (str): string of legal action
        '''
        if action == 'draw':
            #self._perform_draw_action(players)
            self._draw_played_cards(players)
            return None
        player = players[self.current_player]
        #card_info = action.split('-')
        #number_of_cards_to_play = card_info[1]
        card_info=action
        trait = card_info
        # remove corresponding card
        remove_index = None
        #if trait == 'wild' or trait == 'wild_draw_4':
            
        if player.china_hidden_accessible:
            for index, card in enumerate(player.china_hidden):
                if trait == card.trait:
                    remove_index = index
                    break

            card = player.china_hidden.pop(remove_index)
            
        elif player.china_accessible:
            for index, card in enumerate(player.china):
                if trait == card.trait:
                    remove_index = index
                    break

            card = player.china.pop(remove_index)            
                       
        else: 
            for index, card in enumerate(player.hand):
                if trait == card.trait:
                    remove_index = index
                    break

            card = player.hand.pop(remove_index)           
            
        self.played_cards.append(card)
        
        self._refill_hand(players)
        
        if not player.hand and not player.china_hidden:
            self.is_over = True
            self.winner = [self.current_player]


        # perform the non special or wild action
        if (card.trait != '8' or self.skipped) and card.trait != '10':
            self.skipped = False
            self.current_player = (self.current_player + self.direction) % self.num_players
            if card.trait != '3':
                self.target.clear()
                self.target.append(card)
            

        # perform non-number action
        else:
            self._perform_non_number_action(players, card) #non number is 8 and 10
            
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

    def get_legal_actions(self, players, player_id):
        #wild_flag = 0
        #wild_draw_4_flag = 0
        legal_actions = []
        #wild_4_actions = []
        
        target = self.target
        
        #moves accessible cards into hand
        self.check_accesibility(players[player_id])
        
        hand = players[player_id].hand
        
        if players[player_id].china_accessible == True:
            hand = players[player_id].china
            
        #if china hidden accessible one chooses first and checks if it is feasable   
        if players[player_id].china_hidden_accessible == True and players[player_id].china_hidden:
            legal_actions.append(players[player_id].china_hidden[0].str)
            return legal_actions
            


        #target is None
        if not target:
            for card in hand:
                legal_actions.append(card.str)
            return legal_actions
                                

        for card in hand:
            #2,3,10 are wilds
            if card.type == 'wild':
                legal_actions.append(card.str)
                    
            elif target[0].get_index() == KarmaCard.info['trait'].index('2'): # one can act every card on twos
                legal_actions.append(card.str)
            # one can act every card on threes if it is first played card
            elif target[0].get_index() == KarmaCard.info['trait'].index('3'): 
                legal_actions.append(card.str)          

                    
            elif target[0].get_index() == KarmaCard.info['trait'].index('7'): #value 7 -> lower
                if card.get_index() <= target[0].get_index():
                    legal_actions.append(card.str)

                    
            elif card.get_index() >= target[0].get_index():
                legal_actions.append(card.str)
                
        if not legal_actions:
            legal_actions = ['draw']
                

        return legal_actions
                
            
        
        # target is aciton card or number card
        
        
        # #if target.type == 'wild':
        # for card in hand:
        #     if card.type == 'wild':
        #         if card.trait == 'wild_draw_4':
        #             if wild_draw_4_flag == 0:
        #                 wild_draw_4_flag = 1
        #                 wild_4_actions.extend(WILD_DRAW_4)
        #         else:
        #             if wild_flag == 0:
        #                 wild_flag = 1
        #                 legal_actions.extend(WILD)
        #     elif card.color == target.color:
        #         legal_actions.append(card.str)

        # target is aciton card or number card
        #else:
        # for card in hand:
        #     if card.type == 'wild':
        #         if card.trait == 'wild_draw_4':
        #             if wild_draw_4_flag == 0:
        #                 wild_draw_4_flag = 1
        #                 wild_4_actions.extend(WILD_DRAW_4)
        #         else:
        #             if wild_flag == 0:
        #                 wild_flag = 1
        #                 legal_actions.extend(WILD)
        #     elif card.color == target.color or card.trait == target.trait:
        #         legal_actions.append(card.str)
        # if not legal_actions:
        #     legal_actions = wild_4_actions
        # if not legal_actions:
        #     legal_actions = ['draw']
        # return legal_actions

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
        state['target'] = cards2list(self.target)
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
        state['card_num'] = []
        for player in players:
            state['card_num'].append(len(player.hand)+len(player.china)+len(player.china_hidden))
        return state

    def replace_deck(self):
        ''' Add cards have been played to deck
        '''
        self.dealer.deck.extend(self.played_cards)
        self.dealer.shuffle()
        self.played_cards = []

    def _draw_played_cards(self, players):
        #add knowledge about who has cards in which cards in his hand
         
        players[self.current_player].hand.extend(self.played_cards)
        self.played_cards.clear()
        self.target.clear()
        
        self.current_player = (self.current_player + self.direction) % self.num_players
        
    def _refill_hand(self, players):
        while len(players[self.current_player].hand) < 3 and self.dealer.deck:
            card = self.dealer.deck.pop()
            players[self.current_player].hand.append(card)


    def _perform_non_number_action(self, players, card):
        current = self.current_player
        direction = self.direction
        num_players = self.num_players

        # perform reverse card
        #if card.trait == 'reverse':
        #    self.direction = -1 * direction

        # perform skip card
        if card.trait == '8':
            current = (current + direction) % num_players
            self.skipped = True
            self.target.clear()
            self.target.append(card)
            
        # perform wild-10 card
        elif card.trait == '10':
            self.removed_cards.extend(self.played_cards)
            self.played_cards.clear()
            self.target.clear()
            #current = current
            '''
        # perform draw_2 card
        elif card.trait == 'draw_2':
            if len(self.dealer.deck) < 2:
                self.replace_deck()
                #self.is_over = True
                #self.winner = UnoJudger.judge_winner(players)
                #return None
            self.dealer.deal_cards(players[(current + direction) % num_players], 2)
            current = (current + direction) % num_players

        # perform wild_draw_4 card
        elif card.trait == 'wild_draw_4':
            if len(self.dealer.deck) < 4:
                self.replace_deck()
                #self.is_over = True
                #self.winner = UnoJudger.judge_winner(players)
                #return None
            self.dealer.deal_cards(players[(current + direction) % num_players], 4)
            current = (current + direction) % num_players
        self.current_player = (current + self.direction) % num_players
        self.target = card
        '''
