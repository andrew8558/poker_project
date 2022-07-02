import socket
import threading
import time
import queue
import json
import datapack.auth_context, datapack.menu_context, datapack.game_context


class ClientTerminal:
    def __init__(self, sender, ip, start_port, end_port):
	"""Inits client terminal object

	Keyword arguments:
	sender -- an object which sends all requests
	ip -- client ip
	start_port -- the first port in a list of server ports
	end_port -- the last port in a list of server ports
	"""

        self.sender = sender
        self.ip = ip
        self.start_port = start_port
        self.end_port = end_port
        self.mail = queue.Queue()

        self.interrupted = True
        self.connected = False

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
	"""Executes all threads in client terminal

	No keyword arguments
	"""


        self.interrupted = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        t_connect_port = threading.Thread(target=self.connect_port)
        t_listen_port_signals = threading.Thread(target=self.listen_port_signals)
        t_connect_port.start()
        t_listen_port_signals.start()

    def stop(self):
	"""Stops all threads in client terminal

	No keyword arguments
	"""

        self.interrupted = True
        self.client_socket.send(b'DISCONNECT')
        time.sleep(2)
        self.client_socket.close()

    def connect_port(self):
	"""Searches for a free server port and connects it

	No keyword arguments
	"""

        while not self.interrupted:
            self.current_port = self.start_port
            while self.current_port <= self.end_port:
                try:
                    self.client_socket.connect((self.ip, self.current_port))
                except socket.error:
                    print(f'Address {self.ip}:{self.current_port} is unavailable right now!')
                    self.current_port += 1
                    continue
                break
            print(f'Successful connection to {self.ip}:{self.current_port}!')
            self.connected = True

            while not self.interrupted:
                # Вытаскивать команды из очереди и следовать им
                while not self.mail.empty():
                    command = self.mail.get()
                    if command[0] == 'DESTROY':
                        self.stop()
                        break
                    elif command[0] == 'SEND':
                        self.client_socket.send(json.dumps(list(command[1])).encode('utf-8'))
                    time.sleep(0.05)

            self.connected = False

    def listen_port_signals(self):
	"""Listens to all requests from connected port

	No keyword arguments
	"""

        while not self.interrupted:
            if not self.connected:
                continue
            signal = self.client_socket.recv(4096)
            if signal == b'DISCONNECT':
                self.sender.mail.put(('CONNECTION_LOST',))
                self.stop()
                break
            else:
                d = json.loads(signal.decode('utf-8'))
                if d['name'] == 'AUTH':
                    temp = datapack.auth_context.AuthContext.decoded(d)
                elif d['name'] == 'MENU':
                    temp = datapack.menu_context.MenuContext.decoded(d)
                elif d['name'] == 'GAME':
                    temp = datapack.game_context.GameContext.decoded(d)
                self.sender.mail.put(('NEW_CONTEXT', temp))
            time.sleep(0.05)
