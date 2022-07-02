import datapack.table
import datapack.account


class MenuContext:
    """Data object describing all important parameters of the Menu Context"""

    def __init__(self, account, change_login_status='DEFAULT', change_password_status='DEFAULT', tables_list=[],
                 connect_status='DEFAULT', enter_stack=None):
        """Construct Menu Context object

        :param account: Account object, allocated by Authorization Center, associated with account, which is under user
        control.
        :param change_login_status: Status of Change Login attempt. By default, its value is DEFAULT.
        :param change_password_status: Status of Change Password attempt. By default, its value is DEFAULT.
        :param tables_list: List of all server tables. By default, the list is empty.
        :param connect_status: Status of Connect To Room attempt. By default, its value is DEFAULT.
        :param enter_stack: Field used to store entered enter-stack value.
        """

        self.name = 'MENU'
        self.account = account
        self.change_login_status = change_login_status
        self.change_password_status = change_password_status
        self.tables_list = tables_list
        self.connect_status = connect_status
        self.enter_stack = enter_stack

    def check_change_login_form(self, new_login):
        """Method for Change Login form validation.

        :param new_login: Entered new login.
        :return: Returns True if the form is valid. Otherwise, returns False.
        """

        return new_login and new_login != self.account.login

    def check_change_password_form(self, new_password):
        """Method for Change Password form validation.

        :param new_password: Entered new password.
        :return: Returns True if the form is valid. Otherwise, returns False.
        """
        return bool(new_password)

    def check_connect_form(self, room_id, enter_stack):
        """Method for form validation.

        :param room_id: Entered room id.
        :param enter_stack: Entered enter stack.
        :return: Returns True if the form is valid. Otherwise, returns False.
        """
        return enter_stack <= self.account.money

    def check_create_form(self, blind_size, enter_stack, ):
        """Method for form validation.

        :param blind_size: Entered blind size.
        :param enter_stack: Entered enter stack.
        :return: Returns True if the form is valid. Otherwise, returns False.
        """
        return enter_stack <= self.account.money and 40 * blind_size <= enter_stack <= 100 * blind_size

    @staticmethod
    def decoded(enc_dict):
        """Decode JSON-formatted dictionary of an object and return corresponding Context object."""
        account = datapack.account.Account.decoded(enc_dict['account'])
        change_login_status = enc_dict['change_login_status']
        change_password_status = enc_dict['change_password_status']
        tables_list = list(
            map(lambda table_enc_dict: datapack.table.Table.decoded(table_enc_dict), enc_dict['tables_list']))
        connect_status = enc_dict['connect_status']
        enter_stack = enc_dict['enter_stack']
        return MenuContext(account,
                           change_login_status, change_password_status,
                           tables_list,
                           connect_status,
                           enter_stack)
