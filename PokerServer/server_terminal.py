import socket
import threading
import json
import time
import queue


class ServerTerminal:
    def __init__(self, sender, ip, port):
	"""Inits server

	Keyword arguments:
	sender -- an object which sends requests
	ip -- server ip
	port -- server port
	"""

        self.sender = sender
        self.ip = ip
        self.port = port
        self.mail = queue.Queue()

        self.interrupted = True
        self.connected = False

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()

    def run(self):
	"""Executes all server threads
	
	No keyword arguments
	"""

        self.interrupted = False
        print(f'Server successfully started!')
        t_listen_client_signals = threading.Thread(target=self.listen_client_signals)
        t_listen_mail_signals = threading.Thread(target=self.listen_mail_signals)
        t_listen_client_signals.start()
        t_listen_mail_signals.start()
        t_listen_mail_signals.join()
        t_listen_client_signals.join()

    def stop(self):
	"""Stops all server threads in a safe way
	
	No keyword arguments
	"""

        self.interrupted = True
        if self.connected:
            self.client_socket.send(b'DISCONNECT')
            time.sleep(2)
            print(f'Client {self.addr} successfully disconnected!')
        else:
            temp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_client.connect((self.ip, self.port))
            time.sleep(2)
            temp_client.close()
        print(f'Server successfully stopped!')

    def listen_client_signals(self):
	"""Listens to all messages from connected clients

	No keyword arguments
	"""

        while not self.interrupted:
            self.client_socket, self.addr = self.server_socket.accept()
            print(f'Client {self.addr} connected to port {self.port}')
            self.connected = True
            self.sender.mail.put(('NEW_CONNECTION',))
            while not self.interrupted:
                msg = self.client_socket.recv(4096)
                if not msg or msg == b'DISCONNECT':
                    self.client_socket.send(b'DISCONNECT')
                    break
                else:
                    try:
                        t = tuple(json.loads(msg.decode('utf-8')))
                        self.sender.mail.put(('NEW_ACTION', t))
                    except Exception:
                        pass
            self.connected = False
            self.sender.mail.put(('CONNECTION_LOST',))

    def listen_mail_signals(self):
	"""Listens to all messages from inner mail system
	
	No keyword arguments
	"""
        while not self.interrupted:
            if not self.connected:
                pass
                #continue
            #print('Waiting mail!')
            while not self.mail.empty() and not self.interrupted:
                print('Exploring queue!')
                command = self.mail.get()
                if command[0] == 'DESTROY':
                    self.stop()
                    break
                elif command[0] == 'SEND':
                    self.client_socket.send(json.dumps(command[1].encoded()).encode('utf-8'))
                time.sleep(0.05)
