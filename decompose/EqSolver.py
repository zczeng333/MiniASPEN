# coding=utf-8
"""
@File  : EqSolver.py
@Author: ZC Zeng
@Date  : 2020/12/12 10:30
@Desc  : An equation solver finding optimal solution order for a set of equations
"""

from common.Sys2Matrix import generateEventMatrix
from common.Sys2Graph import generateGraph
from common.EqParse import eqsReformat
from decompose.OutputSelection import optimalAlignment
from decompose.Decomposer import Decomposer


class EqSolver(object):
    def __init__(self, eq_string, ismatrix=False):
        """
        this function initializes parameter for Equations
        @param eq: a set of equations represented as either graph or matrix representation
        @param ismatrix: whether eq is graph representation (False), or matrix representation (True)
        """
        self.eq_string = eq_string
        self.eq = eqsReformat(self.eq_string)
        if ismatrix:
            self.eventMatrix = self.eq
        else:
            self.eventMatrix = generateEventMatrix(self.eq)  # event matrix for equations
        print("%s" % self.eq_string + "\n")
        self.alignmentMap = optimalAlignment(self.eventMatrix)
        self.matrix = generateGraph(self.eventMatrix, self.alignmentMap)
        self.solution = []

    def optimalEq(self):
        """
        this function finds the optimal solution to a set of equations
        @return solution: optimal solution for input set of equations
        """
        solver = Decomposer(self.matrix, True, False)
        solution = solver.decompose()
        # format output string
        res_str = 'Optimal solution\n' + '----------------\n'
        if len(solution) != 0:
            for item in solution:
                res_str = res_str + str(item) + '\n'
            print(res_str)
        return solution
