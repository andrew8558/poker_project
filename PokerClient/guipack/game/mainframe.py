from tkinter import *
from tkinter import ttk
import os
import guipack.game.player_subframe
import guipack.game.actions_subframe
import guipack.game.board_subframe


class Mainframe(ttk.Frame):
    """Class describing mainframe in Game Context."""

    def __init__(self, master, terminal, context):
        """ Construct Game Mainframe.

        :param master: Master widget.
        :param terminal: Client terminal object.
        :param context: Authorization context object.
        """

        super().__init__(master)

        self.terminal = terminal
        self.context = context
        self.incoming_context = None

        self.canvas_w = 1200
        self.canvas_h = 900
        self.canvas = Canvas(self, width=self.canvas_w, height=self.canvas_h)

        path = os.path.dirname(__file__)
        self.table_img = PhotoImage(file=os.path.join(path, '../../resources/Stol_bez_mest.png'))

        self.leave_button = Button(self.canvas, text='Leave', font=72, borderwidth=5, command=self.on_leave)
        self.room_id_label = Label(self.canvas, text=f'{self.context.table_id}', font=72, relief=SOLID, borderwidth=5)
        self.board_sub = guipack.game.board_subframe.BoardSubframe(self.canvas, terminal, context, self.canvas_w, self.canvas_h)
        self.me_sub = guipack.game.player_subframe.PlayerSubframe(self.canvas, terminal, context, 'me')
        self.opponent_sub = guipack.game.player_subframe.PlayerSubframe(self.canvas, terminal, context, 'opponent')
        self.actions_sub = guipack.game.actions_subframe.ActionsSubframe(self.canvas, terminal, context)

        tmp = self.canvas.create_image(self.canvas_w // 2, self.canvas_h // 2, image=self.table_img, anchor=CENTER)
        self.canvas.tag_lower(tmp)
        self.canvas.create_window(self.canvas_w // 15, self.canvas_h // 20, window=self.leave_button, anchor=CENTER)
        self.canvas.create_window(self.canvas_w // 15 * 14, self.canvas_h // 20, window=self.room_id_label, anchor=CENTER)
        self.canvas.create_window(self.canvas_w // 2, self.canvas_h // 7, window=self.opponent_sub, anchor=CENTER)
        self.opponent_sub.lower()
        self.opponent_sub.lower()
        self.canvas.create_window(self.canvas_w // 2, self.canvas_h // 7 * 6, window=self.me_sub, anchor=CENTER)
        self.me_sub.lower()
        self.me_sub.lower()
        self.canvas.create_window(self.canvas_w // 5 * 4, self.canvas_h // 6 * 5, window=self.actions_sub, anchor=CENTER)
        self.canvas.grid()

    def context_update(self):
        """Method for updating current object context."""

        self.board_sub.incoming_context = self.incoming_context
        self.me_sub.incoming_context = self.incoming_context
        self.opponent_sub.incoming_context = self.incoming_context
        self.actions_sub.incoming_context = self.incoming_context

        self.board_sub.context_update()
        self.me_sub.context_update()
        self.opponent_sub.context_update()
        self.actions_sub.context_update()

        self.context = self.incoming_context
        self.incoming_context = None

    def on_leave(self):
        """Read user Leave form and send all data to the Terminal"""

        action = ('DISCONNECT',)
        self.terminal.mail.put(('SEND', action))
