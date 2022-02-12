import os
from argparse import ArgumentParser
from utils.runners import ScannerRunner, ServerRunner
from utils.settings import Settings
from utils.file_operation import build_if_not_exists


"""
    Run both client and server from the same file
"""
def main(args):
    # Update target dirs if necessary
    if args.cdir is not None:
        Settings.client_dir = os.path.normpath(args.cdir)
        build_if_not_exists(Settings.client_dir)
    if args.sdir is not None:
        Settings.server_dir = os.path.normpath(args.sdir)
        build_if_not_exists(Settings.server_dir)

    # Create threads
    scanner_runner = ScannerRunner()
    server_runner = ServerRunner()

    try:
        # Start threads
        server_runner.start()
        scanner_runner.start()
        while True:
            pass
    finally:
        # End runners, close connections
        scanner_runner.scanner.running = False
        server_runner.server.running = False
        server_runner.server.listener.close()
        scanner_runner.join()
        server_runner.join()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--cdir", type=str,
                        help="Client directory for scanner to watch")
    parser.add_argument("--sdir", type=str,
                        help="Server directory for server to maintain")

    args = parser.parse_args()
    main(args)