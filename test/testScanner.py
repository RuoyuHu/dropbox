import os
import time
import unittest
from unittest.mock import Mock
from threading import Thread
from shutil import rmtree

from src.scanner import FileScanner
from utils.settings import Settings


"""
    Testing thread to run scanner in separate thread to test
"""
class TestThread(Thread):
    def __init__(self, scanner):
        super(TestThread, self).__init__()
        self.scanner = scanner

    def run(self):
        self.scanner.run()


class TestScanner(unittest.TestCase):

    def setUp(self):
        # Set up testing directory
        self.test_dir = os.path.relpath("testFileDir", start=os.curdir)
        if not os.path.exists(self.test_dir):
            os.mkdir(self.test_dir)

        # Setup test file
        with open(os.path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write("Hello world!")
        f.close()

        # Setup event handler and file scanner
        Settings.client_dir = self.test_dir  # File scanner to watch testing directory
        dummy_handler = Mock()
        self.scanner = FileScanner(dummy_handler)
        self.thread = TestThread(self.scanner)

    def test_create(self):
        # Scanner should detect when a file is created
        self.thread.start()
        time.sleep(1)
        with open(os.path.join(self.test_dir, 'create.txt'), 'w') as f:
            f.write("Hello world!")
        time.sleep(Settings.scanner_interval + 1)
        self.scanner.handler.handle_create.assert_called()

    def test_update(self):
        # Scanner should detect when a file is updated
        self.thread.start()
        time.sleep(1)
        with open(os.path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write("New content")
        time.sleep(Settings.scanner_interval + 1)
        self.scanner.handler.handle_update.assert_called()

    def test_delete(self):
        # Scanner should detect when a file is deleted
        self.thread.start()
        time.sleep(1)
        file_path = os.path.join(self.test_dir, 'test.txt')
        os.remove(file_path)
        self.assertFalse(os.path.exists(file_path))
        time.sleep(Settings.scanner_interval + 1)
        self.scanner.handler.handle_delete.assert_called()

    def tearDown(self):
        self.scanner.running = False
        rmtree(self.test_dir)
        self.thread.join()