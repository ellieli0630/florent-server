import os, sys, logging

from .. import project_dir

LOGGING_PATH = os.path.join(project_dir("logs"), "florent.log")
LOG_FORMAT = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"

logging.basicConfig(stream=sys.stdout, format=LOG_FORMAT, level=logging.DEBUG)
fileHandler = logging.FileHandler(LOGGING_PATH)
fileHandler.setFormatter(logging.Formatter(LOG_FORMAT))
logging.getLogger('').addHandler(fileHandler)

def getLogger(name):
    return logging.getLogger(name)
