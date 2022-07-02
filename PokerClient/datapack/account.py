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

    @staticmethod
    def decoded(enc_dict):
        """Decode JSON-formatted dictionary of an object and return corresponding Account object."""

        nick = enc_dict['login']
        password = enc_dict['password']
        money = enc_dict['money']
        return Account(nick, password, money)
