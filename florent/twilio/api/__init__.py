import os

from twilio.rest import TwilioRestClient

from ...utils import getLogger

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token  = os.getenv("TWILIO_ACCOUNT_TOKEN")
client = TwilioRestClient(account_sid, auth_token)

logger = getLogger("MessageSender")

def send_message(message, from_, to):
    message = client.messages.create(
        body=message,
        to=to,
        from_=from_
    )
    logger.info("From: {from_}, To: {to}, Sent: {message}".format(
        from_=from_,
        to=to,
        message=message
    ))
