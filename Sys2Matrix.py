"""
@File  :Sys2Matrix.py
@Author:Zhichen Zeng
@Date  :2020/12/18 9:32
@Desc  :this python script implements a function converting a system to an adjacent matrix
"""

import pandas as pd


def generateAdjacentMatrix(system):
    """
    this function transfers a system to an adjacent matrix representation
    @param system: system representation, format: {part1: [parts_connect_to 1], part2:...}
    @return adjacent matrix: adjacent matrix representation
    """
    # template for further representation
    template = {}
    for item in system:
        template[item] = 0
    dic = {}
    for item1 in system:  # iterate system nodes
        temp = template.copy()
        for item2 in system[item1]:  # iterate system nodes
            temp[item2] = 1  # item1 -> item2
        dic[item1] = temp
    adjacent_matrix = pd.DataFrame(dic).T
    # print("adjacent_matrix:\n%s" % adjacent_matrix + "\n")
    return adjacent_matrix
