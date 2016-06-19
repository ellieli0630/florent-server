import json

from .utils import route_message
from ..database.feedback import Feedback
from ..database import get_session

def service(message):
    serialized_message = message
    message = json.loads(message)
    body = message["Body"]

    company, topic, feedback = route_message(body)

    feedback = Feedback(
        body=feedback,
        country=message["FromCountry"],
        state=message["FromState"],
        zip_code=message["FromZip"],
        sender=message["From"],
        category=topic,
        serialized=serialized_message
    )

    session = get_session(company)
    session.add(feedback)
    session.commit()
    session.close()

    return {
        "success": True
    }
