import json

from .utils import route_message
from ..database.feedback import Feedback
from ..database import get_session
from ..utils.errors import FlorentError
from ..utils import getLogger
from .api import send_message
from .strings import FEEDBACK_THANKS_MESSAGES

FEEDBACK_LOGGER = getLogger("FeedbackService")
def service(message):
    body = message["Body"]
    company, topic, feedback = route_message(body)
    feedback = Feedback(
        body=feedback,
        company=company,
        topic=topic,
        country=message["FromCountry"],
        state=message["FromState"],
        zip_code=message["FromZip"],
        sender=message["From"],
        receiver=message["To"],
        serialized=json.dumps(message)
    )

    FEEDBACK_LOGGER.info("Received: From {number} for {company} about {topic} saying {feedback}".format(
        number=feedback.sender,
        company=feedback.company,
        topic=feedback.topic,
        feedback=feedback.body
    ))

    save_feedback(feedback)

    return feedback

def save_feedback(feedback):
    if not feedback.company:
        FEEDBACK_LOGGER.warning("Could not detect company to save feedback for {message}".format(
            message=feedback.serialized
        ))
        return
    session = get_session(feedback.company)
    try:
        session.add(feedback)
        session.commit()
    finally:
        session.close()

    send_message(
        FEEDBACK_THANKS_MESSAGES.get(feedback.company, FEEDBACK_THANKS_MESSAGES["_default"]),
        feedback.receiver,
        feedback.sender
    )
