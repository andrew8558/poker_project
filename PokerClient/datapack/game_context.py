import datapack.account
import datapack.game_state
import time


class GameContext:
    """Data object describing all important parameters of the Game Context"""

    def __init__(self, account, table_id):
        """Construct Game Context object

        :param account: Account, associated with user.
        :param table_id: Room id.
        """
        self.name = 'GAME'
        self.account = account
        self.table_id = table_id
        self.player_dict = {'me': None, 'opponent': None}
        self.game_state = None

    def check_fold_form(self):
        """Method for Fold form validation.

        :return: Returns True if the form is valid. Otherwise, returns False.
        """
        return self.game_state.stage != 'WAITING' and self.game_state.stage != 'SHOWDOWN'

    def check_bet_form(self, bet):
        """Method for Bet form validation.

        :param bet: Bet value.
        :return: Returns True if the form is valid. Otherwise, returns False.
        """
        if self.game_state.stage != 'WAITING' and self.game_state.stage != 'SHOWDOWN':
            cur = time.time()
            myself = self.player_dict['me']
            floor = self.player_dict['opponent'].bet if self.player_dict['opponent'].bet else 0
            ceil = min(
                [player.bet + player.stack if player.bet else player.stack for player in self.player_dict.values()])
            return (bet == floor or 2 * floor <= bet <= ceil) and (bet == 0 or bet >= self.game_state.blind_size) and (
                        25.0 - (cur - myself.time_st) > 0.0)

    def check_add_chips_form(self, chips):
        """Method for Add Chips form validation.

        :param chips: Chips value.
        :return: Returns True if the form is valid. Otherwise, returns False.
        """
        return self.account.money >= chips and 100 * self.game_state.blind_size >= self.player_dict['me'].stack + chips >= 40 * self.game_state.blind_size

    @staticmethod
    def decoded(enc_dict):
        """Decode JSON-formatted dictionary of an object and return corresponding Context object."""
        account = datapack.account.Account.decoded(enc_dict['account'])
        table_id = enc_dict['table_id']
        player_dict = dict(zip(enc_dict['player_dict'].keys(), tuple(map(lambda p_d: datapack.game_state.GameState.Player.decoded(p_d) if p_d else None, enc_dict['player_dict'].values()))))
        game_state = datapack.game_state.GameState.decoded(enc_dict['game_state'])

        dec_obj = GameContext(account, table_id)
        dec_obj.player_dict = player_dict
        dec_obj.game_state = game_state
        return dec_obj
