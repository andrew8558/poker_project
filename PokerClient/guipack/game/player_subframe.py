from tkinter import *
from tkinter import ttk
import os
import guipack.game.img_parser
import guipack.game.turn_timer


class PlayerSubframe(ttk.Frame):
    """ Class describing Player subframe of the Game mainframe."""

    def __init__(self, master, terminal, context, str_p):
        """ Construct Player Subframe.

        :param master: Master widget.
        :param terminal: Client terminal object.
        :param context: Authorization context object.
        :param str_p: Player codename in player_dict field of Game Context object.
        """

        super().__init__(master, relief=SOLID, borderwidth=5)

        self.terminal = terminal
        self.context = context
        self.incoming_context = None
        self.str_p = str_p

        path = os.path.dirname(__file__)
        self.player_stack_img = guipack.game.img_parser.parse_chips(0, 1)
        self.player_hand1_img = guipack.game.img_parser.parse_cards(None)
        self.player_hand2_img = guipack.game.img_parser.parse_cards(None)

        self.player_name = ttk.Label(self)
        self.player_stack = ttk.Label(self, image=self.player_stack_img)
        self.player_stack_val = ttk.Label(self)
        self.player_hand1 = ttk.Label(self, image=self.player_hand1_img)
        self.player_hand2 = ttk.Label(self, image=self.player_hand2_img)
        self.player_ready = ttk.Label(self)
        self.turn_timer = guipack.game.turn_timer.TurnTimer(self, terminal, context, str_p)

        if self.context.player_dict[self.str_p]:
            self.player_name.configure(text=self.context.player_dict[self.str_p].account.login)
            if self.context.player_dict[self.str_p].stack:
                val = self.context.player_dict[self.str_p].stack
                blind = self.context.game_state.blind_size
                self.player_stack_img = guipack.game.img_parser.parse_chips(val, blind)
                self.player_stack.configure(image=self.player_stack_img)
                self.player_stack_val.configure(text=self.context.player_dict[self.str_p].stack)

            self.player_ready.configure(text='(Ready)' if self.context.player_dict[self.str_p].ready else '(Not Ready)')

        self.player_name.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.player_ready.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.player_stack.grid(row=2, column=0, padx=5, pady=5)
        self.player_stack_val.grid(row=3, column=0, padx=5, pady=5)
        self.player_hand1.grid(row=2, rowspan=2, column=1, padx=5, pady=5)
        self.player_hand2.grid(row=2, rowspan=2, column=2, padx=5, pady=5)
        self.turn_timer.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    def context_update(self):
        """Method for updating current object context."""

        self.turn_timer.incoming_context = self.incoming_context
        self.turn_timer.context_update()

        myself = self.incoming_context.player_dict[self.str_p]
        if myself:
            self.player_name.configure(text=myself.account.login)
            val = myself.stack
            blind = self.context.game_state.blind_size
            self.player_stack_img = guipack.game.img_parser.parse_chips(val, blind)
            self.player_stack.configure(image=self.player_stack_img)
            self.player_stack_val.configure(text=val)

            if myself.hand:
                hand_cards = myself.hand.split(' ')
                self.player_hand1_img = guipack.game.img_parser.parse_cards(hand_cards[0])
                self.player_hand2_img = guipack.game.img_parser.parse_cards(hand_cards[1])
                self.player_hand1.configure(image=self.player_hand1_img)
                self.player_hand2.configure(image=self.player_hand2_img)
            else:
                self.player_hand1_img = guipack.game.img_parser.parse_cards(None)
                self.player_hand2_img = guipack.game.img_parser.parse_cards(None)
                self.player_hand1.configure(image=self.player_hand1_img)
                self.player_hand2.configure(image=self.player_hand2_img)

            if myself.ready:
                self.player_ready.configure(text='(Ready)')
            else:
                self.player_ready.configure(text='(Not Ready)')
        else:
            self.player_name.configure(text='')
            val = 0
            blind = self.context.game_state.blind_size
            self.player_stack_img = guipack.game.img_parser.parse_chips(val, blind)
            self.player_stack.configure(image=self.player_stack_img)
            self.player_stack_val.configure(text='')
            self.player_hand1_img = guipack.game.img_parser.parse_cards(None)
            self.player_hand2_img = guipack.game.img_parser.parse_cards(None)
            self.player_hand1.configure(image=self.player_hand1_img)
            self.player_hand2.configure(image=self.player_hand2_img)
            self.player_ready.configure(text='')
        self.context = self.incoming_context
        self.incoming_context = None
