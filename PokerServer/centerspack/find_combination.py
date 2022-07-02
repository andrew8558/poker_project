hierarchy = {'1': 0,
             '2': 1,
             '3': 2,
             '4': 3,
             '5': 4,
             '6': 5,
             '7': 6,
             '8': 7,
             '9': 8,
             'T': 9,
             'J': 10,
             'Q': 11,
             'K': 12,
             'A': 13}
"""Dictionary where the key is a card, and the value is its rang"""


def combination(hand, table):
    """Looking for a player combination.

    Keyword arguments:
    hand -- player's hand
    table -- table's cards

    Returns a tuple meaning a combination.

    """
    hand = sorted(hand, key=lambda x: hierarchy[x[0]])
    card_set = hand + table
    card_set = sorted(card_set, key=lambda x: hierarchy[x[0]])
    flush_cards = check_flushness(card_set)
    if flush_cards:
        x = check_straight_flush(flush_cards)
        if x:
            return x
    same_cards = check_sameness(card_set)
    x = check_care(card_set)
    if x:
        return x
    x = check_full_house(same_cards)
    if x:
        return x
    if flush_cards:
        x = check_flush(flush_cards, hand)
        if x:
            return x
    x = check_straight(same_cards)
    if x:
        return x
    x = check_set(same_cards)
    if x:
        return x
    x = check_dopers(same_cards)
    if x:
        return x
    x = check_pair(same_cards)
    if x:
        return x
    x = check_high_card(card_set, hand)
    if x:
        return x


def check_flushness(card_set):
    """Checks a set of cards for the presence of a flash

    Keyword arguments:
    card_set -- list of player's cards and table's cards

    Returns boolean variable.
    """
    clubs = []
    diamonds = []
    hearts = []
    spades = []
    x = {'C': clubs, 'D': diamonds, 'H': hearts, 'S': spades}
    for card in card_set:
        card_suit = card[1]
        x[card_suit].append(card)
    for i in x.values():
        if len(i) >= 5:
            return i
    return False


def check_sameness(card_set):
    """Checks how many times a card of the same denomination is repeated.

    Keyword arguments:
    card_set -- list of player's cards and table's cards

    Returns dictionary where the key is the denomination of the cards and the value is how many times it is repeated.
    """
    twos = []
    threes = []
    fours = []
    fives = []
    sixes = []
    sevens = []
    eights = []
    nines = []
    tens = []
    jacks = []
    queens = []
    kings = []
    aces = []
    x = {'2': twos,
         '3': threes,
         '4': fours,
         '5': fives,
         '6': sixes,
         '7': sevens,
         '8': eights,
         '9': nines,
         'T': tens,
         'J': jacks,
         'Q': queens,
         'K': kings,
         'A': aces}
    for card in card_set:
        card_suit = card[0]
        x[card_suit].append(card)
    return x


def check_straight_flush(cards_set):
    """Checks whether a set of cards has a straight flush combination.

    Keyword arguments:
    card_set -- list of player's cards and table's cards

    Returns a tuple describing the combination
    """
    count = len(cards_set)
    for i in range(count-4):
        if (hierarchy[cards_set[count-i-1][0]] == hierarchy[cards_set[count-i-2][0]]+1 and
            hierarchy[cards_set[count-i-1][0]] == hierarchy[cards_set[count-i-3][0]]+2 and
            hierarchy[cards_set[count-i-1][0]] == hierarchy[cards_set[count-i-4][0]]+3 and
            hierarchy[cards_set[count-i-1][0]] == hierarchy[cards_set[count-i-5][0]]+4):
            return 9, hierarchy[cards_set[count-i-1][0]]
    if (cards_set[0][0] == '2' and
        cards_set[1][0] == '3' and
        cards_set[2][0] == '4' and
        cards_set[3][0] == '5' and
        cards_set[count-1][0] == 'A'):
        return 9, hierarchy[cards_set[3][0]]


def check_care(card_set):
    """Checks whether a set of cards has a care combination.

    Keyword arguments:
    card_set -- list of player's cards and table's cards

    Returns a tuple describing the combination
    """
    for i in range(4):
        if (card_set[i][0] == card_set[i+1][0] and
            card_set[i][0] == card_set[i+2][0] and
            card_set[i][0] == card_set[i+3][0]):
            if i != 3:
                return 8, hierarchy[card_set[3][0]], hierarchy[card_set[-1][0]]
            else:
                return 8, hierarchy[card_set[3][0]], hierarchy[card_set[2][0]]


def check_full_house(same_cards):
    """Checks whether a set of cards has a full house combination.

    Keyword arguments:
    card_set -- list of player's cards and table's cards

    Returns a tuple describing the combination
    """
    pare = []
    trips = []
    for i in same_cards.values():
        if len(i) == 3:
            trips = i
    for i in same_cards.values():
        if len(i) > 1 and i != trips:
            pare = i[:2]
    if pare and trips:
        return 7, hierarchy[trips[2][0]], hierarchy[pare[0][0]]


def check_flush(card_set, hand):
    """Checks whether a set of cards has a flush combination.

    Keyword arguments:
    card_set -- list of player's cards and table's cards

    Returns a tuple describing the combination
    """
    kicker = '1'
    card_set = card_set[-5:]
    for card in hand:
        if card in card_set:
            kicker = card
    return 6, hierarchy[kicker[0]]


def check_straight(same_cards):
    """Checks whether a set of cards has a straight combination.

    Keyword arguments:
    card_set -- list of player's cards and table's cards

    Returns a tuple describing the combination
    """
    cards_set = []
    for i in same_cards.values():
        if i:
            cards_set.append(i[0])
    count = len(cards_set)
    for i in range(count-4):
        if (hierarchy[cards_set[count-i-1][0]] == hierarchy[cards_set[count-i-2][0]]+1 and
            hierarchy[cards_set[count-i-1][0]] == hierarchy[cards_set[count-i-3][0]]+2 and
            hierarchy[cards_set[count-i-1][0]] == hierarchy[cards_set[count-i-4][0]]+3 and
            hierarchy[cards_set[count-i-1][0]] == hierarchy[cards_set[count-i-5][0]]+4):
            return 5, hierarchy[cards_set[count-i-1][0]]
    if (cards_set[0][0] == '2' and
        cards_set[1][0] == '3' and
        cards_set[2][0] == '4' and
        cards_set[3][0] == '5' and
        cards_set[count-1][0] == 'A'):
        return 5, hierarchy[cards_set[3][0]]


def check_set(same_cards):
    """Checks whether a set of cards has a set combination.

    Keyword arguments:
    card_set -- list of player's cards and table's cards

    Returns a tuple describing the combination
    """
    trips = []
    kickers = []
    for i in same_cards.values():
        if len(i) == 3:
            trips = i
        elif i:
            kickers.append(i[0])
    if trips:
        return 4, hierarchy[trips[0][0]], hierarchy[kickers[-1][0]], hierarchy[kickers[-2][0]]


def check_dopers(same_cards):
    """Checks whether a set of cards has a two pairs combination.

    Keyword arguments:
    card_set -- list of player's cards and table's cards

    Returns a tuple describing the combination
    """
    first_pair = []
    second_pair = []
    kicker = []
    for i in same_cards.values():
        if len(i) == 2:
            first_pair = i
    for i in same_cards.values():
        if len(i) == 2 and i != first_pair:
            second_pair = i
    for i in same_cards.values():
        if len(i) and i != first_pair and i != second_pair:
            kicker = [i[0]]
    if first_pair and second_pair:
        return 3, hierarchy[first_pair[0][0]], hierarchy[second_pair[0][0]], hierarchy[kicker[0][0]]


def check_pair(same_cards):
    """Checks whether a set of cards has a one pair combination.

    Keyword arguments:
    card_set -- list of player's cards and table's cards

    Returns a tuple describing the combination
    """
    pair = []
    kickers = []
    for i in same_cards.values():
        if len(i) == 2:
            pair = i
        elif i:
            kickers.append(i[0])
    if pair:
        return 2, hierarchy[pair[0][0]], hierarchy[kickers[-1][0]], hierarchy[kickers[-2][0]], hierarchy[kickers[-3][0]]


def check_high_card(card_set, hand):
    """Checks whether a set of cards has a high card combination.

    Keyword arguments:
    card_set -- list of player's cards and table's cards

    Returns a tuple describing the combination
    """
    card_set = card_set[-5:]
    kickers = []
    for card in hand:
        if card in card_set:
            kickers.append(card)
    if len(kickers) == 0:
        kickers = ['1', '1']
    if len(kickers) == 1:
        kickers.append('1')
        kickers = kickers[::-1]
    return 1, hierarchy[kickers[-1][0]], hierarchy[kickers[-2][0]]
