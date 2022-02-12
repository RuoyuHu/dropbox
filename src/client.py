import os
import multiprocessing.connection as connection
from utils.settings import Settings


"""
    Client object, used by the scanner event handler to send information (files)
    to the server
"""
class Client:
    def __init__(self):
        self.connected = False  # Flag indicating client status

    """
        Sends request to server
        :arg str filename               - Name of the file involved
        :arg RequestType request_type   - Type of request to send
    """
    def update_server(self, filename, request_type):
        f = None
        if request_type.send_data():
            client_dir = os.path.relpath(Settings.client_dir, start=os.curdir)
            path = os.path.join(client_dir, filename)
            f = open(path, 'rb')  # Load data before contacting server
        try:
            print(f"Connecting to {Settings.server_address}...")
            server_conn = connection.Client(Settings.server_address,
                                            authkey=Settings.authkey)
            print(f"Connected to {Settings.server_address}")
            self.connected = True
            server_conn.send((request_type, filename))
            if request_type.send_data():
                server_conn.send(f.read())
                f.close()
            print("Send successful")
            server_conn.close()
        except TimeoutError:
            print(f"Failed to connect to {Settings.server_address} - Connection Timed Out")
        except ConnectionRefusedError:
            print(f"Failed to connect to {Settings.server_address} - Connection Refused")
        finally:
            self.connected = False
