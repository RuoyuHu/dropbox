import os
import unittest
import time
from shutil import rmtree, copyfile

from utils.runners import ScannerRunner, ServerRunner
from utils.settings import Settings


class TestClientServer(unittest.TestCase):
    def setUp(self):
        self.client_dir = os.path.relpath("testClientDir", start=os.curdir)
        if not os.path.exists(self.client_dir):
            os.mkdir(self.client_dir)
        self.server_dir = os.path.relpath("testServerDir", start=os.curdir)
        if not os.path.exists(self.server_dir):
            os.mkdir(self.server_dir)

        Settings.client_dir = self.client_dir
        Settings.server_dir = self.server_dir
        self.scanner = ScannerRunner()
        self.server = ServerRunner()

    def testClientServerAddFile(self):
        self.scanner.start()
        self.server.start()

        source_file = os.path.join(self.client_dir, 'test.txt')
        with open(source_file, 'w') as f:
            f.write("Hello world!")
            f.close()

        time.sleep(2 * Settings.scanner_interval)
        server_file = os.path.join(self.server_dir, 'test.txt')
        self.assertTrue(os.path.exists(server_file))
        with open(server_file, 'r') as sf:
            self.assertTrue("Hello world!" in sf.readlines())
            sf.close()

    def testClientServerUpdateFile(self):
        source_file = os.path.join(self.client_dir, 'test.txt')
        server_file = os.path.join(self.server_dir, 'test.txt')
        with open(source_file, 'w') as f:
            f.write("Hello world!")
            f.close()
        copyfile(source_file, server_file)

        time.sleep(Settings.scanner_interval)
        self.server.start()
        self.scanner.start()

        with open(source_file, 'a') as f:
            f.write("\nfoo")
            f.close()

        time.sleep(Settings.scanner_interval)
        self.assertTrue(os.path.exists(server_file))
        with open(server_file, 'r') as sf:
            self.assertTrue("foo" in sf.readlines())
            sf.close()

    def testClientServerDeleteFile(self):
        source_file = os.path.join(self.client_dir, 'test.txt')
        server_file = os.path.join(self.server_dir, 'test.txt')
        with open(source_file, 'w') as f:
            f.write("Hello world!")
            f.close()
        copyfile(source_file, server_file)

        time.sleep(Settings.scanner_interval)
        self.server.start()
        self.scanner.start()
        time.sleep(1)
        os.remove(source_file)
        self.assertFalse(os.path.exists(source_file))
        time.sleep(Settings.scanner_interval)
        self.assertFalse(os.path.exists(server_file))

    def tearDown(self):
        try:
            self.scanner.scanner.running = False
            self.server.server.running = False
            self.server.server.listener.close()
            self.server.join()
            self.scanner.join()
        except ConnectionAbortedError:
            pass
        rmtree(self.client_dir)
        rmtree(self.server_dir)
