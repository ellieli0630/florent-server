import json

from ..database.feedback import Feedback
from ..database import get_session

"""
{
  u'AccountSid': u'AC0a215171b6c7ed286ebae5dd74455543',
  u'ApiVersion': u'2010-04-01',
  u'Body': u'Hello',
  u'From': u'+19097208906',
  u'FromCity': u'POMONA',
  u'FromCountry': u'US',
  u'FromState': u'CA',
  u'FromZip': u'91767',
  u'MessageSid': u'SM1e98f0501bfaeb833eaaca74e057b922',
  u'NumMedia': u'0',
  u'NumSegments': u'1',
  u'SmsMessageSid': u'SM1e98f0501bfaeb833eaaca74e057b922',
  u'SmsSid': u'SM1e98f0501bfaeb833eaaca74e057b922',
  u'SmsStatus': u'received',
  u'To': u'+16265873439',
  u'ToCity': u'WEST COVINA',
  u'ToCountry': u'US',
  u'ToState': u'CA',
  u'ToZip': u'91722'
}
"""

def service(message):
    message = json.loads(message)

    feedback = Feedback(
        body=message["Body"],
        country=message["FromCountry"],
        state=message["FromState"],
        zip_code=message["FromZip"],
        sender=message["From"]
    )

    session = get_session()
    session.add(feedback)
    session.commit()
    session.close()

    return {
        "success": True
    }
