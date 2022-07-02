from datapack.account import Account

class GameState:
    class Player:
        def __init__(self, account, bank, ready=False, hand=None, dealer=False, time_st=None, bet=None, able=True):
            self.account = account
            self.stack = bank
            self.ready = ready
            self.hand = hand
            self.dealer = dealer
            self.time_st = time_st
            self.bet = bet
            self.able = able

        @staticmethod
        def decoded(enc_dict):
            if enc_dict:
                return GameState.Player(Account.decoded(enc_dict['account']),
                                        enc_dict['stack'],
                                        enc_dict['ready'],
                                        enc_dict['hand'],
                                        enc_dict['dealer'],
                                        enc_dict['time_st'],
                                        enc_dict['bet'],
                                        enc_dict['able'])
            else:
                return None

    def __init__(self,
                 blind_size=None,
                 stage='WAITING',
                 players=None,
                 time_ready_st=None,
                 time_showdown=None,
                 ready_players=0,
                 board=None,
                 dealer=None,
                 not_dealer=None,
                 pot=0):
        self.blind_size = blind_size
        self.stage = stage
        self.players = []
        self.time_ready_st = time_ready_st
        self.time_showdown = time_showdown
        self.ready_players = ready_players
        self.board = board
        self.dealer = dealer
        self.not_dealer = not_dealer
        self.pot = pot

    @staticmethod
    def decoded(enc_dict):
        return GameState(enc_dict['blind_size'],
                         enc_dict['stage'],
                         list(map(lambda player_enc_dict: GameState.Player.decoded(player_enc_dict),
                                  enc_dict['players'])),
                         enc_dict['time_ready_st'],
                         enc_dict['time_showdown'],
                         enc_dict['ready_players'],
                         enc_dict['board'],
                         GameState.Player.decoded(enc_dict['dealer']),
                         GameState.Player.decoded(enc_dict['not_dealer']),
                         enc_dict['pot'])
