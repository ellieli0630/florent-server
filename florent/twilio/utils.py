import re

from ..utils.errors import FlorentSMSError
from ..utils.strings import FEEDBACK_ERROR_MESSAGES

PATTERN = re.compile("^@(\w*)[:,]?\s?(@(\w+))?(.*)")

def route_message(body):
    """
    Parse text message to decide which database / table to save the feedback

    """
    results = PATTERN.match(body)

    if not results:
        raise FlorentSMSError(FEEDBACK_ERROR_MESSAGES[0])

    company, _, topic, feedback = results.groups()
    if not company:
        raise FlorentSMSError(FEEDBACK_ERROR_MESSAGES[0])
    if not topic:
        topic = "default"
    if not feedback:
        raise FlorentSMSError(FEEDBACK_ERROR_MESSAGES[2])

    return company, topic, feedback
