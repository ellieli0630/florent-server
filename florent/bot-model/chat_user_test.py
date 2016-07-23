# -*- coding: utf-8 -*-
import user_api
import sys
from  Mindy.Nlp.tools import date2timestamp

print ("User message interface interactive test")
print ("type test messanges like:")
print ('send reply to "We are glad to see!" to all subscribers for event with id=4')
print ()

do = True
while do:
    sys.stdout.write('>>')
    input_data = sys.stdin.readline()
    data = {}
    if "|" in input_data:
        vars2 = input_data.split("|")[1]
        vars2 = vars2.split("=")
        try:
            dta = date2timestamp(vars2[1]. strip())
            data[vars2[0].strip()] = dta
        except:
            data[vars2[0].strip()] = vars2[1].strip()

    answer = user_api.process_owner_message(input_data, data)
    print (answer)
