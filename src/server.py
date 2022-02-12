import os
import multiprocessing.connection as connection

from utils.networking import RequestType
from utils.settings import Settings

"""
    Server object, manages a directory. Receives requests for file creation,
    update and deletion from client(s). Updates its own directory to match
    given requests
"""
class Server:
    def __init__(self):
        self.listener = connection.Listener(Settings.server_address,
                                            authkey=Settings.authkey)
        self.data_dir = os.path.relpath(Settings.server_dir, start=os.curdir)
        self.running = True

    def up(self):
        print("Server up")

        while self.running:
            try:
                client_conn = self.listener.accept()
            except ConnectionAbortedError:
                self.running = False
                break  # Time to end the server
            print(f"Accepted connection from client at: {client_conn}")
            try:
                request_type, filename = client_conn.recv()
                # Check requested file exists/has valid operation
                success, f = self.get_file(filename, request_type)
                if not success:
                    print(f"File {filename} does not exist")
                    continue
                if request_type.send_data():
                    try:
                        rec_data = client_conn.recv()
                        while rec_data:
                            f.write(rec_data)
                            rec_data = client_conn.recv()
                    except EOFError:  # File has completely been read
                        f.close()
                        pass
                elif request_type == RequestType.DELETE:
                    print(f"Deleting {filename}")
                    f.close()
                    self.delete_recursive(filename)
            finally:
                print(f"Transmission over")
                client_conn.close()
        print("Server closing")
        self.listener.close()

    """
        Determines if the given filetype and request type are feasible together
        :args str filename              - Name of the file
        :arg RequestType request_type   - Type of request to service
        
        :returns (bool, File)           - Whether the operation is feasible and
                                          the file pointer if it is
    """
    def get_file(self, filename, request_type):
        prefix = self.get_prefix(filename)

        file_path = os.path.join(self.data_dir, filename)
        if not os.path.exists(file_path):
            if request_type == RequestType.CREATE:
                os.makedirs(os.path.join(self.data_dir, prefix), exist_ok=True)
            else:
                return False, None
        return True, open(file_path, 'wb')

    """
        Delete a file and recursively delete all empty directories above this
        except root
        :arg str filename       - Name of file to delete
    """
    def delete_recursive(self, filename):
        prefix = self.get_prefix(filename)
        os.remove(os.path.join(self.data_dir, filename))
        if prefix != "":
            os.removedirs(os.path.join(self.data_dir, prefix))

    """
        For a given path find its prefix i.e. 'src/main.py' will return 'src'
        :arg str filename       - Name of the file
        
        :returns str            - Path prefix
    """
    def get_prefix(self, filename):
        names = os.path.normpath(filename).rsplit(os.sep, 1)
        prefix = ""
        if len(names) > 1:
            prefix = names[-2]
        return prefix

