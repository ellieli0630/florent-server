# -*- coding: utf-8 -*-
import Mindy.Interpreter.rule_engine as engine
#from Mindy.Graph.basics import Node,NodeList,Graph

from Mindy.Graph.neo4j_graph import PersistentGraph
import config


rules = engine.load_rules("user.json")
global_graph = PersistentGraph(config.graph_connection)
engine.set_main_graph(global_graph)


def process_user_message(message, data):
    ''' process user message and generate reply

    Args:
        message - string containing message recieved from user
        data - dictionary with additional data
            {'user_phone':<phone_string>,message_time:<date_time_string>}
    Returns:
        list of messages to be send [
            {'user_phone'':<phone_string>,'message':<message_string>}]
    '''
    if 'user_phone' in data:
        user_phone = data['user_phone']
    else:
        user_phone = ''

    results, y = engine.get_reply(rules, message, user_phone, data)

    return [{'message': results, 'user_phone': user_phone}]


def real_owner(data):
    if 'user_name' in data:
        user_name=data['user_name']
    results, x = engine.get_reply(rules, message, user_phone, data)
    if x!=data['user_phone']:
        return False
    else:
        return True


def process_owner_message(message, data):

    if 'user_phone' in data:
        user_phone = data['user_phone']
    else:
        user_phone = ''
    #print "process owner message"
    results, x = engine.get_reply(rules, message, user_phone, data)
    phones=[]
    #for i in range(len(x)):
        #print "phone is"
        #print x['$Phone']
    str1=x['$Phone']
    list=str1.split('\n')
    #phones.append({'phone': x['$Phone'], 'message': results})
    phones.append({'phone': list, 'message': results})
    return phones

