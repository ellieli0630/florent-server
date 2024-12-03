"""
Florent router
"""
import traceback

from tornado.web import RequestHandler
from tornado.gen import coroutine
from tornado.escape import json_encode

from manager import THREAD_POOL, execute
from ..utils import getLogger
from ..utils.errors import FlorentError, FlorentSMSError, DEFAULT_ERROR

LOGGER = getLogger("FlorentRouter")
class FlorentRouter(RequestHandler):
    """
    Receives and Handles all calls to the server
    """
    def send_response(self, response, code=200):
        """
        Helper that wraps the response in a statused & json response
        """
        self.set_status(code)
        self.write(json_encode(response))

    @coroutine
    def get(self, *args, **kwargs):
        """
        Handles GET requests
        """
        self.send_response("Hello! You've reached the Florent Server. :) Have a good day!")

    @coroutine
    def post(self, path, method=None):
        """
        Handles POST requests
        """
        try:
            LOGGER.debug("Received POST at [{path}][{method}]:\nbody:{body}".format(
                path=path,
                method=method,
                body=self.request.body
            ))
            # HANDLING LOGIC
            response = yield THREAD_POOL.submit(execute, path, method, self.request.body)
            self.send_response(response)
        except FlorentSMSError as e:
            self.send_response(e.to_json(), code=e.code)
            # TODO - send this message back to user via SMS
        except FlorentError as e:
            self.send_response(e.to_json(), code=e.code)
            LOGGER.warning(e)
        except Exception as e:
            self.send_response(DEFAULT_ERROR, code=503)
            LOGGER.error(
                "SERVER ERROR at [{path}][{method}]\nheaders: {header}\nbody: {body}\nerror: {error}".format(
                    path=path,
                    method=method,
                    body=self.request.body,
                    header=self.request.headers,
                    error=traceback.format_exc()
                )
            )
        finally:
            self.finish()
