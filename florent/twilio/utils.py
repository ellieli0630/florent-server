import re

from ..utils.errors import FlorentSMSError
from .strings import FEEDBACK_ERROR_STRINGS

PATTERN = re.compile("^(@(\w*))?[:,]?\s?(@(\w+))?(.*)")

def route_message(body):
    """
    Parse text message to decide which database / table to save the feedback
    """
    results = PATTERN.match(body)

    if not results:
        raise FlorentSMSError(FEEDBACK_ERROR_STRINGS[0])

    _, company, _, topic, feedback = results.groups()
    return company, topic, feedback
