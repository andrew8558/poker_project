from tkinter import *
from tkinter import ttk


class ActionsSubframe(ttk.Frame):
    """ Class describing Action subframe of the Game mainframe."""

    def __init__(self, master, terminal, context):
        """ Construct Actions Subframe.

        :param master: Master widget.
        :param terminal: Client terminal object.
        :param context: Authorization context object.
        """

        super().__init__(master, relief=SOLID, borderwidth=5)

        self.terminal = terminal
        self.context = context
        self.incoming_context = None

        self.ready_checkbutton_cv = IntVar()
        self.ready_checkbutton = ttk.Checkbutton(self, text='Ready', command=self.on_change,
                                                 variable=self.ready_checkbutton_cv)
        self.add_chips_entry = ttk.Entry(self)
        self.add_chips_button = ttk.Button(self, text='Add chips', command=self.on_add_chips)

        self.bet_var = StringVar()
        self.bet_scale = \
            ttk.Scale(self, orient=HORIZONTAL, length=200, from_=0.0, to=1.0, variable=self.bet_var,
                      command=self.on_scale)
        self.bet_value_label = ttk.Label(self, text=0)
        self.call_or_check_button = ttk.Button(self, text='Call', command=self.on_call_or_check)
        self.raise_x2_button = ttk.Button(self, text='Raise(x2)', command=self.on_raise_x2)
        self.all_or_knock_button = ttk.Button(self, text='All in!', command=self.on_all_or_knock)
        self.bet_button = ttk.Button(self, text='Bet', command=self.on_bet)
        self.fold_button = ttk.Button(self, text='Fold', command=self.on_fold)

        self.bet_scale.configure(state=DISABLED)
        self.call_or_check_button.configure(state=DISABLED)
        self.raise_x2_button.configure(state=DISABLED)
        self.all_or_knock_button.configure(state=DISABLED)
        self.bet_button.configure(state=DISABLED)
        self.fold_button.configure(state=DISABLED)

        self.ready_checkbutton.grid(row=0, column=0, padx=5, pady=5)
        self.add_chips_entry.grid(row=10, column=0, columnspan=2, padx=5, pady=5)
        self.add_chips_button.grid(row=10, column=2, padx=5, pady=5)

    def context_update(self):
        """Method for updating current object context."""

        if self.incoming_context.game_state.stage != 'WAITING':
            if self.context.game_state.stage == 'WAITING':
                self.add_chips_entry.grid_remove()
                self.add_chips_button.grid_remove()
                self.call_or_check_button.grid(row=10, column=0, padx=5, pady=5)
                self.raise_x2_button.grid(row=10, column=1, padx=5, pady=5)
                self.all_or_knock_button.grid(row=10, column=2, padx=5, pady=5)
                self.bet_value_label.grid(row=11, column=0, padx=5, pady=5)
                self.bet_scale.grid(row=11, column=1, columnspan=2, padx=5, pady=5)
                self.bet_button.grid(row=12, column=0, columnspan=3, padx=5, pady=5)
                self.fold_button.grid(row=20, column=0, columnspan=3, padx=5, pady=5)

            if self.incoming_context.player_dict['me'].time_st:
                opponents_bet = \
                    self.incoming_context.player_dict['opponent'].bet if self.incoming_context.player_dict['opponent'].bet else 0
                opponents_stack = \
                    self.incoming_context.player_dict['opponent'].stack if self.incoming_context.player_dict['opponent'].stack else 0
                my_bet = self.incoming_context.player_dict['me'].bet if self.incoming_context.player_dict['me'].bet else 0
                my_stack = self.incoming_context.player_dict['me'].stack if self.incoming_context.player_dict['me'].stack else 0

                condition = opponents_bet == 0 or \
                            self.incoming_context.game_state.stage == 'PREFLOP' and \
                            self.incoming_context.game_state.dealer.account.login != self.context.account.login and\
                            opponents_bet == self.context.game_state.blind_size
                if condition:
                    self.call_or_check_button.configure(text='Check')
                else:
                    self.call_or_check_button.configure(text='Call')
                if opponents_bet < my_stack:
                    self.call_or_check_button.configure(state=NORMAL)
                else:
                    self.call_or_check_button.configure(state=DISABLED)

                condition = 2 * opponents_bet - my_bet <= my_stack and 2 * opponents_bet - my_bet <= opponents_stack
                if condition:
                    self.raise_x2_button.configure(state=NORMAL)
                else:
                    self.raise_x2_button.configure(state=DISABLED)

                if my_stack + my_bet > opponents_stack + opponents_bet:
                    self.all_or_knock_button.configure(text='Knock')
                    if opponents_bet >= opponents_stack:
                        self.all_or_knock_button.configure(state=DISABLED)
                    else:
                        self.all_or_knock_button.configure(state=NORMAL)
                else:
                    self.all_or_knock_button.configure(text='All in!')
                    self.all_or_knock_button.configure(state=NORMAL)

                self.bet_var.set(0)
                self.bet_value_label.configure(text=0)
                self.bet_scale.configure(state=NORMAL)
                self.bet_button.configure(state=NORMAL)
                self.fold_button.configure(state=NORMAL)
        else:
            self.call_or_check_button.grid_remove()
            self.raise_x2_button.grid_remove()
            self.all_or_knock_button.grid_remove()
            self.bet_value_label.grid_remove()
            self.bet_scale.grid_remove()
            self.bet_button.grid_remove()
            self.fold_button.grid_remove()

            if self.incoming_context.game_state.stage == 'WAITING':
                self.add_chips_entry.grid(row=10, column=0, columnspan=2, padx=5, pady=5)
                self.add_chips_button.grid(row=10, column=2, padx=5, pady=5)

                if self.incoming_context.player_dict['me'].able:
                    self.ready_checkbutton.configure(state=NORMAL)
                else:
                    self.ready_checkbutton.configure(state=DISABLED)

                if self.incoming_context.player_dict['me'].ready:
                    self.ready_checkbutton_cv.set(1)
                else:
                    self.ready_checkbutton_cv.set(0)

        self.context = self.incoming_context
        self.incoming_context = None

    def on_change(self):
        """Read change ready-status form and send it to the Terminal"""

        if self.ready_checkbutton_cv.get() == 0:
            action = ('NOT_READY',)
        else:
            action = ('READY',)
        self.terminal.mail.put(('SEND', action))

    def on_call_or_check(self):
        """Read click-on-call-or-check-button and update game screen."""

        opponents_bet = self.context.player_dict['opponent'].bet if self.context.player_dict['opponent'].bet else 0
        my_stack = self.context.player_dict['me'].stack if self.context.player_dict['me'].stack else 0
        my_bet = self.context.player_dict['me'].bet if self.context.player_dict['me'].bet else 0
        self.bet_var.set((opponents_bet - my_bet) / my_stack)
        self.bet_value_label.configure(text=int(float(self.bet_var.get()) * my_stack))
        bet = self.context.player_dict['me'].bet if self.context.player_dict['me'].bet else 0
        bet += int(self.bet_value_label.cget('text'))
        if self.context.check_bet_form(bet):
            self.bet_button.configure(state=NORMAL)
        else:
            self.bet_button.configure(state=DISABLED)

    def on_raise_x2(self):
        """Read click-on-raise-x2-button and update game screen."""

        opponents_bet = self.context.player_dict['opponent'].bet if self.context.player_dict['opponent'].bet else 0
        my_stack = self.context.player_dict['me'].stack if self.context.player_dict['me'].stack else 0
        my_bet = self.context.player_dict['me'].bet if self.context.player_dict['me'].bet else 0
        self.bet_var.set((2 * opponents_bet - my_bet) / my_stack)
        self.bet_value_label.configure(text=int(float(self.bet_var.get()) * my_stack))
        bet = self.context.player_dict['me'].bet if self.context.player_dict['me'].bet else 0
        bet += int(self.bet_value_label.cget('text'))
        if self.context.check_bet_form(bet):
            self.bet_button.configure(state=NORMAL)
        else:
            self.bet_button.configure(state=DISABLED)

    def on_all_or_knock(self):
        """Read click-on-all-or-knock-button and update game screen."""

        opponents_bet = self.context.player_dict['opponent'].bet if self.context.player_dict['opponent'].bet else 0
        my_stack = self.context.player_dict['me'].stack if self.context.player_dict['me'].stack else 0
        opponents_stack = self.context.player_dict['opponent'].stack if self.context.player_dict[
            'opponent'].stack else 0
        my_bet = self.context.player_dict['me'].bet if self.context.player_dict['me'].bet else 0
        if self.all_or_knock_button.cget('text') == 'All in!':
            self.bet_var.set(my_stack / my_stack)
        else:
            self.bet_var.set((opponents_stack + opponents_bet - my_bet) / my_stack)
        self.bet_value_label.configure(text=int(float(self.bet_var.get()) * my_stack))
        bet = self.context.player_dict['me'].bet if self.context.player_dict['me'].bet else 0
        bet += int(self.bet_value_label.cget('text'))
        if self.context.check_bet_form(bet):
            self.bet_button.configure(state=NORMAL)
        else:
            self.bet_button.configure(state=DISABLED)

    def on_scale(self, val):
        """Read user actions with Scale widget and update game screen."""

        my_stack = self.context.player_dict['me'].stack if self.context.player_dict['me'].stack else 0
        self.bet_var.set(val)
        self.bet_value_label.configure(text=int(float(self.bet_var.get()) * my_stack))
        bet = self.context.player_dict['me'].bet if self.context.player_dict['me'].bet else 0
        bet += int(self.bet_value_label.cget('text'))
        if self.context.check_bet_form(bet):
            self.bet_button.configure(state=NORMAL)
        else:
            self.bet_button.configure(state=DISABLED)

    def on_bet(self):
        """Read user Bet form and if its validation was successful, send all data to the Terminal"""

        bet = self.context.player_dict['me'].bet if self.context.player_dict['me'].bet else 0
        bet += int(self.bet_value_label.cget('text'))
        try:
            bet = int(bet)
            if self.context.check_bet_form(bet):
                action = ('BET', bet)
                self.terminal.mail.put(('SEND', action))
                self.call_or_check_button.configure(state=DISABLED)
                self.call_or_check_button.configure(state=DISABLED)
                self.raise_x2_button.configure(state=DISABLED)
                self.all_or_knock_button.configure(state=DISABLED)
                self.bet_scale.configure(state=DISABLED)
                self.bet_button.configure(state=DISABLED)
                self.fold_button.configure(state=DISABLED)
        except Exception:
            pass

    def on_add_chips(self):
        """Read user Add Chips form and if its validation was successful, send all data to the Terminal"""

        chips = self.add_chips_entry.get()
        try:
            chips = int(chips)
            if self.context.check_add_chips_form(chips):
                self.add_chips_entry.delete(0, END)
                action = ('ADD_CHIPS', chips)
                self.terminal.mail.put(('SEND', action))
        except Exception:
            pass

    def on_fold(self):
        """Read user Bet form and if its validation was successful, send all data to the Terminal"""

        if self.context.check_fold_form():
            action = ('FOLD',)
            self.terminal.mail.put(('SEND', action))
            self.call_or_check_button.configure(state=DISABLED)
            self.raise_x2_button.configure(state=DISABLED)
            self.all_or_knock_button.configure(state=DISABLED)
            self.bet_scale.configure(state=DISABLED)
            self.bet_button.configure(state=DISABLED)
            self.fold_button.configure(state=DISABLED)
