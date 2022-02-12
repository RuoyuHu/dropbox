import os
import unittest
import time
import multiprocessing.connection as connection
from shutil import rmtree
from threading import Thread
from unittest.mock import Mock

from src.client import Client
from utils.networking import RequestType
from utils.settings import Settings


"""
    Dummy server to test client connectivity with server
"""
class DummyServer(Thread):
    def __init__(self):
        super(DummyServer, self).__init__()
        self.listener = connection.Listener(Settings.server_address,
                                            authkey=Settings.authkey)
        self.running = True
        self.result = Mock()

    def run(self):
        while self.running:
            client_conn = self.listener.accept()
            try:
                request_type, filename = client_conn.recv()
                self.result.received(request_type, filename)
                self.running = False
            except Exception:
                self.result.fail()
            finally:
                client_conn.close()


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.server = DummyServer()

        self.test_dir = os.path.relpath("testClientDir", start=os.curdir)
        if not os.path.exists(self.test_dir):
            os.mkdir(self.test_dir)
        with open(os.path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write("Hello world!")
            f.close()
        Settings.client_dir = self.test_dir

    def testClientConnectOnCreate(self):
        self.server.start()
        time.sleep(1)
        self.client.update_server("test.txt", RequestType.CREATE)
        time.sleep(1)
        self.server.result.received.assert_called_with(RequestType.CREATE, "test.txt")
        self.server.result.fail.assert_not_called()

    def testClientConnectOnUpdate(self):
        self.server.start()
        time.sleep(1)
        self.client.update_server("test.txt", RequestType.UPDATE)
        time.sleep(1)
        self.server.result.received.assert_called_with(RequestType.UPDATE, "test.txt")
        self.server.result.fail.assert_not_called()

    def testClientConnectOnDelete(self):
        self.server.start()
        time.sleep(1)
        self.client.update_server("test.txt", RequestType.DELETE)
        time.sleep(1)
        self.server.result.received.assert_called_with(RequestType.DELETE, "test.txt")
        self.server.result.fail.assert_not_called()

    def tearDown(self):
        self.server.listener.close()
        self.server.join()
        rmtree(self.test_dir)