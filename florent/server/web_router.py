"""
Florent router
"""
import os

from tornado.web import RequestHandler
from tornado.gen import coroutine

from manager import THREAD_POOL, execute
from ..utils import getLogger
from ..utils.errors import FlorentError, DEFAULT_ERROR

from .web.qa import handle as qa_handler
from .web.not_found import handle as not_found_handler

ROUTE_TABLE = {
    "qa": qa_handler,
}

DIR = os.path.join(os.path.dirname(__file__), "templates")
LOGGER = getLogger("WebRouter")
class WebRouter(RequestHandler):
    @coroutine
    def get(self, *args, **kwargs):
        """
        Handles GET requests
        """
        path = self.request.uri.split("/")
        handler = ROUTE_TABLE.get(path[0], not_found_handler)
        result_page, kwargs = handler(path, self.request.query, self.request.body)
        self.render(result_page, **kwargs)
