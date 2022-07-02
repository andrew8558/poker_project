from tkinter import *
from tkinter import ttk
import time


class TurnTimer(ttk.Frame):
    """Class, describing Turn Timer frame."""

    def __init__(self, master, terminal, context, str_p):
        """Construct Turn Timer frame.

        :param master: Master widget.
        :param terminal: Client Terminal.
        :param context: Game Context object.
        :param str_p: Player codename in player_dict field of Game Context object.
        """

        super().__init__(master)
        self.terminal = terminal

        self.context = context
        self.incoming_context = None
        self.str_p = str_p

        self.frame = ttk.Frame(self)
        self.timer = ttk.Label(self.frame)

        self.timer.grid()
        self.frame.grid()

    def context_update(self):
        """Method for updating current object context."""
        myself = self.incoming_context.player_dict[self.str_p]
        if myself and myself.time_st:
            cur = time.time()
            new_text = '{:.1f}'.format(25.0 - (cur - myself.time_st))
            self.timer.configure(text=new_text)
            self.after(100, self.tick)
        else:
            self.timer.configure(text='')
        self.context = self.incoming_context
        self.incoming_context = None

    def tick(self):
        """Self-scheduling method, that updates time left on the timer."""
        myself = self.context.player_dict[self.str_p]
        if myself and myself.time_st:
            cur = time.time()
            if 25.0 - (cur - myself.time_st) > 0.0:
                new_text = '{:.1f}'.format(25.0 - (cur - myself.time_st))
                self.timer.configure(text=new_text)
                self.after(100, self.tick)
            else:
                self.timer.configure(text='0.0')
