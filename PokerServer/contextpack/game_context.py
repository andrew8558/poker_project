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

    def build_context(self, game_state):
        """Build Game Context object on the base of a given Game State object.

        :param game_state: Game state object, provided by Game Center.
        :return: Returns Game Context object.
        """

        self.player_dict['me'] = None
        self.player_dict['opponent'] = None
        for player in game_state.players:
            if player.account.login == self.account.login:
                self.player_dict['me'] = player
            else:
                self.player_dict['opponent'] = player
                player.account.password = None
                player.account.money = None
                if game_state.stage != 'SHOWDOWN':
                    player.hand = '?? ??' if player.hand else None
        if game_state.stage == 'PREFLOP':
            game_state.board = ''
        elif game_state.stage == 'FLOP':
            game_state.board = ' '.join(game_state.board.split(' ')[:3])
        elif game_state.stage == 'TURN':
            game_state.board = ' '.join(game_state.board.split(' ')[:4])
        elif game_state.stage == 'RIVER' or game_state.stage == 'SHOWDOWN':
            game_state.board = game_state.board
        self.game_state = game_state

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
            ceil = min([player.bet + player.stack if player.bet else player.stack for player in self.player_dict.values()])
            return (bet == floor or 2 * floor <= bet <= ceil) and (bet == 0 or bet >= self.game_state.blind_size) and (25.0 - (cur - myself.time_st) > 0.0)

    def check_add_chips_form(self, chips):
        """Method for Add Chips form validation.

        :param chips: Chips value.
        :return: Returns True if the form is valid. Otherwise, returns False.
        """

        return self.account.money >= chips and 100 * self.game_state.blind_size >= self.player_dict['me'].stack + chips >= 40 * self.game_state.blind_size

    def encoded(self):
        """ Get JSON-encoded version of Game Context.

        :return: Returns JSON-encoded version of the object state.
        """

        enc_dict = {
            'name': self.name,
            'account': self.account.encoded(),
            'table_id': self.table_id,
            'player_dict': dict(zip(self.player_dict.keys(), tuple(
                map(lambda player: player.encoded() if player else None, self.player_dict.values())))),
            'game_state': self.game_state.encoded()
        }
        return enc_dict
