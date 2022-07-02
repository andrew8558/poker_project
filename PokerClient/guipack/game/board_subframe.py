from tkinter import *
from tkinter import ttk
import os
import guipack.game.ready_timer
import guipack.game.img_parser


class BoardSubframe(ttk.Frame):
    """Class describing Board subframe in Game Context."""

    def __init__(self, master, terminal, context, canvas_w, canvas_h):
        """ Construct Board subframe

        :param master: Master widget.
        :param terminal: Client terminal object.
        :param context: Authorization Context object.
        :param canvas_w: Width of surrounding Canvas widget.
        :param canvas_h: Height of surrounding Canvas widget.
        """

        super().__init__(master)

        self.terminal = terminal
        self.context = context
        self.incoming_context = None
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.canvas = master

        self.wmd_dict = {}

        path = os.path.dirname(__file__)
        self.dealer_img = PhotoImage(file=os.path.join(path, '../../resources/Fishka_Dilera_D.png'))
        self.my_bet_img = guipack.game.img_parser.parse_chips(0, 1)
        self.my_bet_label = ttk.Label(self.canvas, relief=SOLID, borderwidth=5)
        self.opponent_bet_img = guipack.game.img_parser.parse_chips(0, 1)
        self.opponent_bet_label = ttk.Label(self.canvas, relief=SOLID, borderwidth=5)
        self.pot_img = guipack.game.img_parser.parse_chips(0, 1)
        self.pot_label = ttk.Label(self.canvas, relief=SOLID, borderwidth=5)
        self.cards = [guipack.game.img_parser.parse_cards(None) for i in range(5)]
        self.ready_timer = guipack.game.ready_timer.ReadyTimer(self.canvas, terminal, context)

        self.wmd_dict['dealer_img'] = \
            self.canvas.create_image(0, 0, image=self.dealer_img, anchor=CENTER)
        self.canvas.itemconfigure(self.wmd_dict['dealer_img'], state=HIDDEN)

        self.wmd_dict['my_bet_img'] = \
            self.canvas.create_image(self.canvas_w // 2, self.canvas_h // 90 * 56, image=self.my_bet_img, anchor=CENTER)
        self.canvas.itemconfigure(self.wmd_dict['my_bet_img'], state=HIDDEN)
        self.wmd_dict['my_bet_label'] = \
            self.canvas.create_window(self.canvas_w // 2, self.canvas_h // 90 * 56, window=self.my_bet_label,
                                      anchor=CENTER)
        self.canvas.lift(self.wmd_dict['my_bet_label'])
        self.canvas.itemconfigure(self.wmd_dict['my_bet_label'], state=HIDDEN)

        self.wmd_dict['opponent_bet_img'] = \
            self.canvas.create_image(self.canvas_w // 2, self.canvas_h // 3, image=self.opponent_bet_img, anchor=CENTER)
        self.canvas.itemconfigure(self.wmd_dict['opponent_bet_img'], state=HIDDEN)
        self.wmd_dict['opponent_bet_label'] = \
            self.canvas.create_window(self.canvas_w // 2, self.canvas_h // 3, window=self.opponent_bet_label,
                                      anchor=CENTER)
        self.canvas.lift(self.wmd_dict['opponent_bet_label'])
        self.canvas.itemconfigure(self.wmd_dict['opponent_bet_label'], state=HIDDEN)

        self.wmd_dict['pot_img'] = \
            self.canvas.create_image(self.canvas_w // 24 * 7, self.canvas_h // 2, image=self.pot_img, anchor=CENTER)
        self.canvas.itemconfigure(self.wmd_dict['pot_img'], state=HIDDEN)
        self.wmd_dict['pot_label'] = \
            self.canvas.create_window(self.canvas_w // 24 * 7, self.canvas_h // 2, window=self.pot_label, anchor=CENTER)
        self.canvas.lift(self.wmd_dict['pot_label'])
        self.canvas.itemconfigure(self.wmd_dict['pot_label'], state=HIDDEN)
        for i, card in enumerate(self.cards):
            self.wmd_dict[f'card_{i}'] = \
                self.canvas.create_image(self.canvas_w // 30 * 11 + self.canvas_w // 15 * i, self.canvas_h // 2,
                                         image=card, anchor=CENTER)
            self.canvas.itemconfigure(self.wmd_dict[f'card_{i}'], state=HIDDEN)
        self.wmd_dict['ready_timer'] = \
            self.canvas.create_window(self.canvas_w // 2, self.canvas_h // 2, window=self.ready_timer, anchor=CENTER)
        self.canvas.itemconfigure(self.wmd_dict['ready_timer'], state=HIDDEN)

    def context_update(self):
        """Method for updating current object context."""

        if self.incoming_context.game_state.dealer:
            if self.incoming_context.game_state.dealer.account.login == self.context.player_dict['me'].account.login:
                self.canvas.coords(self.wmd_dict['dealer_img'], self.canvas_w // 8 * 5, self.canvas_h // 3 * 2)
            else:
                self.canvas.coords(self.wmd_dict['dealer_img'], self.canvas_w // 8 * 5, self.canvas_h // 3)
        else:
            self.canvas.itemconfigure(self.wmd_dict['dealer_img'], state=HIDDEN)

        if self.incoming_context.game_state.stage == 'WAITING':
            if self.context.game_state.stage != 'WAITING':
                self.canvas.itemconfigure(self.wmd_dict['my_bet_img'], state=HIDDEN)
                self.canvas.itemconfigure(self.wmd_dict['my_bet_label'], state=HIDDEN)
                self.canvas.itemconfigure(self.wmd_dict['opponent_bet_img'], state=HIDDEN)
                self.canvas.itemconfigure(self.wmd_dict['opponent_bet_label'], state=HIDDEN)
                self.canvas.itemconfigure(self.wmd_dict['pot_img'], state=HIDDEN)
                self.canvas.itemconfigure(self.wmd_dict['pot_label'], state=HIDDEN)
                for i, card in enumerate(self.cards):
                    self.cards[i] = guipack.game.img_parser.parse_cards(None)
                    self.canvas.itemconfigure(self.wmd_dict[f'card_{i}'], image=self.cards[i])
                    self.canvas.itemconfigure(self.wmd_dict[f'card_{i}'], state=HIDDEN)

            self.ready_timer.incoming_context = self.incoming_context
            self.ready_timer.context_update()
            if self.incoming_context.game_state.time_ready_st:
                self.canvas.itemconfigure(self.wmd_dict['ready_timer'], state=NORMAL)
            else:
                self.canvas.itemconfigure(self.wmd_dict['ready_timer'], state=HIDDEN)
        else:
            if self.context.game_state.stage == 'WAITING':
                self.ready_timer.incoming_context = self.incoming_context
                self.ready_timer.context_update()
                self.canvas.itemconfigure(self.wmd_dict['dealer_img'], state=NORMAL)
                self.canvas.itemconfigure(self.wmd_dict['ready_timer'], state=HIDDEN)
                self.canvas.itemconfigure(self.wmd_dict['my_bet_img'], state=NORMAL)
                self.canvas.itemconfigure(self.wmd_dict['my_bet_label'], state=NORMAL)
                self.canvas.itemconfigure(self.wmd_dict['opponent_bet_img'], state=NORMAL)
                self.canvas.itemconfigure(self.wmd_dict['opponent_bet_label'], state=NORMAL)
                self.canvas.itemconfigure(self.wmd_dict['pot_img'], state=NORMAL)
                self.canvas.itemconfigure(self.wmd_dict['pot_label'], state=NORMAL)
                for i, card in enumerate(self.cards):
                    self.canvas.itemconfigure(self.wmd_dict[f'card_{i}'], state=NORMAL)
                if self.incoming_context.game_state.dealer.account.login == self.context.player_dict[
                    'me'].account.login:
                    self.canvas.coords(self.wmd_dict['dealer_img'], self.canvas_w // 8 * 5, self.canvas_h // 3 * 2)
                else:
                    self.canvas.coords(self.wmd_dict['dealer_img'], self.canvas_w // 8 * 5, self.canvas_h // 3)

            blind = self.incoming_context.game_state.blind_size
            my_bet_val = self.incoming_context.player_dict['me'].bet if self.incoming_context.player_dict[
                'me'].bet else 0
            self.my_bet_img = guipack.game.img_parser.parse_chips(my_bet_val, blind)
            self.canvas.itemconfigure(self.wmd_dict['my_bet_img'], image=self.my_bet_img)
            self.my_bet_label.configure(text=str(my_bet_val))
            opponent_bet_val = self.incoming_context.player_dict['opponent'].bet if self.incoming_context.player_dict[
                'opponent'].bet else 0
            self.opponent_bet_img = guipack.game.img_parser.parse_chips(opponent_bet_val, blind)
            self.canvas.itemconfigure(self.wmd_dict['opponent_bet_img'], image=self.opponent_bet_img)
            self.opponent_bet_label.configure(text=str(opponent_bet_val))
            pot_val = self.incoming_context.game_state.pot if self.incoming_context.game_state.pot else 0
            self.pot_img = guipack.game.img_parser.parse_chips(pot_val, blind)
            self.canvas.itemconfigure(self.wmd_dict['pot_img'], image=self.pot_img)
            self.pot_label.configure(text=str(pot_val))

            if self.incoming_context.game_state.board:
                card_vals = self.incoming_context.game_state.board.split(' ')
                for i, card_val in enumerate(card_vals):
                    self.cards[i] = guipack.game.img_parser.parse_cards(card_val)
                    self.canvas.itemconfigure(self.wmd_dict[f'card_{i}'], image=self.cards[i])

        self.context = self.incoming_context
        self.incoming_context = None
