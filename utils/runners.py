from threading import Thread

from src.scanner import FileEventHandler, FileScanner
from src.server import Server


"""
    Thread to start file scanner
"""
class ScannerRunner(Thread):
    def __init__(self):
        super(ScannerRunner, self).__init__()
        self.handler = FileEventHandler()
        self.scanner = FileScanner(self.handler)

    def run(self):
        self.scanner.run()


"""
    Thread to run file server
"""
class ServerRunner(Thread):
    def __init__(self):
        super(ServerRunner, self).__init__()
        self.server = Server()

    def run(self):
        self.server.up()
