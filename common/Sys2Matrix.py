"""
@File  :Sys2Matrix.py.py
@Author:Zhichen Zeng
@Date  :2020/12/12 10:18
@Desc  :this python script implements a function converting equations to an event matrix
"""

import pandas as pd


def generateEventMatrix(eq):
    """
    this function transfers a set of equations to an event matrix representation
    @param eq: equations, format: {eq1_id: [param1_id, param2_id,...], eq2_id:...}
    @return event_matrix: event matrix of equations
    """
    param_set = []  # parameters included in equations
    num_eq = 0  # number of equations
    for item in eq:
        param_set.extend(eq[item])
        num_eq += 1
    param_set = list(set(param_set))  # remove repeated parameters
    num_param = len(param_set)  # number of parameters
    print("Equation Statistics:\n" + "# equations: %d, " % num_eq + "# parameters: %d" % num_param)
    # template for further representation
    template = {}
    for i in range(len(param_set)):
        template[param_set[i]] = 0
    dic = {}
    for item1 in eq:  # iterate equations
        temp = template.copy()
        for item2 in eq[item1]:  # iterate parameters in equations
            temp[item2] = 1  # indicate item2 exists in item1
        dic[item1] = temp
    event_matrix = pd.DataFrame(dic).T
    # print("event_matrix:\n%s" % event_matrix + "\n")
    return event_matrix


def generateAdjacentMatrix(graph):
    """
    this function transfers a graph representation into a matrix representation
    @param graph: graph representation, format: {node1: [nodes_connected_to_1], node2:...}
    @return ad_matrix: adjacenet matrix
    """
    num_node = len(graph)  # number of equations
    num_edge = 0
    # template for further representation
    template = {}
    for item in graph:
        template[item] = 0
    dic = {}
    for item1 in graph:  # iterate equations
        temp = template.copy()
        for item2 in graph[item1]:  # iterate parameters in equations
            temp[item2] = 1  # indicate item2 exists in item1
            num_edge += 1
        dic[item1] = temp
    print("System Statistics:\n" + "# nodes: %d, " % num_node + "# edges: %d" % num_edge)
    ad_matrix = pd.DataFrame(dic).T
    return ad_matrix
