import datetime
import tornado.escape
import tornado.ioloop
import tornado.web
import sys
import json
from user_api import process_message
from sms_bc_sender import send_sms

class postReplyHandler(tornado.web.RequestHandler):
    def post(self):
        print self.request.body
        receiver = {'user_phone': self.get_arguments("To")}
        text = self.get_arguments("Body")
        text[0]=str(text[0])
        date = self.get_arguments("DateSent")
        if date != []:
            message_info={'datetime':date[0]}
        else:
            date=datetime.datetime.now()
            message_info = {'datetime': date}
        f=self.get_body_arguments("From")
        f=(f[0])
        f=str(f)
        message_info = {'user_phone':f}
        data_sending=process_message(text[0], message_info)
        for i in range(len(data_sending[0]['phone'])):
            send_sms(message_info['user_phone'], str(data_sending[0]['phone'][i]), (data_sending[0]['message']))

application = tornado.web.Application([
    (r"/bot", postReplyHandler)
])


if __name__ == "__main__":
    application.listen(8889)
    tornado.ioloop.IOLoop.instance().start()
