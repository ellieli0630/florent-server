# -*- coding: utf-8 -*-
import user_api
import sys
from  Mindy.Nlp.tools import date2timestamp

print ("User message interface interactive test")
print ("type test messanges like:")
print ('@a "Best Restaurant" feedback |message_time=11-08-2016 10:30am')
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

    answer = user_api.process_user_message(input_data, data)
    print (answer)
