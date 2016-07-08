# -*- coding: utf-8 -*-
import Mindy.Interpreter.rule_engine as engine
from Mindy.Graph.basics import Node,NodeList,Graph
#from Mindy.Graph.neo4j_graph import PersistentGraph
import config
import sys
#import config
rules = engine.load_rules("rules.json")
#global_graph = PersistentGraph(config.graph_connection)
global_graph = Graph()

engine.set_main_graph(global_graph)
print "Florent Admin Bot (Using Mindy Engine)"


sent = "<start>"
user_id = "1"

while True:
    answer = engine.get_reply(rules,sent,user_id)
    if answer != "":
        print ("Florent Admin Bot: " + answer)
    #print (engine.get_debug_info(sent))
   # print (global_graph.Match({}))
    sys.stdout.write('You:')
    sent = sys.stdin.readline().strip().encode("utf-8")
    if sent == "exit":
        quit()