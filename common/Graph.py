# coding=utf-8
"""
@File  :Graph.py
@Author:Zhichen Zeng
@Date  :2020/12/12 10:21
@Desc  :this python script implements classes for nodes and graphs
"""


class Node(object):
    def __init__(self, id='0', parent=[], children=[]):
        """
        initialize a node
        @param id: id of the node
        @param parent: id of parent nodes (list)
        @param children: id of child nodes (list)
        """
        self.id = id
        self.parent = parent
        self.children = children


class Graph(object):
    def __init__(self, matrix):
        """
        initialize a graph
        @param matrix: adjacency matrix of a graph
        """
        self.nodes_list = matrix.columns.values.tolist()  # record names of nodes
        self.g = {}
        for item1 in self.nodes_list:
            parent = []
            children = []
            for item2 in self.nodes_list:
                if matrix.loc[item1, item2] == 1:  # item1->item2
                    children.append(item2)
                if matrix.loc[item2, item1] == 1:  # item2->item1
                    parent.append(item2)
            node = Node(item1, parent, children)
            self.g[item1] = node
        # for i in self.nodes_list:
        #     print("node:%s ," % self.g[i].id + 'parent:%s ,' % self.g[i].parent + 'children:%s' % self.g[i].children)
