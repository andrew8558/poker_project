from tkinter import *
from tkinter import ttk


class AccountSubframe(ttk.Frame):
    """ Class describing Account subframe of the Menu mainframe."""

    def __init__(self, master, terminal, context):
        """ Construct Account subframe

        :param master: Master widget.
        :param terminal: Client terminal object.
        :param context: Authorization Context object.
        """

        super().__init__(master)
        self.terminal = terminal

        self.context = context
        self.incoming_context = None

        self.frame = ttk.Frame(self)
        self.login_label = ttk.Label(self.frame, text='Login:')
        self.password_label = ttk.Label(self.frame, text='Password:')
        self.money_label = ttk.Label(self.frame, text='Money:')
        self.login_entry = ttk.Entry(self.frame, width=25)
        self.login_entry.insert(0, self.context.account.login)
        self.password_entry = ttk.Entry(self.frame, width=25)
        self.password_entry.insert(0, self.context.account.password)
        self.money_value_label = ttk.Label(self.frame, text=self.context.account.money)

        self.login_change_button = ttk.Button(self.frame, text='Change', command=self.on_change_login)
        self.password_change_button = ttk.Button(self.frame, text='Change', command=self.on_change_password)
        self.logout_button = ttk.Button(self.frame, text='Logout', command=self.on_logout)

        self.login_label.grid(row=0, column=0, padx=5, pady=5)
        self.login_entry.grid(row=0, column=1, padx=5, pady=5)
        self.login_change_button.grid(row=0, column=2, padx=5, pady=5)
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        self.password_change_button.grid(row=1, column=2, padx=5, pady=5)
        self.money_label.grid(row=2, column=0, padx=5, pady=5)
        self.money_value_label.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.logout_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        self.frame.grid(padx=10, pady=10)

    def context_update(self):
        """Method for updating current object context."""

        self.login_entry.delete(0, END)
        self.login_entry.insert(0, self.incoming_context.account.login)
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, self.incoming_context.account.password)
        self.context = self.incoming_context
        self.incoming_context = None

    def on_change_login(self):
        """Read user Change Login form and if its validation was successful, send all data to the Terminal"""

        new_login = self.login_entry.get()
        if self.context.check_change_login_form(new_login):
            action = ('CHANGE_LOGIN', new_login)
            self.terminal.mail.put(('SEND', action))

    def on_change_password(self):
        """Read user Change Password form and if its validation was successful, send all data to the Terminal"""

        new_password = self.password_entry.get()
        if self.context.check_change_password_form(new_password):
            action = ('CHANGE_PASSWORD', new_password)
            self.terminal.mail.put(('SEND', action))

    def on_logout(self):
        """Read user Logout form and send data to the Terminal"""

        action = ('LOGOUT',)
        self.terminal.mail.put(('SEND', action))