# -*- coding: utf-8 -*-
import basics


class PersistentGraph():

    def __init__(self, graph_connection):
        #super(Graph, self).__init__()
        self.nodes = []
        self.edges = {}
        self.graph_connection = graph_connection
        #self.nodes.append(Node(self,{"type":"empty"}))

    def __format_args(self, dic):
        string = ""

        for x in dic:
            prop = x

            value = dic[x]

            if prop != "type" and prop != 'id':
                string = string + "" + prop + ":'" + str(value) + "'" + ','

        string = string[:-1]
       # print string
        return string

    def __dict2query(self, node_name, dic):
        node_type = dic["type"]

        return node_name + ":" + node_type + "{" + self.__format_args(dic) + '}'

    def __dict2where(self, dic):
        string = ""
        for x in dic:
            prop = x
            value = dic[x]
            if prop != "type":
                string = string + "'" + prop + "= {" + str(value) + "}'" + ','

    def AddNode(self, node):
        session = self.graph_connection.session()
        node_type = node["type"]
        #print node_type
        strcon = "CREATE (node:" + node_type + " {" + self.__format_args(node) + '}) RETURN node'

        #print (strcon)
        result = session.run(strcon)
        node = self.__neoj2graph_query2nodes(result)[0]

        session.close()

        return node

    def AddEdge(self, node1, node2):
        session = self.graph_connection.session()
       # node1a = self.__dict2query("node1", node1)
       # node2a = self.__dict2query("node2", node2)
        query = "MATCH  (node1),(node2) WHERE  id(node1) = " + node1['id'] + " and id(node2)=" + str(node2['id']) +  " CREATE UNIQUE (node1)-[conn:CONNECTS]->(node2)"
       # print query
        #query = "MATCH (" + node1 + ")," + "(" + node2 + ")" + "CREATE UNIQUE (node1)-[conn:CONNECTS]->(node2)"
      #  print (query)
        session.run(query)
        session.close()

    def __neoj2graph_node(self, neoj):
        node = neoj["node"]
        ids = node.id
        node_type = list(node.labels)[0]
        other_props = node.properties
        new_dict = {}
        new_dict["id"] = ids
        new_dict["type"] = node_type
        for x in other_props:
            new_dict[x] = other_props[x]

        return basics.Node(self,new_dict,makenew=False)

    def __neoj2graph_query2nodes(self, result):
        rlist = []
        for  record in result:
            dic = {}
            for x in record:
                dic[x] = record[x]
            rlist.append(dic)
        rlist2 = basics.NodeList(self)
        for d in rlist:
            rlist2.append(self.__neoj2graph_node(d))

        return rlist2

    def Match(self, node):
        node1 = self.__dict2query("node", node)
        if "id" in node:
            query = "START node = NODE(" + str(node["id"]) + ')' + "MATCH (" + node1 + ") RETURN node"
            #print query
        else:
            query = "MATCH (" + node1 + ") RETURN node"
            #print query
        session = self.graph_connection.session()
        result = session.run(query)
        session.close()
        rlist2 = self.__neoj2graph_query2nodes(result)
        return rlist2

    def ConnectsTo(self, node):
        '''finds all nodes in the graph that are connected to selected node'''

        node1 = self.__dict2query("n", node)
        query = "match (" + node1 + ")-[r]-(node) return (node)"
        #print (query)
        session = self.graph_connection.session()
        result = session.run(query)
        rlist2 = self.__neoj2graph_query2nodes(result)
        session.close()
        return rlist2

    def DeleteNode(self,node):
        '''Remove node from graph'''

        node1 = self.__dict2query("n", node)
        query = "MATCH (" + node1 + ") DETACH DELETE n"

        session = self.graph_connection.session()
        session.run(query)
        #rlist2 = self.__neoj2graph_query2nodes(result)
        session.close()


    def UpdateNodeProperty(self, node, property_name, new_property_value):
        '''Updates value of node property at the database for
           permanent storage'''

        node1 = self.__dict2query("n", node)
        query = "MATCH (" + node1 + ") SET n." + property_name  + " = '" +  new_property_value + "' RETURN n"

        session = self.graph_connection.session()
        session.run(query)
        #rlist2 = self.__neoj2graph_query2nodes(result)
        session.close()









