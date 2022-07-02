from tkinter import *
from tkinter import ttk
import time


class ReadyTimer(ttk.Frame):
    """Class, describing Ready Timer frame."""

    def __init__(self, master, terminal, context):
        """Construct Ready Timer frame.

        :param master: Master widget.
        :param terminal: Client Terminal.
        :param context: Game Context object.
        """

        super().__init__(master, relief=SOLID, borderwidth=5)
        self.terminal = terminal

        self.context = context
        self.incoming_context = None

        self.frame = ttk.Frame(self)
        self.timer = ttk.Label(self.frame, font=72)

        self.timer.grid()
        self.frame.grid()

    def context_update(self):
        """Method for updating current object context."""

        if self.incoming_context.game_state.time_ready_st:
            cur = time.time()
            new_text = '{:.1f}'.format(8.0 - (cur - self.incoming_context.game_state.time_ready_st))
            self.timer.configure(text=new_text)
            self.after(100, self.tick)
        else:
            self.timer.configure(text='')
        self.context = self.incoming_context
        self.incoming_context = None

    def tick(self):
        """Self-scheduling method, that updates time left on the timer."""

        if self.context.game_state.time_ready_st:
            cur = time.time()
            if 8.0 - (cur - self.context.game_state.time_ready_st) > 0.0:
                new_text = '{:.1f}'.format(8.0 - (cur - self.context.game_state.time_ready_st))
                self.timer.configure(text=new_text)
                self.after(100, self.tick)
            else:
                self.timer.configure(text='0.0')