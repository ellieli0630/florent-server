# -*- coding: utf-8 -*-
from neo4j.v1 import GraphDatabase, basic_auth
neoj_login = "neo4j"
neoj_password = "wer321"

graph_connection = GraphDatabase.driver("bolt://localhost",
                            auth=basic_auth(neoj_login, neoj_password))
