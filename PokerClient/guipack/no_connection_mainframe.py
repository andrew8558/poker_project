from tkinter import ttk


class NoConnectionMainframe(ttk.Frame):
    """Class describing Mainframe of No Connection Context."""

    def __init__(self, master):
        super().__init__(master)
        self.label = ttk.Label(self, text='No Connection!')
        self.label.grid(padx=120, pady=80)
