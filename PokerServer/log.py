import time
import queue
import threading


class Log:
    """Implementation of Log architectural unit. Used for logging important Server events."""

    def __init__(self):
        """Create Log object"""
        self.mail = queue.Queue()
        self.running = True

    def process(self, msg):
        """Process incoming message."""
        cmd, *args = msg
        if cmd == 'DESTROY':
            self.running = False
        elif cmd == 'LOG':
            print(args[0])

    def run(self):
        """Run Log lifecycle"""
        while self.running:
            while not self.mail.empty() and self.running:
                msg = self.mail.get()
                self.process(msg)
            time.sleep(0.05)