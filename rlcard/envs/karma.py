import numpy as np

from rlcard.envs import Env
from rlcard.games.karma import Game
from rlcard.games.karma.utils import encode_cards, encode_target
from rlcard.games.karma.utils import ACTION_SPACE, ACTION_LIST
from rlcard.games.karma.utils import cards2list


class KarmaEnv(Env):

    def __init__(self, config):
        self.name = 'karma'
        self.game = Game()
        super().__init__(config)
        self.state_shape = [7, 4, 13]

    def _load_model(self):
        ''' Load pretrained/rule model

        Returns:
            model (Model): A Model object
        '''
        from rlcard import models
        return models.load('karma-rule-v1')

    def _extract_state(self, state):
        obs = np.zeros((7, 4, 13), dtype=int)
        encode_cards(obs[0], state['hand'])
        encode_cards(obs[1], state['china'])
        encode_target(obs[2], state['target'])
        encode_cards(obs[3], state['others_hand'])
        encode_cards(obs[4], state['others_china'])
        encode_cards(obs[5], state['played_cards'])
        encode_cards(obs[6], state['removed_cards'])
        legal_action_id = self._get_legal_actions()
        extracted_state = {'obs': obs, 'legal_actions': legal_action_id}
        if self.allow_raw_data:
            extracted_state['raw_obs'] = state
            extracted_state['raw_legal_actions'] = [
                a for a in state['legal_actions']]
        if self.record_action:
            extracted_state['action_record'] = self.action_recorder
        # print('HAND ')
        # print(state['hand'])
        # print('OTHER_HAND ')
        # print(state['others_hand'])
        # print('LEGAL ACRTIONS ')
        # print(extracted_state['raw_legal_actions'])
        # print('PLAYED CARDS ')
        # print(state['played_cards'])
        # print('-----------')

        
        return extracted_state

    def get_payoffs(self):

        return np.array(self.game.get_payoffs())

    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        if action_id in legal_ids:
            return ACTION_LIST[action_id]
        # if (len(self.game.dealer.deck) + len(self.game.round.played_cards)) > 17:
        #    return ACTION_LIST[60]
        return ACTION_LIST[np.random.choice(legal_ids)]

    def _get_legal_actions(self):
        legal_actions = self.game.get_legal_actions()
        legal_ids = [ACTION_SPACE[action] for action in legal_actions]
        return legal_ids

    def get_perfect_information(self):
        ''' Get the perfect information of the current state

        Returns:
            (dict): A dictionary of all the perfect information of the current state
        '''
        state = {}
        state['player_num'] = self.game.get_player_num()
        state['hand_cards'] = [cards2list(player.hand)
                               for player in self.game.players]
        #add china cards
        #add china accessible
        state['played_cards'] = cards2list(self.game.round.played_cards)
        state['target'] = self.game.round.target.str
        state['current_player'] = self.game.round.current_player
        state['legal_actions'] = self.game.round.get_legal_actions(
            self.game.players, state['current_player'])
        return state
