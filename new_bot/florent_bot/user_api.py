# -*- coding: utf-8 -*-
import sys

sys.path.append("../")

import config
from yelp_req import get_places
from Mindy.Interpreter import rule_engine as engine
from Mindy.Graph.neo4j_graph import PersistentGraph

rules = engine.load_rules("user.json")
global_graph = PersistentGraph(config.graph_connection)
engine.set_main_graph(global_graph)


def process_message(message, data):

    '''
process user message and generate reply

Args:
    message - string containing message recieved from user
    data - dictionary with additional data
        {'user_phone':<phone_string>,message_time:<date_time_string>}
Returns:
    list of messages to be send [
        {'phone'':[list of phones],'message':<message_string>}]
    '''

    if 'user_phone' in data:
        phone = data['user_phone']
    else:
        phone = ''
    message=str(message)
    phone=str(phone)
    data['user_phone']=str(data['user_phone'])
    str1=''
    for c in data['user_phone']:
        if c not in ['+', ' ']:
            str1=str1+c
    data['user_phone']=str1
    data['fun']=get_places
    results, x = engine.get_reply(rules, message, phone, data)
    phones=[]
    if x=={}:
        print "You are not authorized to access this command"
        return
    else:
        str1=x['$Phone']
        str1=str(str1)
        list=str1.split('\n')
        phones.append({'phone': list, 'message': results})
    return phones

