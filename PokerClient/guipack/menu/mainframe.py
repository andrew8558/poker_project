from tkinter import *
from tkinter import ttk
import guipack.menu.account_subframe
import guipack.menu.direct_subframe
import guipack.menu.create_subframe


class Mainframe(ttk.Frame):
    """Class describing mainframe in Menu Context."""

    def __init__(self, master, terminal, context):
        """ Construct Menu Mainframe.

        :param master: Master widget.
        :param terminal: Client terminal object.
        :param context: Authorization context object.
        """

        super().__init__(master)
        self.terminal = terminal

        self.context = context
        self.incoming_context = None

        self.account_button = ttk.Button(self, text='Account', command=self.on_account)
        self.direct_button = ttk.Button(self, text='Direct', command=self.on_direct)
        self.create_button = ttk.Button(self, text='Create', command=self.on_create)
        self.account = guipack.menu.account_subframe.AccountSubframe(self, self.terminal, self.context)
        self.direct = guipack.menu.direct_subframe.DirectSubframe(self, self.terminal, self.context)
        self.create = guipack.menu.create_subframe.CreateSubframe(self, self.terminal, self.context)

        self.account_button.grid(row=0, column=0, sticky='we')
        self.direct_button.grid(row=0, column=1, sticky='we')
        self.create_button.grid(row=0, column=2, sticky='we')
        self.account.grid(row=1, column=0, columnspan=3, sticky='nswe')

    def context_update(self):
        """Method for updating current object context."""

        self.account.incoming_context = self.incoming_context
        self.direct.incoming_context = self.incoming_context
        self.create.incoming_context = self.incoming_context
        self.account.context_update()
        self.direct.context_update()
        self.create.context_update()
        self.context = self.incoming_context
        self.incoming_context = None

    def on_account(self):
        """Display Account subframe"""

        self.create.grid_remove()
        self.direct.grid_remove()
        self.account.grid(row=1, column=0, columnspan=3, sticky='nswe')

    def on_direct(self):
        """Display Direct subframe"""

        self.account.grid_remove()
        self.create.grid_remove()
        self.direct.grid(row=1, column=0, columnspan=3, sticky='nswe')

    def on_create(self):
        """Display Create subframe"""

        self.account.grid_remove()
        self.direct.grid_remove()
        self.create.grid(row=1, column=0, columnspan=3, sticky='nswe')
