import unittest
import os
from shutil import rmtree, copyfile
from utils.file_operation import build_directory_tree


class TestFileOperation(unittest.TestCase):

    def setUp(self):
        # Create directory for testing
        self.test_path = os.path.relpath('testFileDir', start=os.curdir)
        if not os.path.exists(self.test_path):
            os.mkdir(self.test_path)

        # Create placeholder text file
        self.test_file = os.path.join(self.test_path, 'test.txt')
        test_file = open(self.test_file, 'w')
        test_file.write("Hello world!")
        test_file.close()

        # Put tree structure in place
        os.mkdir(os.path.join(self.test_path, 'dir1'))
        os.mkdir(os.path.join(self.test_path, 'dir1/dir2'))

        copyfile(self.test_file, os.path.join(self.test_path, 'dir1/test1.txt'))
        copyfile(self.test_file, os.path.join(self.test_path, 'dir1/dir2/test2.txt'))

    def test_root(self):
        # Root files should show up in directory tree without prefixes
        root_file = 'test.txt'
        dir_names = build_directory_tree(self.test_path)
        self.assertTrue(root_file in dir_names)

    def test_embed(self):
        # Embedded files should appear in directory tree with directory prefix
        #  but not root
        embedded_files = ['dir1/test1.txt', 'dir1/dir2/test2.txt']
        dir_names = build_directory_tree(self.test_path)
        for filename in embedded_files:
            self.assertTrue(filename in dir_names)

        # Embedded files should not appear without prefix
        self.assertFalse('test1.txt' in dir_names)

    def test_empty_dir(self):
        # Empty directories should not appear in the directory tree
        empty_path = os.path.join(self.test_path, 'empty')
        os.mkdir(empty_path)
        self.assertTrue(os.path.exists(empty_path))
        self.assertFalse('empty' in build_directory_tree(self.test_path))

    def tearDown(self):
        rmtree(self.test_path)
