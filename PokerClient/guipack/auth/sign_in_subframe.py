from tkinter import *
from tkinter import ttk


class SignInSubframe(ttk.Frame):
    """ Class describing Sign In subframe of the Authorization mainframe."""

    def __init__(self, master, terminal, context):
        """ Construct Sign In subframe

        :param master: Master widget.
        :param terminal: Client terminal object.
        :param context: Authorization Context object.
        """

        super().__init__(master)

        self.terminal = terminal
        self.context = context
        self.incoming_context = None

        self.frame = ttk.Frame(self)
        self.login_label = ttk.Label(self.frame, text='Login')
        self.login_entry = ttk.Entry(self.frame, width=32)
        self.password_label = ttk.Label(self.frame, text='Password')
        self.password_entry = ttk.Entry(self.frame, width=32, show='*')
        self.sign_in_button = ttk.Button(self.frame, text='Sign In', command=self.on_sign_in)
        self.separator = ttk.Separator(self.frame)
        self.or_label = ttk.Label(self.frame, text='or')
        self.sign_up_button = ttk.Button(self.frame, text='Sign Up', command=self.on_sign_up)

        style = ttk.Style()
        style.configure("BW.TLabel", foreground="red", font=('Calibri', 8))
        self.login_is_empty = ttk.Label(self.frame, text='Required field!', style='BW.TLabel')
        self.password_is_empty = ttk.Label(self.frame, text='Required field!', style='BW.TLabel')
        self.signin_failed = ttk.Label(self.frame, text='Wrong login or password!', style='BW.TLabel')
        self.signin_taken = ttk.Label(self.frame, text='Someone had already signed into that account!', style='BW.TLabel')

        self.frame.grid(padx=10, pady=10)
        self.login_label.grid(row=10, padx=5, sticky='w')
        self.login_entry.grid(row=11, padx=5, pady=5, sticky='we')
        self.password_label.grid(row=20, padx=5, sticky='w')
        self.password_entry.grid(row=21, padx=5, pady=5, sticky='we')
        self.sign_in_button.grid(row=30, padx=5, pady=5, sticky='we')
        self.separator.grid(row=40, padx=5, pady=5, sticky='we')
        self.or_label.grid(row=40, padx=5, pady=5)
        self.sign_up_button.grid(row=50, padx=5, pady=5, sticky='we')

    def context_update(self):
        """Method for updating current object context."""

        if self.incoming_context.signin_status == 'FAILED':
            self.signin_failed.grid(row=22, padx=5)
            self.password_entry.delete(0, END)
        if self.incoming_context.signin_status == 'TAKEN':
            self.signin_taken.grid(row=22, padx=5)
            self.password_entry.delete(0, END)
        self.context = self.incoming_context
        self.incoming_context = None
        # self.email_is_empty.grid_remove()
        # self.password_is_empty.grid_remove()
        # self.login_failed.grid_remove()
        #
        # if self.incoming_context.sign_in_email_status == 'EMPTY':
        #     self.email_is_empty.grid(row=12, padx=5, sticky='e')
        #     self.password_entry.delete(0, END)
        # if self.incoming_context.sign_in_password_status == 'EMPTY':
        #     self.password_is_empty.grid(row=22, padx=5, sticky='e')
        # if self.incoming_context.sign_in_login_status == 'FAILED':
        #     self.login_failed.grid(row=22, padx=5)
        #     self.password_entry.delete(0, END)
        # if (self.incoming_context.sign_in_email_status == 'DEFAULT' and
        #         self.incoming_context.sign_in_password_status == 'DEFAULT' and
        #         self.incoming_context.sign_in_login_status == 'DEFAULT'):
        #     self.email_entry.delete(0, END)
        #     self.password_entry.delete(0, END)

    def on_sign_in(self):
        """Read user Sign In form and if its validation was successful, send all data to the Terminal"""

        self.login_is_empty.grid_remove()
        self.password_is_empty.grid_remove()
        self.signin_failed.grid_remove()
        self.signin_taken.grid_remove()

        login = self.login_entry.get()
        password = self.password_entry.get()
        if self.context.check_signin_form(login, password):
            action = ('SIGNIN', login, password)
            self.terminal.mail.put(('SEND', action))
        else:
            if not login:
                self.login_is_empty.grid(row=12, padx=5, sticky='e')
                self.password_entry.delete(0, END)
            if not password:
                self.password_is_empty.grid(row=22, padx=5, sticky='e')

    def on_sign_up(self):
        """Schedule CHANGE_TO_SIGN_UP event."""
        self.master.event_generate('<<CHANGE_TO_SIGN_UP>>')
