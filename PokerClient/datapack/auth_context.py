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

    @staticmethod
    def decoded(enc_dict):
        """Decode JSON-formatted dictionary of an object and return corresponding Context object."""
        signin_status = enc_dict['signin_status']
        signup_status = enc_dict['signup_status']
        context = AuthContext(signin_status, signup_status)
        return context
