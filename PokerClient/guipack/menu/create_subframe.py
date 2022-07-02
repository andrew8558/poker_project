from tkinter import *
from tkinter import ttk


class CreateSubframe(ttk.Frame):
    """ Class describing Create subframe of the Menu mainframe."""

    def __init__(self, master, terminal, context):
        """ Construct Create subframe

        :param master: Master widget.
        :param terminal: Client terminal object.
        :param context: Authorization Context object.
        """

        super().__init__(master)
        self.terminal = terminal

        self.context = context
        self.incoming_context = None

        self.frame = ttk.Frame(self)
        self.blind_label = ttk.Label(self.frame, text='Blind Size:')
        self.blind_entry = ttk.Entry(self.frame, width=15)
        self.stack_label = ttk.Label(self.frame, text='Enter stack:')
        self.stack_entry = ttk.Entry(self.frame, width=15)
        self.create_button = ttk.Button(self.frame, text='Create', command=self.on_create)

        self.blind_label.grid(row=0, column=0, padx=15, pady=15)
        self.blind_entry.grid(row=0, column=1, padx=15, pady=15)
        self.stack_label.grid(row=10, column=0, padx=15, pady=15)
        self.stack_entry.grid(row=10, column=1, padx=15, pady=15)
        self.create_button.grid(row=20, column=0, columnspan=2, padx=15, pady=15)
        self.frame.grid(padx=10, pady=10)

    def context_update(self):
        """Method for updating current object context."""

        self.context = self.incoming_context
        self.incoming_context = None

    def on_create(self):
        """Read user Create Room form and if its validation was successful, send all data to the Terminal"""

        try:
            blind = int(self.blind_entry.get())
            stack = int(self.stack_entry.get())
            if self.context.check_create_form(blind, stack):
                action = ('CREATE', blind, stack)
                self.terminal.mail.put(('SEND', action))
        except Exception:
            pass
