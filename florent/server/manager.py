import os, json
from multiprocessing import Process, Queue, Lock
from importlib import import_module
from collections import defaultdict

import zmq
from concurrent.futures import ThreadPoolExecutor

from .errors import FlorentError
from .. import project_dir
from ..config import MANAGER_CONFIG
from ..utils import getLogger
from ..utils.wrappers import try_catch
from ..utils.parsing_utils import smart_parse

LOGGER = getLogger("Management")
ZMQ_CONTEXT = zmq.Context()
THREAD_POOL = ThreadPoolExecutor(max_workers=4)

MANAGERS = defaultdict(dict)

IPIDS_DIR = project_dir(".ipids")

def execute(path, method, body):
    methods = MANAGERS.get(path, {})
    manager = methods.get(method)

    if not manager:
        raise FlorentError("{path}/{method} does not exist".format(
            path=path,
            method=method
        ))

    body = json.dumps(smart_parse(body))
    response = manager.router.route(body)

    if "error" in response:
        raise FlorentError(response.get("error"), code=400)

    return response

class Manager(object):
    """
    Uses Multiprocessing and ZMQ to distribute workload
    """

    def __init__(self, name, processes):
        self.name = name
        self.processes = processes
        self.router = None

        self.router_address = _get_address(self.name, "router")
        self.dealer_address = _get_address(self.name, "dealer")

        Process(target=self._start_poller).start()

    @try_catch("Server Failed to Start Router")
    def start_router(self):
        self.router = Router(self.name, self.router_address)

    @try_catch("Server Failed to Start Dealers")
    def start_dealers(self, func):
        for dealer_id in xrange(self.processes):
            Process(
                target=Dealer,
                args=(self.name, self.dealer_address, dealer_id, import_module(func))
            ).start()

    @try_catch("Server Failed to Start Poller")
    def _start_poller(self):
        LOGGER.info("Manager {name} starting".format(name=self.name))
        # Create Sockets
        router = ZMQ_CONTEXT.socket(zmq.ROUTER)
        router.bind(self.router_address)
        dealer = ZMQ_CONTEXT.socket(zmq.DEALER)
        dealer.bind(self.dealer_address)

        # Initilize the Polls
        poller = zmq.Poller()
        poller.register(router, zmq.POLLIN)
        poller.register(dealer, zmq.POLLIN)

        # Send / Receive between Router & Dealers
        while True:
            socks = dict(poller.poll())
            if socks.get(router) == zmq.POLLIN:
                dealer.send_multipart(router.recv_multipart())
            if socks.get(dealer) == zmq.POLLIN:
                router.send_multipart(dealer.recv_multipart())

class Dealer(object):
    def __init__(self, name, dealer_address, dealer_id, func):
        LOGGER.info("Router {name} starting".format(name=name))
        self.name = name
        self.dealer_id = dealer_id
        self.func = func.service

        self.socket = zmq.Context().socket(zmq.REP)
        self.socket.connect(dealer_address)

        self._handle_zmq()

    @try_catch("Dealer failed to handle message")
    def _handle_zmq(self):
        """
        Begin listening for messages to respond to
        """
        while True:
            message = self.socket.recv()
            LOGGER.debug("{name} Dealer {dealer_id} received: {message}".format(
                name = self.name,
                message = message,
                dealer_id = self.dealer_id
            ))
            message = self._reply(message)
            self.socket.send(message)

    def _reply(self, message):
        """
        Handle the message received
        """
        body = json.loads(message)
        result = self.func(body)
        return json.dumps(result, ensure_ascii=True)

class Router(object):
    def __init__(self, name, router_address):
        LOGGER.info("Router {name} starting".format(name=name))
        self.name = name
        self.router_address = router_address

    @try_catch("Router failed to route")
    def route(self, body):
        socket = _create_socket(self.router_address)
        try:
            socket.send(body)
        except zmq.ZMQError:
            raise FlorentError("{name} has not been activated yet".format(
                name=self.name
            ))

        LOGGER.debug("{name} Router sent {body}".format(
            name=self.name,
            body=body
        ))

        message = socket.recv()
        LOGGER.debug("{name} Router received: {body}".format(
            name=self.name,
            body=message
        ))

        return json.loads(message)

def initialize():
    """
    Initializes the Managers and determines when to load the modules
    """
    for path, methods in MANAGER_CONFIG.iteritems():
        for method, info in methods.iteritems():
            manager = Manager(info["name"], info["processes"])
            manager.start_router()
            manager.start_dealers(info["func"])
            MANAGERS[path][method] = manager

"""
ZMQ Communications
"""
def _get_address(name, address_type):
    return 'ipc://%s/%s-%s.ipc' % (IPIDS_DIR, name, address_type)

def _create_socket(address):
    """
    Create a new socket to pass messages to the broker
    Connects to the given address
    """
    socket = ZMQ_CONTEXT.socket(zmq.REQ)
    socket.connect(address)
    return socket
