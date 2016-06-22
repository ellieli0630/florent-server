import json

from .utils import route_message
from ..database.feedback import Feedback
from ..database import get_session
from ..utils import getLogger

FEEDBACK_LOGGER = getLogger("FeedbackService")
def service(message):
    body = message["Body"]

    company, topic, feedback = route_message(body)

    feedback = Feedback(
        body=feedback,
        country=message["FromCountry"],
        state=message["FromState"],
        zip_code=message["FromZip"],
        sender=message["From"],
        topic=topic,
        serialized=json.dumps(message)
    )

    FEEDBACK_LOGGER.info("Received: From {number} for {company} about {topic} saying {feedback}".format(
        number=message["From"],
        company=company,
        topic=topic,
        feedback=feedback
    ))

    session = get_session(company)
    session.add(feedback)
    session.commit()
    session.close()

    return {
        "success": True
    }
