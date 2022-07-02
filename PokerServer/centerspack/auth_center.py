import sqlite3 as sql
import queue
import time


class AuthCenter:
    """Used to work with player accounts"""
    class Account:
        """Represents players data"""
        def __init__(self, nick, password, money):
            """Defines class fields.

            Keyword arguments:
            nick -- player's nickname
            password -- player's password
            money -- player's balance

            """
            self.login = nick
            self.password = password
            self.money = money

        def encoded(self):
            """Encodes a class object to send

            Returns dictionary where the key is the name of the field, the value is the content of the field

            """
            enc_dict = {
                'login': self.login,
                'password': self.password,
                'money': self.money
            }
            return enc_dict

    def __init__(self):
        """Defines class fields"""
        self.mail = queue.Queue()
        self.condition_terminate = False
        self.con = None
        self.cur = None

    def process(self, message):
        """Parses the request and calls the appropriate method

        Keywords arguments:
        message -- tuple where the first argument is a request and the rest is data

        """
        func, *args = message
        if func == 'AUTH_CENTER_SEARCH':
            self.log(args[1], args[2], args[0])
        elif func == 'AUTH_CENTER_APPEND':
            self.auth(args[1], args[2], args[0])
        elif func == 'AUTH_CENTER_CHANGE_LOGIN':
            self.change_login(args[1], args[2], args[0])
        elif func == 'AUTH_CENTER_CHANGE_PASSWORD':
            self.change_password(args[1], args[2], args[0])
        elif func == 'AUTH_CENTER_LOGOUT':
            self.log_out(args[0])
        elif func == 'DESTROY':
            self.terminate()

    def log(self, nick, password, sender):
        """Registers the player, saves player data in a database and informs about the success of the request.

        Keyword arguments:
        nick -- player's nickname
        password -- player's password
        sender -- the object of the manager who sent the request

        """
        self.cur.execute(f"SELECT COUNT(nickname) FROM 'players' WHERE nickname='{nick}'")
        count = self.cur.fetchall()[0][0]
        if count == 0:
            sender.mail.put(('AUTH_CENTER_SEARCH_FAILED', ))
        else:
            self.cur.execute(f"SELECT taken FROM 'players' WHERE nickname='{nick}'")
            taken = self.cur.fetchall()[0][0]
            if taken == 1:
                sender.mail.put(('AUTH_CENTER_SEARCH_TAKEN', ))
            else:
                right_password = self.get_password(nick)
                m = self.get_money(nick)
                if right_password == password:
                    self.cur.execute(f"UPDATE 'players' SET taken='{1}' WHERE nickname='{nick}'")
                    self.con.commit()
                    sender.mail.put(('AUTH_CENTER_SEARCH_SUCCESS', AuthCenter.Account(nick, password, m)))
                else:
                    sender.mail.put(('AUTH_CENTER_SEARCH_FAILED', ))

    def auth(self, nick, password, sender):
        """Authorizes the player and informs about the success of the request.

        Keyword arguments:
        nick -- player's nickname
        password -- player's password
        sender -- the object of the manager who sent the request

        """
        self.cur.execute(f"SELECT COUNT(nickname) FROM 'players' WHERE nickname='{nick}'")
        count = self.cur.fetchall()[0][0]
        if count == 0:
            self.cur.execute(f"INSERT INTO 'players' VALUES ('{nick}', '{password}', {1000}, {0})")
            sender.mail.put(('AUTH_CENTER_APPEND_SUCCESS', ))
        else:
            sender.mail.put(('AUTH_CENTER_APPEND_FAILED', ))
        self.con.commit()

    def change_password(self, nick, new_password, sender):
        """Changes player's password.

        Keyword arguments:
        nick -- player's nickname
        new_password -- new player password
        sender -- the object of the manager who sent the request

        """
        self.cur.execute(f"UPDATE 'players' SET password='{new_password}' WHERE nickname='{nick}'")
        m = self.get_money(nick)
        sender.mail.put(('AUTH_CENTER_CHANGE_LOGIN_SUCCESS', AuthCenter.Account(nick, new_password, m)))
        self.con.commit()

    def change_login(self, old_nick, new_nick, sender):
        """Changes player's nickname and informs about the success of the request.

        Keyword arguments:
        old_nick -- old player nickname
        new_nick -- new player nickname
        sender -- the object of the manager who sent the request

        """
        self.cur.execute(f"SELECT COUNT(nickname) FROM 'players' WHERE nickname='{new_nick}'")
        count = self.cur.fetchall()[0][0]
        if count == 0:
            self.cur.execute(f"UPDATE 'players' SET nickname='{new_nick}' WHERE nickname='{old_nick}'")
            password = self.get_password(new_nick)
            m = self.get_money(new_nick)
            sender.mail.put(('AUTH_CENTER_CHANGE_LOGIN_SUCCESS', AuthCenter.Account(new_nick, password, m)))
        else:
            sender.mail.put(('AUTH_CENTER_CHANGE_LOGIN_FAILED', ))
        self.con.commit()

    def get_password(self, nick):
        """Gets player's password from database.

        Keyword arguments:
        nick -- player's nickname

        Returns string - player's password.

        """
        self.cur.execute(f"SELECT password FROM 'players' WHERE nickname='{nick}'")
        x = self.cur.fetchall()
        return x[0][0]

    def get_money(self, nick):
        """Gets player's balance from database.

        Keyword arguments:
        nick -- player's nickname

        Returns integer number - player's balance.

        """
        self.cur.execute(f"SELECT money FROM 'players' WHERE nickname='{nick}'")
        x = self.cur.fetchall()
        return x[0][0]

    def log_out(self, account):
        """Saves the player's balance and changes his activity status in the database.

        Keyword arguments:
        account -- an object of the account class

        """
        self.cur.execute(f"UPDATE 'players' SET taken='{0}' WHERE nickname='{account.login}'")
        self.cur.execute(f"UPDATE 'players' SET money='{account.money}' WHERE nickname='{account.login}'")
        self.con.commit()

    def terminate(self):
        """Changes condition_terminate field that causes the loop to stop in the run method"""
        self.condition_terminate = True

    def run(self):
        """Initializes the lifecycle of the auth_center class object"""
        self.con = sql.connect('user_accounts.db')
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS 'players' ('nickname' TEXT, 'password' TEXT, 'money' INTEGER, 'taken' INTEGER)")
        while not self.condition_terminate:
            while not self.mail.empty() and not self.condition_terminate:
                message = self.mail.get()
                self.process(message)
                time.sleep(0.01)
