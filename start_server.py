import os
from argparse import ArgumentParser
from src.server import Server
from utils.file_operation import build_if_not_exists
from utils.settings import Settings


"""
    Script for starting the file server
"""
def main(args):
    if args.dir is not None:
        Settings.server_dir = os.path.normpath(args.dir)
        build_if_not_exists(Settings.server_dir)
    server = Server()
    try:
        print(f"Server established at {Settings.server_address}")
        print("Server going up...")
        server.up()
    finally:
        server.listener.close()
        print(f"Closed socket at {Settings.server_address}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dir", type=str,
                        help="Directory for server to duplicate files in")
    args = parser.parse_args()
    main(args)
