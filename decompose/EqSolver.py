# coding=utf-8
"""
@File  : EqSolver.py
@Author: ZC Zeng
@Date  : 2020/12/12 10:30
@Desc  : An equation solver finding optimal solution order for a set of equations
"""

from common.Sys2Matrix import generateEventMatrix
from common.Sys2Graph import generateGraph
from decompose.OutputSelection import optimalAlignment
from decompose.Decomposer import Decomposer


class EqSolver(object):
    def __init__(self, eq, ismatrix=False):
        """
        this function initializes parameter for Equations
        @param eq: a set of equations represented as either graph or matrix representation
        @param ismatrix: whether eq is graph representation (False), or matrix representation (True)
        """
        if ismatrix:
            self.eventMatrix = eq
        else:
            self.eventMatrix = generateEventMatrix(eq)  # event matrix for equations
        self.alignmentMap = optimalAlignment(self.eventMatrix)
        self.matrix = generateGraph(self.eventMatrix, self.alignmentMap)
        self.solution = []

    def optimalEq(self):
        """
        this function finds the optimal solution to a set of equations
        @return solution: optimal solution for input set of equations
        """
        solver = Decomposer(self.matrix, True)
        solution = solver.decompose()
        return solution
