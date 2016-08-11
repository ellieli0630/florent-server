# -*- coding: utf-8 -*-
import json

from neo4j.v1 import GraphDatabase, basic_auth

neoj_login = "neo4j"
neoj_password = "qwerty123"

graph_connection = GraphDatabase.driver("bolt://localhost",
                            auth=basic_auth(neoj_login, neoj_password))

yelp_API_key = {'consumer_key': 'AfzyKFR0HjJayuOi4gglAg',
                'consumer_secret': 'cxatAAfvAiMdwJFMx7q6PPqyBDk',
                'access_token_key': 'iytnvUhduTYyi2bxknY1JM1bc316psWI',
                'access_token_secret': 'b7QIpOsvSwATjvrZlTMmHpMAZPg'}

#with open("yelp_categories.json", "r") as file:
#    yelp_categories = json.load(file)
