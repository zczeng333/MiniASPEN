"""
@File  :TearSolver.py
@Author:Zhichen Zeng
@Date  :2020/12/17 10:09
@Desc  :this python script implements a function finding optimal tearing strategy for a system with loops
"""
import numpy as np
from tear.IntProg import intProgSolver
from common.Sys2Matrix import generateAdjacentMatrix
from common.Graph import Graph


class TearSolver(object):
    def __init__(self, system, ismatrix=False):
        """
        this function initialize parameters for the tearing problem
        @param system:
        @param system: a system represented as either graph or matrix representation
        @param ismatrix: whether eq is graph representation (False), or matrix representation (True)
        """
        if ismatrix:
            self.matrix = system
        else:
            self.matrix = generateAdjacentMatrix(system)  # adjacent matrix representation of this system
        print(self.matrix)
        self.record = self.matrix.copy()  # record whether edge has been visited
        self.graph = Graph(self.matrix)  # graph representation of this system
        self.num_loop = 0  # number of loops
        self.num_node = self.matrix.shape[0]  # number of nodes
        self.num_edge = 0  # number of edges
        self.loops = {}  # record loops of this system, format {loop_name:[nodes_in_loop],...}
        self.edges = {}  # record edges of this system, format {edge_name:[nodes_connected_by_edge],...}
        for i in range(self.matrix.shape[0]):  # formulate edge-set
            for j in range(self.matrix.shape[1]):
                if self.matrix.iat[i, j] == 1:
                    self.edges[self.num_edge] = [self.graph.nodes_list[i], self.graph.nodes_list[j]]
                    self.num_edge += 1
        self.cost = np.zeros((1, self.num_edge))  # cost function for integer programming
        self.A = np.empty((0, self.num_edge))  # inequality weight for integer programming

    def loopSearch(self, input_path, node_id):
        """
        this function searches for loops starting from root, following path, going through current node
        and continuing expanding
        @param input_path: path from root to current node's parent
        @param node_id: id for current node
        @return: None
        """
        path = input_path.copy()
        path.append(node_id)
        if len(set(path)) != len(path):  # current node exists in previous path, loop exists, return path
            index = np.where(np.array(path) == path[-1])
            loop = path[index[0][0]:index[0][1] + 1]  # extract the loop inside path
            self.loops["L" + str(self.num_loop)] = loop  # store loop into loop-set
            self.updateParam(loop)  # update cost of tearing corresponding edges inside the loop
            self.num_loop += 1
            return  # recursion returns
        # no loop exists, continue recursion
        for item in self.graph.g[path[-1]].children:  # iterate all child nodes of current node
            if self.record.loc[path[-1], item] == 1:  # edge has not been visited yet
                self.record.loc[path[-1], item] = 0  # label this edge as visited
                self.loopSearch(path, item)  # recursively call depth-first-search
        return

    def updateParam(self, loop):
        """
        this function update parameters for the tearing problem whenever a loop is found
        @param loop: a newly-found loop
        @return: None
        """
        subordinate = np.zeros((1, self.num_edge))  # record edges included in this loop
        for i in range(len(loop) - 1):
            index = list(self.edges.keys())[list(self.edges.values()).index([loop[i], loop[i + 1]])]  # find edge name
            self.cost[0][index] += 1
            subordinate[0][index] = 1
        self.A = np.vstack((self.A, subordinate))

    def optimalTear(self):
        """
        this function converts a tearing problem into a integer programming problem
        @return tear_edge: an optimal set of edges ro be torn
        """
        self.loopSearch([], self.graph.nodes_list[0])  # find loops in the system
        bounds = []  # set upper and lower bound for integer programming
        for i in range(self.num_edge):
            bounds.append((0, 1))
        B = -1 * np.ones((self.num_loop, 1))  # inequality bias for integer programming
        init_x = np.ones(self.num_edge).T  # initial condition for branch and bound method
        init_val = np.dot(self.cost, init_x)  # value of objective function under initial condition
        solution = intProgSolver(self.cost, -1 * self.A, B, None, None, init_x, init_val, 0.00001)
        res_x, res_val, res_flag = solution.intProg(bounds)  # find optimal tearing strategy using integer programming
        if res_flag != 1:  # integer programming is unsolvable
            print("Problem unsolvable")
            return
        tear_edge = []
        for i in range(len(res_x)):  # format solution
            if res_x[i] == 1:
                tear_edge.append(self.edges[i])
        return tear_edge


if __name__ == "__main__":  # for test
    system = {"K": ["L"], "L": ["O", "M"], "M": ["L", "S"], "O": ["K", "S"], "S": ["K"]}
    Solver = TearSolver(system)
    res = Solver.optimalTear()
    print(res)
