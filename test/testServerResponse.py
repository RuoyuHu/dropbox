import unittest
import os
from shutil import rmtree

from src.server import Server
from utils.networking import RequestType


class TestServerResponse(unittest.TestCase):
    def setUp(self):
        self.server = Server()
        self.test_dir = os.path.relpath("testServerDir", start=os.curdir)
        self.server.data_dir = self.test_dir
        if not os.path.exists(self.test_dir):
            os.mkdir(self.test_dir)
        with open(os.path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write("Hello world!")
        f.close()

    def testGetFileCreateDir(self):
        success, f = self.server.get_file("emptyDir/test.txt", RequestType.CREATE)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "emptyDir")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "emptyDir/test.txt")))
        f.close()

    def testGetFileFindsFile(self):
        success, f = self.server.get_file('test.txt', RequestType.UPDATE)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'test.txt')))
        f.close()

    def testGetFileCannotFindFile(self):
        success, f = self.server.get_file('random.txt', RequestType.UPDATE)
        self.assertFalse(success)
        with open(os.path.join(self.test_dir, 'random.txt'), 'w') as f:
            f.write("Hello world!")
        success, f = self.server.get_file('random.txt', RequestType.UPDATE)
        self.assertTrue(success)
        f.close()

    def testDeleteFile(self):
        file_path = os.path.join(self.test_dir, 'test.txt')
        self.assertTrue(os.path.exists(file_path))
        self.server.delete_recursive('test.txt')
        self.assertFalse(os.path.exists(file_path))

    def testDeleteFileRecursive(self):
        filename = 'test/test.txt'
        path = os.path.join(self.test_dir, filename)
        os.mkdir(os.path.join(self.test_dir, 'test'))
        with open(path, 'w') as f:
            f.write("Hello world!")
            f.close()
        self.assertTrue(os.path.exists(path))
        self.server.delete_recursive(filename)
        self.assertFalse(os.path.exists(path))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "test")))

    def testPrefix(self):
        self.assertEqual(self.server.get_prefix("server/test.txt"), "server")
        self.assertEqual(self.server.get_prefix("test.txt"), "")
        self.assertEqual(self.server.get_prefix("server/test/test.txt"), "server/test")

    def tearDown(self):
        self.server.listener.close()
        rmtree(self.test_dir)
