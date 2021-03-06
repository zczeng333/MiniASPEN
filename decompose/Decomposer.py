# coding=utf-8
"""
@File  : Decomposer.py
@Author: ZC Zeng
@Date  : 2020/12/19 10:52
@Desc  : A decomposition solver decomposing an integrated system into several subsystems
"""
from common.Graph import Graph
from common.Sys2Matrix import generateAdjacentMatrix


class Decomposer(object):
    def __init__(self, system, ismatrix=False, show=True):
        """
        this function initializes parameters for decomposition process
        @param system: a system represented as either graph or matrix representation
        @param ismatrix: whether eq is graph representation (False), or matrix representation (True)
        @param show: whether print solver result in console
        """
        self.system = system
        self.show = show
        if ismatrix:
            self.matrix = self.system
        else:
            self.matrix = generateAdjacentMatrix(self.system)  # event matrix for equations
        self.loop_map = {}
        self.num_loop = 0
        self.solution = []
        if show:
            print(self.matrix)

    def loopSearch(self):
        """
        this function finds loop inside a matrix based on adjacency matrix
        @return loop_name: name of detected loop
        @return loop: nodes forming a loop (list form)
        """
        # start depth-first-search
        nodes_list = self.matrix.columns.values.tolist()  # unvisited nodes
        nodes_visited = []  # visited nodes
        nodes_unvisited = [nodes_list[0]]  # nodes to be visited
        loop_index = self.num_loop  # index for loops (imaginary nodes)
        # convert graph representation from adjacency matrix to index form
        graph = Graph(self.matrix)
        while len(nodes_unvisited) > 0:
            node_id = nodes_unvisited[0]  # id for nodes to be visited
            del nodes_unvisited[0]
            node = graph.g[node_id]
            for item1 in node.children:
                if item1 in nodes_visited:  # find loop
                    loop = nodes_visited[nodes_visited.index(item1):]
                    loop.append(node_id)
                    # generate imaginary node
                    input_nodes = []  # input nodes for imaginary node
                    output_nodes = []  # output nodes for imaginary node
                    loop_name = 'L' + str(loop_index)  # name for imaginary node
                    self.matrix.loc[loop_name] = 0  # add row
                    self.matrix[loop_name] = 0  # add column
                    for item2 in loop:
                        input_nodes.extend(graph.g[item2].parent)
                        output_nodes.extend(graph.g[item2].children)
                        self.matrix = self.matrix.drop(labels=item2)  # drop corresponding column
                        self.matrix = self.matrix.drop(labels=item2, axis=1)  # drop corresponding row
                    input_nodes = list(set(input_nodes))
                    output_nodes = list(set(output_nodes))
                    nodes_list = self.matrix.columns.values.tolist()
                    for item2 in nodes_list:
                        if item2 in input_nodes:
                            self.matrix.loc[item2, loop_name] = 1
                        if item2 in output_nodes:
                            self.matrix.loc[loop_name, item2] = 1
                    return loop_name, loop
                else:  # add child node to the start of the unvisited node list
                    nodes_unvisited.insert(0, item1)
            nodes_visited.append(node_id)  # add current node to visited node list
        return None, None  # not solvable

    def decompose(self):
        """
        this function decomposes a system via Sargent method
        @return self.solution: optimal solution for equations
        """
        output_nodes = []  # recording output nodes of the graph (ordered list)
        input_nodes = []  # recording input nodes of the graph (ordered list)
        node_list = self.matrix.columns.values.tolist()
        while not self.matrix.empty:
            # deal with input/output nodes
            tmp_output = []
            tmp_input = []
            for item in node_list:
                if self.matrix.loc[item].sum() == 0:  # zero row -> output node
                    tmp_output.insert(0, str(item))
                    # output_nodes.insert(0, [str(item)])
                    self.matrix = self.matrix.drop(labels=item)  # drop corresponding column
                    self.matrix = self.matrix.drop(labels=item, axis=1)  # drop corresponding row
                elif self.matrix[item].sum() == 0:  # zero column -> input node
                    # input_nodes.append([str(item)])
                    tmp_input.append(str(item))
                    self.matrix = self.matrix.drop(labels=item)  # drop corresponding column
                    self.matrix = self.matrix.drop(labels=item, axis=1)  # drop corresponding row
            if len(tmp_output) != 0:
                output_nodes.insert(0, tmp_output)
            if len(tmp_input) != 0:
                input_nodes.append(tmp_input)
            if self.matrix.empty:
                break
            #   loopSearch for residual self.matrix
            loop_name, loop = self.loopSearch()
            self.num_loop += 1
            self.loop_map[loop_name] = loop
            node_list = self.matrix.columns.values.tolist()
        # self.solution = reversed(input_nodes + output_nodes)
        self.solution = input_nodes + output_nodes
        flag = True
        while flag:  # replace imaginary nodes with actual equations
            flag = False
            for item in self.loop_map:
                for i in range(len(self.solution)):
                    if item in self.solution[i]:
                        flag = True
                        self.solution[i].remove(item)
                        self.solution[i].extend(self.loop_map[item])
        # format output string
        if self.show:
            res_str = '\nOptimal decomposition\n' + '---------------------\n'
            if len(self.solution) != 0:
                for item in self.solution:
                    res_str = res_str + str(item) + '\n'
                print(res_str)
        return self.solution
