import queue
import time
import copy
import random
import centerspack.find_combination


class GameState:
    """Used to store information about game state"""
    class Player:
        """Used to store information about player"""
        def __init__(self, account, bank, ready=False, hand=None, dealer=False, time_st=None, bet=None, able=True):
            """Defines class fields.

            Keyword arguments:
            account -- an object of the account class
            bank -- player's stack
            ready -- readiness of player
            hand -- player's hand
            dealer -- information about whether a player is a dealer or not
            time_st -- start time of the player's turn
            bet -- player's bet
            able -- player's ability to participate in the game

            """
            self.account = account
            self.stack = bank
            self.ready = ready
            self.hand = hand
            self.dealer = dealer
            self.time_st = time_st
            self.bet = bet
            self.able = able

        def encoded(self):
            """Encodes a class object to send.

            Returns dictionary where the key is the name of the field, the value is the content of the field

            """
            enc_dict = {
                'account': self.account.encoded(),
                'stack': self.stack,
                'ready': self.ready,
                'hand': self.hand,
                'dealer': self.dealer,
                'time_st': self.time_st,
                'bet': self.bet,
                'able': self.able
            }
            return enc_dict

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
        """Defines class fields.

        Keyword arguments:
        blind_size -- blind size on table
        stage -- game stage
        players -- list with player objects
        time_ready_st -- start time of the game round
        time_showdown -- start time of the showdown
        ready_players -- number of ready players
        board -- board's cards
        dealer -- an object of the player class
        not_dealer -- an object of the player class
        pot -- number of pot chips

        """
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

    def encoded(self):
        """Encodes a class object to send.

        Returns dictionary where the key is the name of the field, the value is the content of the field

        """
        enc_dict = {
            'blind_size': self.blind_size,
            'stage': self.stage,
            'players': list(map(lambda t: t.encoded(), self.players)),
            'time_ready_st': self.time_ready_st,
            'time_showdown': self.time_showdown,
            'ready_players': self.ready_players,
            'board': self.board,
            'dealer': self.dealer.encoded() if self.dealer else None,
            'not_dealer': self.not_dealer.encoded() if self.not_dealer else None,
            'pot': self.pot
        }
        return enc_dict


class GameCenter:
    """Used to work with the logic of the game"""
    def __init__(self, id, blind_size):
        """Defines class fields.

        Keyword arguments:
        id -- table's id
        blind_size -- blind size on table

        """
        self.senders = []
        self.condition_terminate = False
        self.mail = queue.Queue()
        self.game_state = GameState(blind_size)
        self.id = id
        self.blind_size = blind_size

    def process(self, message):
        """Parses the request and calls the appropriate method

        Keywords arguments:
        message -- tuple where the first argument is a request and the rest is data

        """
        func, *args = message
        if func == 'DESTROY':
            self.terminate()
        elif func == 'GAME_CENTER_CONNECT':
            args[1].money -= args[2]
            self.connect(args[0], args[1], args[2])
        elif func == 'GAME_CENTER_DISCONNECT':
            self.disconnect(args[0], args[1])
        elif func == 'GAME_CENTER_READY':
            self.ready(args[0])
        elif func == 'GAME_CENTER_NOT_READY':
            self.not_ready(args[0])
        elif func == 'GAME_CENTER_FOLD':
            flag = None
            for player in self.game_state.players:
                if player.account == args[0]:
                    flag = player.time_st
            if flag:
                self.fold(args[0])
        elif func == 'GAME_CENTER_BET':
            flag = None
            for player in self.game_state.players:
                if player.account == args[0]:
                    flag = player.time_st
            if flag:
                self.bet(args[0], args[1])
        elif func == 'GAME_CENTER_ADD_CHIPS':
            self.add_chips(args[0], args[1])

    def connect(self, sender, account, bank):
        """Adds a player to the table.

        Keyword arguments:
        sender -- an object of the manager who sent the request
        account -- an object of the account class
        bank -- number of player's chips

        """
        self.senders.append(sender)
        self.game_state.players.append(GameState.Player(account, bank))
        self.update()

    def update(self):
        """Sends the game status to the players"""
        for sen in self.senders:
            sen.mail.put(('GAME_CENTER_UPDATE', copy.deepcopy(self.game_state)))

    def disconnect(self, sender, account):
        """"Removes a player from the table

        Keyword arguments:
        sender -- an object of the manager who sent the request
        account -- an object of the account class

        """
        for sen in self.senders:
            if sen == sender:
                self.senders.remove(sender)

        for player in self.game_state.players:
            if player.account == account:
                if player.ready:
                    self.game_state.ready_players -= 1
                self.game_state.players.remove(player)
                if self.game_state.dealer == player:
                    self.game_state.dealer = None
                else:
                    self.game_state.not_dealer = None
                if self.game_state.stage != 'WAITING':
                    self.fold(account)
                else:
                    self.game_state.time_ready_st = None
                    self.update()
                account.money += player.stack
                sender.mail.put(('GAME_CENTER_DISCONNECT_SUCCESS',))

    def ready(self, account):
        """Changes the player's readiness field.

        Keyword arguments:
        account -- an object of the account class

        """
        for player in self.game_state.players:
            if player.account == account:
                player.ready = True
                self.game_state.ready_players += 1

        if self.game_state.ready_players == 2 and self.game_state.stage == 'WAITING':
            self.game_state.time_ready_st = time.time()

        self.update()

    def not_ready(self, account):
        """Changes the player's readiness field.

        Keyword arguments:
        account -- an object of the account class

        """
        for player in self.game_state.players:
            if player.account == account:
                player.ready = False
                self.game_state.ready_players -= 1
                self.game_state.time_ready_st = None

        self.update()

    def check_time(self):
        """Checks timers and reacts to their completion"""
        if self.game_state.time_ready_st and time.time() - self.game_state.time_ready_st > 8.0:
            self.game_state.time_ready_st = None
            self.preflop()

        elif self.game_state.dealer and self.game_state.dealer.time_st and time.time() - self.game_state.dealer.time_st > 25:
            if self.game_state.not_dealer.bet == 0:
                self.bet(self.game_state.dealer.account, 0)
            else:
                self.game_state.dealer.ready = False
                self.game_state.ready_players -= 1
                self.fold(self.game_state.dealer.account)

        elif self.game_state.not_dealer and self.game_state.not_dealer.time_st and time.time() - self.game_state.not_dealer.time_st > 25:
            if self.game_state.dealer.bet == self.blind_size and self.game_state.stage == 'PREFLOP':
                self.bet(self.game_state.not_dealer.account, self.blind_size)
            elif not self.game_state.dealer.bet:
                self.bet(self.game_state.not_dealer.account, 0)
            else:
                self.game_state.not_dealer.ready = False
                self.game_state.ready_players -= 1
                self.fold(self.game_state.not_dealer.account)

        elif self.game_state.time_showdown and time.time() - self.game_state.time_showdown > 5.0:
            self.game_state.time_showdown = None
            self.default_game_state()

    def preflop(self):
        """Generates a preflop stage"""
        self.game_state.stage = 'PREFLOP'

        if self.game_state.dealer == self.game_state.players[0]:
            self.game_state.dealer = self.game_state.players[1]
            self.game_state.players[1].dealer = True

            self.game_state.not_dealer = self.game_state.players[0]
        else:
            self.game_state.dealer = self.game_state.players[0]
            self.game_state.players[0].dealer = True

            self.game_state.not_dealer = self.game_state.players[1]

        self.game_state.dealer.bet = self.blind_size // 2
        self.game_state.dealer.stack -= self.game_state.dealer.bet

        self.game_state.not_dealer.bet = self.blind_size
        self.game_state.not_dealer.stack -= self.game_state.not_dealer.bet

        self.game_state.pot = self.blind_size // 2 + self.blind_size

        self.deal()
        self.game_state.dealer.time_st = time.time()
        self.update()

    def deal(self):
        """Identifies player cards and board cards"""
        deck = ['AS', 'AH', 'AC', 'AD',
                'KS', 'KH', 'KC', 'KD',
                'QS', 'QH', 'QC', 'QD',
                'JS', 'JH', 'JC', 'JD',
                'TS', 'TH', 'TC', 'TD',
                '9S', '9H', '9C', '9D',
                '8S', '8H', '8C', '8D',
                '7S', '7H', '7C', '7D',
                '6S', '6H', '6C', '6D',
                '5S', '5H', '5C', '5D',
                '4S', '4H', '4C', '4D',
                '3S', '3H', '3C', '3D',
                '2S', '2H', '2C', '2D']
        random.shuffle(deck)
        i = 0
        for player in self.game_state.players:
            player.hand = deck[i] + ' ' + deck[i + 1]
            i += 2
        self.game_state.board = deck[i] + ' ' + deck[i + 1] + ' ' + deck[i + 2] + ' ' + deck[i + 3] + ' ' + deck[i + 4]

    def fold(self, account):
        """Accepts the player's fold and calls the default_game_state method

        Keyword arguments:
        account -- an object of the account class

        """
        for player in self.game_state.players:
            if player.account != account:
                player.stack += self.game_state.pot

        self.default_game_state()

    def bet(self, account, bet):
        """Accepts the player's bet and determines the next move of the game

        account -- an object of the account class
        bet -- the number of chips that the player has bet

        """
        for player in self.game_state.players:
            if player.account == account:
                if player.bet:
                    self.game_state.pot += bet - player.bet
                    player.stack += player.bet - bet
                else:
                    self.game_state.pot += bet
                    player.stack -= bet
                player.bet = bet
                player.time_st = None
            else:
                next_player = player

        if bet == self.blind_size and self.game_state.dealer.account == account and self.game_state.stage == 'PREFLOP':
            next_player.time_st = time.time()
            self.update()
        elif self.game_state.dealer.bet == self.game_state.not_dealer.bet:
            self.update()
            if self.game_state.dealer.stack == 0 or self.game_state.not_dealer.stack == 0:
                self.showdown()
            elif self.game_state.stage == 'PREFLOP':
                self.flop()

            elif self.game_state.stage == 'FLOP':
                self.turn()

            elif self.game_state.stage == 'TURN':
                self.river()

            elif self.game_state.stage == 'RIVER':
                self.showdown()
        else:
            next_player.time_st = time.time()
            self.update()

    def flop(self):
        """Changes the stage of the game and starts the timer of the player on the big blind"""
        self.game_state.stage = 'FLOP'
        for player in self.game_state.players:
            player.bet = None
        self.game_state.not_dealer.time_st = time.time()
        self.update()

    def turn(self):
        """Changes the stage of the game and starts the timer of the player on the big blind"""
        self.game_state.stage = 'TURN'
        for player in self.game_state.players:
            player.bet = None
        self.game_state.not_dealer.time_st = time.time()
        self.update()

    def river(self):
        """Changes the stage of the game and starts the timer of the player on the big blind"""
        self.game_state.stage = 'RIVER'
        for player in self.game_state.players:
            player.bet = None
        self.game_state.not_dealer.time_st = time.time()
        self.update()

    def showdown(self):
        """Changes the stage of the game and determines the winner"""
        self.game_state.stage = 'SHOWDOWN'
        for player in self.game_state.players:
            player.bet = None

        comb_d = centerspack.find_combination.combination(self.game_state.dealer.hand.split(),
                                                          self.game_state.board.split())
        comb_nd = centerspack.find_combination.combination(self.game_state.not_dealer.hand.split(),
                                                           self.game_state.board.split())

        if comb_d > comb_nd:
            self.game_state.dealer.stack += self.game_state.pot
        elif comb_nd > comb_d:
            self.game_state.not_dealer.stack += self.game_state.pot
        else:
            self.game_state.dealer.stack += self.game_state.pot // 2
            self.game_state.not_dealer.stack += self.game_state.pot // 2

        self.game_state.time_showdown = time.time()

        self.update()

    def add_chips(self, account, chips):
        """Adds chips to the player's stack

        Keyword arguments:
        account -- an object of the account class
        chips -- the number of chips that the player adds

        """
        for player in self.game_state.players:
            if player.account == account:
                account.money -= chips
                player.stack += chips
                player.able = True
        self.update()

    def default_game_state(self):
        """Changes the fields of the game center class object to default values"""
        self.game_state.stage = 'WAITING'
        for player in self.game_state.players:
            player.hand = None
            player.time_st = None
            player.dealer = False
            player.bet = None
            if player.stack < self.blind_size:
                player.able = False
                player.ready = False
                self.game_state.ready_players -= 1

        self.game_state.flop = None
        self.game_state.turn = None
        self.game_state.river = None
        self.game_state.pot = 0
        if self.game_state.ready_players == 2:
            self.game_state.time_ready_st = time.time()
        self.update()

    def terminate(self):
        """Changes condition_terminate field that causes the loop to stop in the run method"""
        self.condition_terminate = True

    def run(self):
        """Initializes the lifecycle of the game_center class object"""
        while not self.condition_terminate:
            self.check_time()
            while not self.mail.empty() and not self.condition_terminate:
                message = self.mail.get()
                self.process(message)
                time.sleep(0.01)
