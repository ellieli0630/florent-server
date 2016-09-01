# -*- coding: utf-8 -*-
import user_bc_api
import sys

sys.path.append("../")

from Mindy.Nlp.tools import date2timestamp
from yelp_req import get_places


print ("User message interface interactive test")
print ("type test messages like:")
print ('@subsribers send message to "We are glad to see" to all subscribers for event with id=19')
print ()

do = True
while do:
    sys.stdout.write('>>')
    input_data = sys.stdin.readline().strip()
    data = {}
    if "|" in input_data:
        vars2 = input_data.split("|")[1]
        vars2 = vars2.split("=")
        input_data = input_data.split("|")[0]
        try:
            dta = date2timestamp(vars2[1]. strip())
            data[vars2[0].strip()] = dta
        except:
            data[vars2[0].strip()] = vars2[1].strip()
    # print "input data:"
    # print input_data
    # print type(input_data)
    answer = user_bc_api.process_message(input_data, data)
    #for i in range(len(answer['phone'])):
    #    send_sms(+19788194149, answer['message'], answer['phone'][i])
    #send_sms(+19788194149, 'Messages sent', data['phone'])
    print (answer)
