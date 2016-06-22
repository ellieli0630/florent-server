import signal, os, psutil
from argparse import ArgumentParser

from tornado.web import Application
from tornado.ioloop import IOLoop, PeriodicCallback

from .server.api_router import FlorentRouter
from .server.web_router import WebRouter
from .server.manager import initialize
from .utils import getLogger

LOGGER = getLogger("Main")
ENDPOINTS = [
    (r"api/(?P<path>[a-zA-Z]+)/(?P<method>[a-zA-Z0-9]+)", FlorentRouter),
    (r"/", WebRouter)
]

def kill_processes():
    """
    Kill process children, then kill parent
    """
    parent = psutil.Process(os.getpid())
    for child in parent.children(recursive=True):
        try:
            child.terminate()
        except psutil.NoSuchProcess:
            continue
    parent.kill()

def start(port):
    application = Application(
        ENDPOINTS,
        static_path=os.path.join(os.path.dirname(__file__), "server", "static"),
        template_path=os.path.join(os.path.dirname(__file__), "server", "templates")
    )

    application.listen(port)
    LOGGER.info("Server listening on port {port}".format(port=port))

    # Start Services
    initialize()

    signal.signal(signal.SIGTERM, kill_processes)
    signal.signal(signal.SIGINT, kill_processes)

    IOLoop.current().start()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--production", help="uses port 80", action="store_true")
    parser.add_argument("--port", help="set the port used")

    args = parser.parse_args()
    port = 80 if args.production else (args.port or 3000)
    start(port)
