from tkinter import *
from tkinter import ttk


class SignUpSubframe(ttk.Frame):
    """ Class describing Sign Up subframe of the Authorization mainframe."""

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
        self.repeat_password_label = ttk.Label(self.frame, text='Repeat Password')
        self.repeat_password_entry = ttk.Entry(self.frame, width=32, show='*')
        self.submit_button = ttk.Button(self.frame, text='Submit', command=self.on_submit)
        self.back_button = ttk.Button(self.frame, text='Back', command=self.on_back)

        err_style = ttk.Style()
        err_style.configure("BW.TLabel", foreground="red", font=('Calibri', 8))
        ok_style = ttk.Style()
        ok_style.configure("OK.TLabel", foreground="green", font=('Calibri', 8))
        self.login_is_empty = ttk.Label(self.frame, text='Required field!', style='BW.TLabel')
        self.login_is_taken = ttk.Label(self.frame, text='Login is already taken!', style='BW.TLabel')
        self.passwords_are_empty = ttk.Label(self.frame, text='Both fields are required!', style='BW.TLabel')
        self.passwords_mismatch = ttk.Label(self.frame, text="Passwords' mismatch!", style='BW.TLabel')
        self.signup_success = ttk.Label(self.frame, text="Success!", style='OK.TLabel')

        self.frame.grid(padx=10, pady=10)
        self.login_label.grid(row=10, column=0, padx=5, sticky='w')
        self.login_entry.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky='we')
        self.password_label.grid(row=20, column=0, padx=5, sticky='w')
        self.password_entry.grid(row=21, column=0, columnspan=2, padx=5, pady=5, sticky='we')
        self.repeat_password_label.grid(row=22, column=0, padx=5, sticky='w')
        self.repeat_password_entry.grid(row=23, column=0, columnspan=2, padx=5, pady=5, sticky='we')
        self.submit_button.grid(row=30, column=0, columnspan=2, padx=5, pady=5, sticky='we')
        self.back_button.grid(row=40, column=1, padx=5, pady=5, sticky='e')

    def context_update(self):
        """Method for updating current object context."""

        if self.incoming_context.signup_status == 'SUCCESS':
            self.signup_success.grid(row=24, column=0, columnspan=2, padx=5)
            self.password_entry.delete(0, END)
            self.repeat_password_entry.delete(0, END)
        if self.incoming_context.signup_status == 'FAILED':
            self.login_is_taken.grid(row=12, column=1, padx=5, sticky='e')
            self.password_entry.delete(0, END)
            self.repeat_password_entry.delete(0, END)
        self.context = self.incoming_context
        self.incoming_context = None
        # self.email_is_empty.grid_remove()
        # self.email_is_taken.grid_remove()
        # self.passwords_are_empty.grid_remove()
        # self.passwords_mismatch.grid_remove()
        #
        # if self.incoming_context.sign_up_email_status == 'EMPTY':
        #     self.email_is_empty.grid(row=12, column=1, padx=5, sticky='e')
        # if self.incoming_context.sign_up_email_status == 'TAKEN':
        #     self.email_is_taken.grid(row=12, column=1, padx=5, sticky='e')
        #     self.password_entry.delete(0, END)
        #     self.repeat_password_entry.delete(0, END)
        # if self.incoming_context.sign_up_passwords_status == 'EMPTY':
        #     self.passwords_are_empty.grid(row=24, column=1, padx=5, sticky='e')
        #     self.password_entry.delete(0, END)
        #     self.repeat_password_entry.delete(0, END)
        # if self.incoming_context.sign_up_passwords_status == 'MISMATCH':
        #     self.passwords_mismatch.grid(row=24, column=1, padx=5, sticky='e')
        #     self.password_entry.delete(0, END)
        #     self.repeat_password_entry.delete(0, END)
        # if (self.incoming_context.sign_up_email_status == 'DEFAULT' and
        #         self.incoming_context.sign_up_passwords_status == 'DEFAULT'):
        #     self.email_entry.delete(0, END)
        #     self.password_entry.delete(0, END)
        #     self.repeat_password_entry.delete(0, END)
        # self.context = self.incoming_context

    def on_submit(self):
        """Read user Sign Up form and if its validation was successful, send all data to the Terminal"""

        self.login_is_empty.grid_remove()
        self.login_is_taken.grid_remove()
        self.passwords_are_empty.grid_remove()
        self.passwords_mismatch.grid_remove()
        self.signup_success.grid_remove()

        login = self.login_entry.get()
        password = self.password_entry.get()
        repeat_password = self.repeat_password_entry.get()
        if self.context.check_signup_form(login, password, repeat_password):
            self.login_entry.delete(0, END)
            self.password_entry.delete(0, END)
            self.repeat_password_entry.delete(0, END)
            action = ('SIGNUP', login, password, repeat_password)
            self.terminal.mail.put(('SEND', action))
        else:
            if not login:
                self.login_is_empty.grid(row=12, column=1, padx=5, sticky='e')
            if not password or not repeat_password:
                self.passwords_are_empty.grid(row=24, column=1, padx=5, sticky='e')
                self.password_entry.delete(0, END)
                self.repeat_password_entry.delete(0, END)
            elif password != repeat_password:
                self.passwords_mismatch.grid(row=24, column=1, padx=5, sticky='e')
                self.password_entry.delete(0, END)
                self.repeat_password_entry.delete(0, END)

    def on_back(self):
        """Schedule CHANGE_TO_SIGN_IN event."""
        self.master.event_generate('<<CHANGE_TO_SIGN_IN>>')
