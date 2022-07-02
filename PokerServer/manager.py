import time
import threading
import queue
import server_terminal
import datetime
import contextpack.no_connection_context
import contextpack.auth_context
import contextpack.menu_context
import contextpack.game_context


class Manager:
    """Implementation of Manager architectural unit

    mail -- Field used to pass requests for Manager object. Implemented as a queue.Queue object.
    """

    def __init__(self, poker_server_log, auth_center, table_center, port_number):
        """Construct Manager object

        :param poker_server_log: Server log object used for logging important Manager operations.
        :param auth_center: Authorization center object used for sending requests in Authorization context.
        :param table_center: Table center object used for sending requests in Menu context.
        :param port_number: Allocated port used for creation of Server Terminal object
        """

        self.mail = queue.Queue()
        self.state = 'RUNNING'

        self.poker_server_log = poker_server_log
        self.auth_center = auth_center
        self.table_center = table_center
        self.game_center = None

        self.terminal = server_terminal.ServerTerminal(self, '25.69.43.137', port_number)  # You can set IP-address here.
        self.terminal_thread = threading.Thread(target=self.terminal.run, name='terminal_thread')

        self.context = contextpack.no_connection_context.NoConnectionContext()

    def process(self, msg):
        """Process incoming message.

        :param msg: Incoming message.
        """

        cmd, *args = msg
        if cmd == 'DESTROY':
            self.state = 'TERMINATING'
            if self.context.name == 'NO_CONNECTION':
                self.state = 'TERMINATED'
            elif self.context.name == 'AUTH':
                self.state = 'TERMINATED'
            elif self.context.name == 'MENU':
                self.auth_center.mail.put(('AUTH_CENTER_LOGOUT', self.context.account))
                self.state = 'TERMINATED'
            elif self.context.name == 'GAME':
                sender = self
                account = self.context.account
                self.game_center.mail.put(('GAME_CENTER_DISCONNECT', sender, account))
        elif cmd == 'NEW_CONNECTION':
            self.context = contextpack.auth_context.AuthContext()
            self.terminal.mail.put(('SEND', self.context))
        elif cmd == 'CONNECTION_LOST':
            self.state = 'DEFAULTING'
            if self.context.name == 'AUTH':
                self.context = contextpack.no_connection_context.NoConnectionContext()
                self.state = 'RUNNING'
            elif self.context.name == 'MENU':
                self.auth_center.mail.put(('AUTH_CENTER_LOGOUT', self.context.account))
                self.state = 'RUNNING'
            elif self.context.name == 'GAME':
                sender = self
                account = self.context.account
                self.game_center.mail.put(('GAME_CENTER_DISCONNECT', sender, account))
        elif cmd == 'NEW_ACTION':
            if self.state == 'RUNNING':
                action = args[0]
                self.process_action(action)
        elif cmd == 'AUTH_CENTER_SEARCH_SUCCESS':
            account = args[0]
            self.context = contextpack.menu_context.MenuContext(account)
            self.terminal.mail.put(('SEND', self.context))
            self.state = 'RUNNING'
        elif cmd == 'AUTH_CENTER_SEARCH_FAILED':
            self.context.signin_status = 'FAILED'
            self.terminal.mail.put(('SEND', self.context))
            self.state = 'RUNNING'
        elif cmd == 'AUTH_CENTER_SEARCH_TAKEN':
            self.context.signin_status = 'TAKEN'
            self.terminal.mail.put(('SEND', self.context))
            self.state = 'RUNNING'
        elif cmd == 'AUTH_CENTER_APPEND_SUCCESS':
            self.context.signup_status = 'SUCCESS'
            self.terminal.mail.put(('SEND', self.context))
            self.state = 'RUNNING'
        elif cmd == 'AUTH_CENTER_APPEND_FAILED':
            self.context.signup_status = 'FAILED'
            self.terminal.mail.put(('SEND', self.context))
            self.state = 'RUNNING'
        elif cmd == 'AUTH_CENTER_CHANGE_LOGIN_SUCCESS':
            account = args[0]
            self.context.account = account
            self.context.change_login_status = 'SUCCESS'
            self.terminal.mail.put(('SEND', self.context))
            self.state = 'RUNNING'
        elif cmd == 'AUTH_CENTER_CHANGE_LOGIN_FAILED':
            self.context.change_login_status = 'FAILED'
            self.terminal.mail.put(('SEND', self.context))
            self.state = 'RUNNING'
        elif cmd == 'AUTH_CENTER_CHANGE_PASSWORD_SUCCESS':
            account = args[0]
            self.context.account = account
            self.context.change_password_status = 'SUCCESS'
            self.terminal.mail.put(('SEND', self.context))
            self.state = 'RUNNING'
        elif cmd == 'TABLE_CENTER_REFRESH_SUCCESS':
            tables_list = args[0]
            self.context.tables_list = tables_list
            self.terminal.mail.put(('SEND', self.context))
            self.state = 'RUNNING'
        elif cmd == 'TABLE_CENTER_CONNECT_SUCCESS':
            sender = self
            self.game_center = args[0]
            enter_stack = self.context.enter_stack
            self.context = contextpack.game_context.GameContext(self.context.account, self.game_center.id)
            self.game_center.mail.put(('GAME_CENTER_CONNECT', sender, self.context.account, enter_stack))
        elif cmd == 'TABLE_CENTER_CONNECT_FAILED':
            self.context.connect_status = 'FAILED'
            self.terminal.mail.put(('SEND', self.context))
            self.state = 'RUNNING'
        elif cmd == 'TABLE_CENTER_CREATE_SUCCESS':
            sender = self
            self.game_center = args[0]
            enter_stack = self.context.enter_stack
            self.context = contextpack.game_context.GameContext(self.context.account, self.game_center.id)
            self.game_center.mail.put(('GAME_CENTER_CONNECT', sender, self.context.account, enter_stack))
        elif cmd == 'TABLE_CENTER_DISCONNECT_SUCCESS':
            if self.state == 'TERMINATING':
                self.auth_center.mail.put(('AUTH_CENTER_LOGOUT', self.context.account))
                self.state = 'TERMINATED'
            elif self.state == 'DEFAULTING':
                self.auth_center.mail.put(('AUTH_CENTER_LOGOUT', self.context.account))
                self.context = contextpack.no_connection_context.NoConnectionContext()
                self.state = 'RUNNING'
            else:
                self.context = contextpack.menu_context.MenuContext(self.context.account)
                self.terminal.mail.put(('SEND', self.context))
                self.state = 'RUNNING'
        elif cmd == 'GAME_CENTER_UPDATE':
            game_state = args[0]
            self.context.build_context(game_state)
            self.terminal.mail.put(('SEND', self.context))
            self.state = 'RUNNING'
        elif cmd == 'GAME_CENTER_DISCONNECT_SUCCESS':
            sender = self
            table_id = self.game_center.id
            self.table_center.mail.put(('TABLE_CENTER_DISCONNECT', sender, table_id))

    def process_action(self, action):
        """Process user action if it is provided in the message

        :param action: User action
        """
        if isinstance(action, tuple) and action:
            cmd, *args = action
            if self.context.name == 'AUTH':
                if cmd == 'SIGNIN':
                    if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
                        sender = self
                        login = args[0]
                        password = args[1]
                        if self.context.check_signin_form(login, password):
                            self.auth_center.mail.put(('AUTH_CENTER_SEARCH', sender, login, password))
                            self.state = 'WAITING'
                elif cmd == 'SIGNUP':
                    if len(args) == 3 and isinstance(args[0], str) and isinstance(args[1], str) and isinstance(args[2],
                                                                                                               str):
                        sender = self
                        login = args[0]
                        password = args[1]
                        repeat_password = args[2]
                        if self.context.check_signup_form(login, password, repeat_password):
                            self.auth_center.mail.put(('AUTH_CENTER_APPEND', sender, login, password))
                            self.state = 'WAITING'

            elif self.context.name == 'MENU':
                if cmd == 'LOGOUT' and len(args) == 0:
                    self.auth_center.mail.put(('AUTH_CENTER_LOGOUT', self.context.account))
                    self.context = contextpack.auth_context.AuthContext()
                    self.terminal.mail.put(('SEND', self.context))
                elif cmd == 'CHANGE_LOGIN':
                    if len(args) == 1 and isinstance(args[0], str):
                        sender = self
                        old_login = self.context.account.login
                        new_login = args[0]
                        if self.context.check_change_login_form(new_login):
                            self.auth_center.mail.put(('AUTH_CENTER_CHANGE_LOGIN', sender, old_login, new_login))
                            self.state = 'WAITING'
                elif cmd == 'CHANGE_PASSWORD':
                    if len(args) == 1 and isinstance(args[0], str):
                        sender = self
                        login = self.context.account.login
                        new_password = args[0]
                        if self.context.check_change_password_form(new_password):
                            self.auth_center.mail.put(('AUTH_CENTER_CHANGE_PASSWORD', sender, login, new_password))
                            self.state = 'WAITING'
                elif cmd == 'REFRESH' and len(args) == 0:
                    sender = self
                    self.table_center.mail.put(('TABLE_CENTER_REFRESH', sender))
                    self.state = 'WAITING'
                elif cmd == 'CONNECT':
                    if len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
                        sender = self
                        room_id = args[0]
                        enter_stack = args[1]
                        if self.context.check_connect_form(room_id, enter_stack):
                            self.context.enter_stack = enter_stack
                            self.table_center.mail.put(('TABLE_CENTER_CONNECT', sender, room_id))
                            self.state = 'WAITING'
                elif cmd == 'CREATE':
                    if len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
                        sender = self
                        blind_size = args[0]
                        enter_stack = args[1]
                        if self.context.check_create_form(blind_size, enter_stack):
                            self.context.enter_stack = enter_stack
                            self.table_center.mail.put(('TABLE_CENTER_CREATE', sender, blind_size))
                            self.state = 'WAITING'

            elif self.context.name == 'GAME':
                if cmd == 'DISCONNECT' and len(args) == 0:
                    sender = self
                    account = self.context.account
                    self.game_center.mail.put(('GAME_CENTER_DISCONNECT', sender, account))
                    self.state = 'WAITING'
                elif cmd == 'READY' and len(args) == 0:
                    sender = self
                    account = self.context.account
                    self.game_center.mail.put(('GAME_CENTER_READY', account))
                    self.state = 'WAITING'
                elif cmd == 'NOT_READY' and len(args) == 0:
                    sender = self
                    account = self.context.account
                    self.game_center.mail.put(('GAME_CENTER_NOT_READY', account))
                    self.state = 'WAITING'
                elif cmd == 'ADD_CHIPS' and len(args) == 1 and isinstance(args[0], int):
                    sender = self
                    account = self.context.account
                    chips = args[0]
                    if self.context.check_add_chips_form(chips):
                        self.game_center.mail.put(('GAME_CENTER_ADD_CHIPS', account, chips))
                        self.state = 'WAITING'
                elif cmd == 'FOLD' and len(args) == 0:
                    sender = self
                    account = self.context.account
                    if self.context.check_fold_form():
                        self.game_center.mail.put(('GAME_CENTER_FOLD', account))
                        self.state = 'WAITING'
                elif cmd == 'BET' and len(args) == 1 and isinstance(args[0], int):
                    sender = self
                    account = self.context.account
                    bet = args[0]
                    if self.context.check_bet_form(bet):
                        self.game_center.mail.put(('GAME_CENTER_BET', account, bet))
                        self.state = 'WAITING'

    def run(self):
        """ Run Manager lifecycle."""
        # Create terminal
        current_time = datetime.datetime.now().time()
        self.poker_server_log.mail.put(('LOG', f'{current_time}\t\t'
                                               f'In {threading.current_thread().name}: Running initiated!'))

        self.terminal_thread.start()

        # Run mainloop
        while self.state != 'TERMINATED':
            while not self.mail.empty() and self.state != 'TERMINATED':
                msg = self.mail.get()

                current_time = datetime.datetime.now().time()
                self.poker_server_log.mail.put(('LOG', f'{current_time}\t\t'
                                                       f'In {threading.current_thread().name}: Got message: {msg}'))

                self.process(msg)
            time.sleep(0.05)

        # Get ready for termination
        self.terminal.mail.put(('DESTROY',))
        self.terminal_thread.join()

        current_time = datetime.datetime.now().time()
        self.poker_server_log.mail.put(('LOG', f'{current_time}\t\t'
                                               f'In {threading.current_thread().name}: Destruction complete!'))
