import json, traceback
from decorator import decorator

from . import getLogger

def try_catch(message):
    """
    Wrapper to catch errors in ZMQ processes
    """
    @decorator
    def wrapper(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            getLogger("Error").error(
                "Wrapped Func: {func} exited with error: {error}".format(
                    func=func.__name__,
                    error=traceback.format_exc()
                )
            )
            return json.dumps({"error": message})
    return wrapper
