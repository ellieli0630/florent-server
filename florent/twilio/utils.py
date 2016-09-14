import re

from ..utils.errors import FlorentSMSError
from ..utils.strings import FEEDBACK_ERROR_MESSAGES

PATTERN = re.compile("@(.*):\s?@(\w*)\s(.*)")

def route_message(body):
    """
    Parse text message to decide which database / table to save the feedback

    """
    results = PATTERN.match(body)
    info = ["company", "topic", "feedback"]
    for idx in xrange(len(info)):
        try:
            info[idx] = results.group(idx)
        except IndexError:
            message = FEEDBACK_ERROR_MESSAGES[idx]
            if idx > 0:
                message = message.format(info[idx - 1])
            raise FlorentSMSError(message)

    return tuple(info)
