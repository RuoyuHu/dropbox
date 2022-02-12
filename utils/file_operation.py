import os


"""
    Recursively build a list of names of files from a root directory, empty
    directories are ignored
    :returns [str]  - List of filenames
"""
def build_directory_tree(root, prefix=""):
    filenames = []
    directory = os.path.join(root, prefix)
    for node in os.listdir(directory):
        node_path = os.path.join(prefix, node)
        if os.path.isfile(os.path.join(directory, node)):
            filenames.append(node_path)
        else:
            filenames += build_directory_tree(root, node_path)
    return filenames


"""
    Build directory if it does not exist
    :arg str dir    - Directory to build
"""
def build_if_not_exists(dir):
    dir_path = os.path.relpath(dir, start=os.curdir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
