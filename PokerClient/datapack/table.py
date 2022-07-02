class Table:
    """Used to store information about tables"""
    def __init__(self, id, blind_size=1, count_players=1):
        """Defines class fields.

        Keyword arguments:
        id -- table id
        blind_size -- blind size on table
        count_players -- number of players sitting at the table

        """
        self.count_players = count_players
        self.blind_size = blind_size
        self.id = id

    @staticmethod
    def decoded(enc_dict):
        """Decode JSON-formatted dictionary of an object and return corresponding Table object."""
        id = enc_dict['id']
        blind_size = enc_dict['blind_size']
        count_players = enc_dict['count_players']
        return Table(id, blind_size, count_players)
