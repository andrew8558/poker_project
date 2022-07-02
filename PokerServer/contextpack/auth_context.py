class AuthContext:
    """Data object describing all important parameters of the Authorization Context"""

    def __init__(self, signin_status='DEFAULT', signup_status='DEFAULT'):
        """Construct Authorization Context object

        :param signin_status: Status of Sign In attempt. By default, its value is DEFAULT.
        :param signup_status: Status of Sign Up attempt. By default, its value is DEFAULT.
        """

        self.name = 'AUTH'
        self.signin_status = signin_status
        self.signup_status = signup_status

    def check_signin_form(self, login, password):
        """Method for Sign In form validation.

        :param login: Entered login.
        :param password: Entered password.
        :return: Returns True if the form is valid. Otherwise, returns False.
        """

        return login and password

    def check_signup_form(self, login, password, repeat_password):
        """Method for Sign Up form validation.

        :param login: Entered login.
        :param password: Entered password.
        :param repeat_password: Entered repeated password.
        :return: Returns True if the form is valid. Otherwise, returns False.
        """

        return login and password and repeat_password and password == repeat_password

    def encoded(self):
        """ Get JSON-encoded version of Authorization Context.

        :return: Returns JSON-encoded version of the object state.
        """

        enc_dict = {
            'name': self.name,
            'signin_status': self.signin_status,
            'signup_status': self.signup_status
        }
        return enc_dict
