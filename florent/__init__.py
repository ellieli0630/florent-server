import os.path

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def project_dir(*args):
    """
    Return a path relative to project root directory
    Makes the path if it does not yet exist.
    """
    target = os.path.join(PROJECT_DIR, *args)
    if not os.path.exists(target):
        os.makedirs(target)
    return target
