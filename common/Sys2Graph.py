"""
@File  :Sys2Graph.py
@Author:Zhichen Zeng
@Date  :2020/12/12 10:20
@Desc  :this python script implements a function converting equations to a graph based on output alignment
"""

import pandas as pd
import numpy as np


def generateGraph(event_matrix, alignment_map):
    """
    this function transfers a set of equations to a directed graph representation
    @param event_matrix:  event matrix of equations
    @param alignment_map: optimal alignment between parameters and equations
    @return graph: directed graph representation for equations
    """
    eq_id_list = event_matrix._stat_axis.values.tolist()  # id for equations
    graph = pd.DataFrame(data=np.zeros((len(eq_id_list), len(eq_id_list))), columns=eq_id_list, index=eq_id_list)
    # generate directed graph for equations
    for item1 in alignment_map:  # iterate equations
        param = alignment_map[item1]  # corresponding parameter aligned with item1
        for item2 in eq_id_list:
            if event_matrix.loc[item2, param] == 1 and item1 != item2:
                graph.loc[item1, item2] = 1
    # print("Directed graph for equations:")
    # print("%s\n" % graph)
    return graph
