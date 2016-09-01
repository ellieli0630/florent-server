# -*- coding: utf-8 -*-
import sys

sys.path.append("../")

import config
from yelp_req import get_places
from Mindy.Interpreter import rule_engine as engine
from Mindy.Graph.neo4j_graph import PersistentGraph

rules = engine.load_rules("rules_bc.json")
global_graph = PersistentGraph(config.graph_connection)
engine.set_main_graph(global_graph)
print "Florent Admin Bot (Using Mindy Engine)"
sent = "<start>"
user_id = "0"
while True:
    fun={}
    fun['fun']=get_places
    answer, y = engine.get_reply(rules,sent,user_id, fun)
    # print answer, y
    if answer != "":
        print ("Florent Admin Bot: " + answer)
    sys.stdout.write('You:')
    sent = sys.stdin.readline().strip()
    if sent == "exit":
        quit()
