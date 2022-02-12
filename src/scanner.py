import os
import time
from datetime import datetime
from argparse import Namespace

from src.client import Client
from src.event_handler import BaseEventHandler
from utils.networking import RequestType
from utils.settings import Settings
from utils.file_operation import build_directory_tree


"""
    Event handler, called by scanner when it detects change to directory. Uses
    socket client to communicate with server
"""
class FileEventHandler(BaseEventHandler):
    def __init__(self):
        self.client = Client()

    """
        Handles creation event, sends creation request to server
        :arg str filename - Name of file created
    """
    def handle_create(self, filename):
        print(f"New file {filename} added")
        self.client.update_server(filename, RequestType.CREATE)

    """
        Handles update event, sends update request to server
        :arg str filename - Name of file updated
    """
    def handle_update(self, filename):
        print(f"File {filename} has been changed")
        self.client.update_server(filename, RequestType.UPDATE)

    """
        Handles deletion event, sends delete request to server
        :arg str filename - Name of file deleted
    """
    def handle_delete(self, filename):
        print(f"File {filename} has been deleted")
        self.client.update_server(filename, RequestType.DELETE)


"""
    File scanner, scans through a target directory at set intervals. Calls event
    handler if it detects change in the directory
    :arg BaseEventHandler handler   - Event handler, communicates with server
"""
class FileScanner:
    def __init__(self, handler):
        self.handler = handler
        self.dir = os.path.relpath(Settings.client_dir, start=os.curdir)
        self.last_scan_time = datetime.now()
        self.file_ledger = None  # Set in the build_file_ledger function

        self.build_file_ledger()
        self.running = True

    """
        Start the file scanner. Will run at fixed intervals until interrupted
    """
    def run(self):
        try:
            while self.running:
                print(f"Scanning files at {datetime.now()}")
                for entry in self.file_ledger:
                    if os.path.exists(entry.path):
                        mtime = os.path.getmtime(entry.path)
                        if int(time.time() - mtime) < Settings.scanner_interval:
                            # File has been updated recently
                            self.handler.handle_update(entry.filename)
                    else:
                        # File has been deleted
                        self.handler.handle_delete(entry.filename)

                # Check for new files
                old_ledger = self.file_ledger
                self.build_file_ledger()
                new_files = [entry for entry in self.file_ledger if entry not in old_ledger]
                for entry in new_files:
                    # File has been added
                    self.handler.handle_create(entry.filename)

                # Update log and wait
                self.last_scan_time = datetime.now()
                print(f"Scan completed at {self.last_scan_time}, sleeping for {Settings.scanner_interval} seconds")
                time.sleep(Settings.scanner_interval)
        finally:
            print("Scanner closing")

    """
        Builds ledger of files to keep track of in directory
    """
    def build_file_ledger(self):
        ledger = []
        filenames = build_directory_tree(self.dir)
        for filename in filenames:
            path = os.path.join(self.dir, filename)
            ledger.append(Namespace(**{
                'filename': filename,
                'path': path,
            }))
        self.file_ledger = ledger
