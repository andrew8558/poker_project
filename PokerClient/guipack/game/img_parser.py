from tkinter import *
import os


def parse_chips(val, blind):
    """Parse ratio of chips value and blind size with corresponding resource.

    :param val: Chips value
    :param blind: Blind size
    :return: tkinter.PhotoImage object of corresponding resource.
    """
    path = os.path.dirname(__file__)
    file = '../../resources/empty_chips.png'
    if 0 < val < 10 * blind:
        file = '../../resources/Odna_fishka.png'
    elif 10 * blind <= val < 40 * blind:
        file = '../../resources/Odna_stopka.png'
    elif 40 * blind <= val:
        file = '../../resources/3_stopki_fishek.png'
    return PhotoImage(file=os.path.join(path, file))


def parse_cards(val):
    """Parse card value with corresponding resource.

    :param val: Card value.
    :return: tkinter.PhotoImage object of corresponding resource.
    """

    path = os.path.dirname(__file__)
    file = '../../resources/cards/empty_card.png'
    if val:
        if val == '??':
            file = '../../resources/cards/facedown_card.png'
        else:
            rank = val[0]
            suit = val[1]
            rank_parsing = {
                '2': '2',
                '3': '3',
                '4': '4',
                '5': '5',
                '6': '6',
                '7': '7',
                '8': '8',
                '9': '9',
                'T': '10',
                'J': 'jack',
                'Q': 'queen',
                'K': 'king',
                'A': 'ace'
            }
            suit_parsing = {
                'S': 'of_spades',
                'H': 'of_hearts',
                'C': 'of_clubs',
                'D': 'of_diamonds'
            }
            file = f'../../resources/cards/{rank_parsing[rank]}_{suit_parsing[suit]}.png'
    return PhotoImage(file=os.path.join(path, file)).subsample(8, 8)
