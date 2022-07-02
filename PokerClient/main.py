import threading
import queue

import client_terminal
from tkinter import *
from tkinter import ttk
import datapack.no_connection_context
import guipack.no_connection_mainframe
import guipack.auth.mainframe
import guipack.menu.mainframe
import guipack.game.mainframe

"""Launch Poker Client application for specified IP-address of a machine, which runs Poker Server and for specified 
port to knock to. Note that you shall not pass these values as an argument. You need to set them in the main.py code 
directly. """


class Gui(Tk):
    """Main class of Poker Client application. Inherits tkinter.Tk."""

    def __init__(self):
        """Construct Poker Client Gui object."""

        super().__init__()
        self.mail = queue.Queue()

        self.terminal = client_terminal.ClientTerminal(self, '25.69.43.137', 5555, 5555)
        self.terminal_thread = threading.Thread(target=self.terminal.run)

        self.context = datapack.no_connection_context.NoConnectionContext()
        self.incoming_context = None
        self.mainframe = guipack.no_connection_mainframe.NoConnectionMainframe(self)
        self.mainframe.grid()
        self.resizable(False, False)

        self.terminal_thread.start()
        self.after(50, self.check_mail)
        self.protocol('WM_DELETE_WINDOW', self.on_destroy)

    def check_mail(self):
        """Method for checking Gui object mail. Self-schedules itself in Gui event-loop."""
        while not self.mail.empty():
            msg = self.mail.get()
            self.process(msg)
        self.after(50, self.check_mail)

    def process(self, msg):
        """Process incoming message.

        :param msg: Incoming message.
        """
        cmd, *args = msg
        if cmd == 'NEW_CONTEXT':
            self.incoming_context = args[0]
            self.update_context()
        elif cmd == 'CONNECTION_LOST':
            self.incoming_context = datapack.no_connection_context.NoConnectionContext()
            self.update_context()

    def update_context(self):
        """Method for updating current Gui object context."""

        if self.incoming_context.name != self.context.name:
            self.mainframe.destroy()
            if self.incoming_context.name == 'NO_CONNECTION':
                self.mainframe = guipack.no_connection_mainframe.NoConnectionMainframe(self)
            elif self.incoming_context.name == 'AUTH':
                self.mainframe = guipack.auth.mainframe.Mainframe(self, self.terminal, self.incoming_context)
            elif self.incoming_context.name == 'MENU':
                self.mainframe = guipack.menu.mainframe.Mainframe(self, self.terminal, self.incoming_context)
            elif self.incoming_context.name == 'GAME':
                self.mainframe = guipack.game.mainframe.Mainframe(self, self.terminal, self.incoming_context)
            self.mainframe.grid()
        else:
            self.mainframe.incoming_context = self.incoming_context
            self.mainframe.context_update()
        self.context = self.incoming_context
        self.incoming_context = None

    def on_destroy(self):
        """Intercepts Gui object WM_DELETE_WINDOW event. Sets everything to get application ready for termination."""
        self.terminal.mail.put(('DESTROY',))
        self.terminal_thread.join()
        self.destroy()


if __name__ == '__main__':
    """Poker Client main script entry point."""

    gui = Gui()
    gui.mainloop()
