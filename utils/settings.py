from argparse import Namespace


# System wide parameters
params = {
    'client_dir': 'dirs/client',  # Default Client Data Directory
    'server_dir': 'dirs/server',  # Default Server Data Directory
    'server_address': ("localhost", 50000),  # Default server address
    'authkey': b'password',  # Authkey for connecting to server
    'scanner_interval': 5,  # Scanner will scan for file changes every d seconds
}

Settings = Namespace(**params)
