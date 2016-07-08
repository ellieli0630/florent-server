# -*- coding: utf-8 -*-
import types

class NodeList(list):
    def __init__(self, parent_graph, *args):
        list.__init__(self, *args)
        self.parent_graph = parent_graph

    def __matchnode(self,node1, node2):
        is_match = True
        for x in node1:
            if x in node2:
                if node1[x] == node2[x]:
                    pass
                else:
                    is_match = False
            else:
                is_match = False
        return is_match

    def First(self):
        if len(self)>0:
            return self[0]
        else:
            return self.parent_graph.Empty()


    def Match(self,node):

        if type(node) is dict:
            match_list = NodeList(self.parent_graph)
            for x in self:
                match = self.__matchnode(node, x)
                if match:
                    match_list.append(x)

        if type(node) is types.FunctionType:
            match_list = NodeList(self.parent_graph)
            for x in self:
                match = node(x)
                if match:
                    match_list.append(x)


        return match_list

    def NotEmpty(self):
        return len(self)>0

    def Empty(self):
       return len(self)==0


class Node():
    '''Node class represents a single graph node'''
    def __init__(self, parent_graph, dic, makenew=True):
        '''node constructor

        Args:
            dict - dictionary of node properties
            parent_graph - Graph object to add this node to'''

        self.dict = dic

        self.parent_graph = parent_graph
        if makenew:
            parent_graph.AddNode(self)

    def __iter__(self):
        return self.dict.__iter__()

    def __getitem__(self, item_name):
        if (item_name == 'id'):
            return str(self.dict[item_name])
        return self.dict[item_name]

    def __setitem__(self, item_name, item_value):
        self.dict[item_name] = item_value

    def __contains__(self, item):
        return item in self.dict

    def Add(self, node):
        '''Add new node as child to this node (adds directional connection)

        Args:
            node - dictionary with properties or Node class
        '''
        if type(node) is dict:
            node = Node(self.parent_graph, node)
        self.parent_graph.AddNode(node)
        self.parent_graph.AddEdge(self, node)
        return node

    def Connect(self, node):
        self.parent_graph.AddEdge(self, node)

    def ConnectsTo(self):
        return self.parent_graph.ConnectsTo(self)

    def FirstConnected(self):
        return self.parent_graph.ConnectsTo(self)[0]

    def children(self, dict):
        all_children = self.ConnectsTo()
        return all_children.Match(dict)

    def child(self, dict):
        return self.children(dict).First()








class Graph():

    def __init__(self):
        #super(Graph, self).__init__()
        self.nodes = []
        self.edges = {}
        self.last_id = 0
        self.nodes.append(Node(self,{"type":"empty"}))


    def AddNode(self, node):

        node["id"] = str(self.last_id)
        self.last_id = self.last_id + 1
        self.nodes.append(node)

    def AddEdge(self, node1, node2):
        if node1 in self.edges:
            self.edges[node1].append(node2)
        else:
            lst = NodeList(self)
            lst.append(node2)
            self.edges[node1] = lst

    def ConnectsTo(self,node):
        '''finds all nodes in the graph that are connected to selected node'''
        if node in self.edges:
            return self.edges[node]
        else:
            return NodeList(self)
    def Empty(self):
        return Node(self,{"type":"empty"})


    def __matchnode(self,node1, node2):
        is_match = True
        for x in node1:
            if x in node2:
                if node1[x] == node2[x]:
                    pass
                else:
                    is_match = False
            else:
                is_match = False
        return is_match

    def Match(self, node):
        match_list = NodeList(self)
        if type(node) is dict:
            for x in self.nodes:
                match = self.__matchnode(node, x)
                if match:
                    match_list.append(x)

        if type(node) is types.FunctionType:
            match_list = NodeList(self.parent_graph)
            for x in self:
                match = node(x)
                if match:
                    match_list.append(x)


        return match_list

