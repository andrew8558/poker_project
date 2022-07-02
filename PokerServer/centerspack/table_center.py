import queue
import time
import random
import copy
import threading
from centerspack import game_center


class TableCenter:
    """Used to work with tables"""
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

        def encoded(self):
            """Encodes a class object to send

            Returns dictionary where the key is the name of the field, the value is the content of the field"""
            enc_dict = {
                'count_players': self.count_players,
                'blind_size': self.blind_size,
                'id': self.id
            }
            return enc_dict

    def __init__(self):
        """Defines class fields"""
        self.mail = queue.Queue()
        self.condition_terminate = False
        self.tables = {}

    def process(self, message):
        """Parses the request and calls the appropriate method

        Keywords arguments:
        message -- tuple where the first argument is a request and the rest is data

        """
        func, *args = message
        if func == 'TABLE_CENTER_CREATE':
            self.create_table(args[0], args[1])
        elif func == 'TABLE_CENTER_CONNECT':
            self.connect(args[0], args[1])
        elif func == 'TABLE_CENTER_REFRESH':
            self.find_table(args[0])
        elif func == 'TABLE_CENTER_DISCONNECT':
            self.disconnect(args[0], args[1])
        elif func == 'DESTROY':
            self.terminate()

    def create_table(self, sender, blind_size):
        """Creates table, object of game_center class and thread to this object

        Keyword arguments:
        sender -- the object of the manager who sent the request
        blind_size -- blind size on table

        """
        flag = True
        while flag:
            x = random.randint(1000, 9999)
            if x not in self.tables.keys():
                flag = False
        table = TableCenter.Table(x, blind_size)
        g_c = game_center.GameCenter(x, blind_size)
        g_c_thread = threading.Thread(target=g_c.run)
        self.tables[x] = (table, g_c, g_c_thread)
        g_c_thread.start()
        sender.mail.put(('TABLE_CENTER_CREATE_SUCCESS', g_c, x))

    def connect(self, sender, table_id):
        """Adds a player to the table.

        Keyword arguments:
        sender -- the object of the manager who sent the request
        table_id -- table id

        """
        if table_id in self.tables.keys() and self.tables[table_id][0].count_players < 2:
            self.tables[table_id][0].count_players += 1
            sender.mail.put(('TABLE_CENTER_CONNECT_SUCCESS', self.tables[table_id][1], table_id))
        else:
            sender.mail.put(('TABLE_CENTER_CONNECT_FAILED', ))

    def disconnect(self, sender, table_id):
        """Performs the player's exit from the table and sends a destroy message to game center if count players is zero

        Keyword arguments:
        sender -- the object of the manager who sent the request
        table_id -- table id

        """
        self.tables[table_id][0].count_players -= 1
        if self.tables[table_id][0].count_players == 0:
            center = self.tables[table_id][1]
            center.mail.put(('DESTROY', ))
            self.tables[table_id][2].join()
            self.tables.pop(table_id)
        sender.mail.put(('TABLE_CENTER_DISCONNECT_SUCCESS', ))

    def find_table(self, sender):
        """Sends a list of objects of the table class to sender

        Keyword arguments:
        sender -- the object of the manager who sent the request

        """
        sender.mail.put(('TABLE_CENTER_REFRESH_SUCCESS', copy.deepcopy(list(map(lambda i: i[0], self.tables.values())))))

    def terminate(self):
        """Changes condition_terminate field that causes the loop to stop in the run method and sends a destroy message to all game centers"""
        for table, g_c, g_c_thread in self.tables.values():
            g_c.mail.put(('DESTROY', ))
            g_c_thread.join()
        self.tables.clear()
        self.condition_terminate = True

    def run(self):
        """Initializes the lifecycle of the table_center class object"""
        while not self.condition_terminate:
            while not self.mail.empty() and not self.condition_terminate:
                message = self.mail.get()
                self.process(message)
                time.sleep(0.01)
