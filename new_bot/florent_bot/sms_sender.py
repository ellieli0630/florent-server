import json
import codecs
from twilio.rest import TwilioRestClient
import traceback

def ld(p,encoding="utf-8"):
    with codecs.open(p,"rt",encoding=encoding) as f:
        return json.load(f)
data=ld("account_twilio.json")

ACCOUNT_SID=data['ACCOUNT_SID']
AUTH_TOKEN=data['AUTH_TOKEN']

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
def send_sms( sender,receiver, text):
    try:
        len_text=len(text)
        quantity=len_text//1600
        quantity=quantity+1
        for i in range (quantity):
            client.messages.create(
            to="+"+receiver,
            from_="16178700866",
            body=text[i*1600:i*1600+1600],
            )
            print "message sent on number "+(receiver)
            print "____________"
    except Exception, err:
        traceback.print_exc()
        print "cant send message on this number "+receiver

