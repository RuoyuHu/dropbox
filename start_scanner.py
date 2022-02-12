import os
from argparse import ArgumentParser
from src.scanner import FileScanner, FileEventHandler
from utils.file_operation import build_if_not_exists
from utils.settings import Settings


"""
    Script for starting the file scanner
"""
def main(args):
    if args.dir is not None:
        Settings.client_dir = os.path.normpath(args.dir)
        build_if_not_exists(Settings.client_dir)
    handler = FileEventHandler()
    scanner = FileScanner(handler)
    scanner.run()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dir", type=str,
                        help="Directory to scan, defaults to dirs/client")

    args = parser.parse_args()
    main(args)
