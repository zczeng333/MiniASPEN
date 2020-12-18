"""
@File  :Solver.py
@Author:Zhichen Zeng
@Date  :2020/12/12 10:30
@Desc  :this python script implements a function finding the optimal solution to a set of equations
"""
from Graph import Graph
from Eq2Matrix import generateEventMatrix
from Eq2Graph import generateGraph
from OutputSelection import optimalAlignment


class EqSolver(object):
    def __init__(self, eq):
        self.eventMatrix = generateEventMatrix(eq)  # event matrix for equations
        self.alignmentMap = optimalAlignment(self.eventMatrix)
        self.matrix = generateGraph(self.eventMatrix, self.alignmentMap)
        self.loop_map = {}
        self.num_loop = 0

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

    def optimalSolution(self):
        """
        this function finds the optimal solution to a set of equations via Sargent method
        @return optimal_solution: optimal solution for equations
        """
        output_nodes = []  # recording output nodes of the graph (ordered list)
        input_nodes = []  # recording input nodes of the graph (ordered list)
        eq_id_list = self.matrix.columns.values.tolist()
        while not self.matrix.empty:
            # deal with input/output nodes
            for item in eq_id_list:
                if self.matrix.loc[item].sum() == 0:  # zero row -> output node
                    output_nodes.insert(0, [str(item)])
                    self.matrix = self.matrix.drop(labels=item)  # drop corresponding column
                    self.matrix = self.matrix.drop(labels=item, axis=1)  # drop corresponding row
                elif self.matrix[item].sum() == 0:  # zero column -> input node
                    input_nodes.append([str(item)])
                    self.matrix = self.matrix.drop(labels=item)  # drop corresponding column
                    self.matrix = self.matrix.drop(labels=item, axis=1)  # drop corresponding row
            if self.matrix.empty:
                break
            #   loopSearch for residual self.matrix
            loop_name, loop = self.loopSearch()
            self.num_loop += 1
            self.loop_map[loop_name] = loop
            eq_id_list = self.matrix.columns.values.tolist()
        # optimal_solution = reversed(input_nodes + output_nodes)
        optimal_solution = input_nodes + output_nodes
        flag = True
        while flag:  # replace imaginary nodes with actual equations
            flag = False
            for item in self.loop_map:
                for i in range(len(optimal_solution)):
                    if item in optimal_solution[i]:
                        flag = True
                        optimal_solution[i].remove(item)
                        optimal_solution[i].extend(self.loop_map[item])
                # optimal_solution = [loop_map[item] if i == item else i for i in optimal_solution]
        return optimal_solution
