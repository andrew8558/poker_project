from tkinter import *
from tkinter import ttk


class DirectSubframe(ttk.Frame):
    """ Class describing Direct subframe of the Menu mainframe."""

    def __init__(self, master, terminal, context):
        """ Construct Direct subframe

        :param master: Master widget.
        :param terminal: Client terminal object.
        :param context: Authorization Context object.
        """

        super().__init__(master)
        self.terminal = terminal

        self.context = context
        self.incoming_context = None

        self.frame = ttk.Frame(self)
        self.id_label = ttk.Label(self.frame, text='Room ID:')
        self.id_entry = ttk.Entry(self.frame, width=15)
        self.stack_label = ttk.Label(self.frame, text='Enter stack:')
        self.stack_entry = ttk.Entry(self.frame, width=15)
        self.connect_button = ttk.Button(self.frame, text='Connect', command=self.on_connect)

        self.id_label.grid(row=0, column=0, padx=15, pady=15)
        self.id_entry.grid(row=0, column=1, padx=15, pady=15)
        self.stack_label.grid(row=10, column=0, padx=15, pady=15)
        self.stack_entry.grid(row=10, column=1, padx=15, pady=15)
        self.connect_button.grid(row=20, column=0, columnspan=2, padx=15, pady=15)
        self.frame.grid(padx=10, pady=10)

    def context_update(self):
        """Method for updating current object context."""

        self.context = self.incoming_context
        self.incoming_context = None

    def on_connect(self):
        """Read user Connect to Room form and if its validation was successful, send all data to the Terminal"""

        try:
            id = int(self.id_entry.get())
            stack = int(self.stack_entry.get())
            if self.context.check_connect_form(id, stack):
                action = ('CONNECT', id, stack)
                self.terminal.mail.put(('SEND', action))
        except Exception:
            pass
