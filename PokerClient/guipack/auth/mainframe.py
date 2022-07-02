from tkinter import *
from tkinter import ttk
import guipack.auth.sign_in_subframe
import guipack.auth.sign_up_subframe


class Mainframe(ttk.Frame):
    """Class describing mainframe in Authorization Context."""

    def __init__(self, master, terminal, context):
        """ Construct Authorization Mainframe.

        :param master: Master widget.
        :param terminal: Client terminal object.
        :param context: Authorization context object.
        """

        super().__init__(master)
        self.terminal = terminal

        self.context = context
        self.incoming_context = None

        self.sign_in = guipack.auth.sign_in_subframe.SignInSubframe(self, self.terminal, self.context)
        self.sign_up = guipack.auth.sign_up_subframe.SignUpSubframe(self, self.terminal, self.context)

        self.sign_in.grid()

        self.bind('<<CHANGE_TO_SIGN_IN>>', self.on_change_to_sign_in)
        self.bind('<<CHANGE_TO_SIGN_UP>>', self.on_change_to_sign_up)

    def context_update(self):
        """Method for updating current object context."""

        self.sign_in.incoming_context = self.incoming_context
        self.sign_up.incoming_context = self.incoming_context
        self.sign_in.context_update()
        self.sign_up.context_update()
        self.context = self.incoming_context
        self.incoming_context = None

    def on_change_to_sign_in(self, event):
        """Hide Sign Up subframe and show Sign In subframe."""

        self.sign_up.grid_remove()
        self.sign_in.grid()

    def on_change_to_sign_up(self, event):
        """Hide Sign In subframe and show Sign Up subframe."""

        self.sign_in.grid_remove()
        self.sign_up.grid()
