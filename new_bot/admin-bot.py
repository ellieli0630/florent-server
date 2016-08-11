# -*- coding: utf-8 -*-
import Mindy.Interpreter.rule_engine as engine
from Mindy.Graph.neo4j_graph import PersistentGraph
import config
import sys
from yelp_req import get_places

rules = engine.load_rules("rules.json")
global_graph = PersistentGraph(config.graph_connection)
engine.set_main_graph(global_graph)
print "Florent Admin Bot (Using Mindy Engine)"
sent = "<start>"
user_id = "0"
while True:
    fun={}
    fun['fun']=get_places
    answer, y = engine.get_reply(rules,sent,user_id, fun)
    if answer != "":
        print ("Florent Admin Bot: " + answer)
    sys.stdout.write('You:')
    sent = sys.stdin.readline().strip()
    if sent == "exit":
        quit()
