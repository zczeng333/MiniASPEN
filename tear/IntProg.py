# coding=utf-8
"""
@File  : IntProg.py
@Author: ZC Zeng
@Date  : 2020/12/17 19:26
@Desc  : A integer programming solve based on branch and bound method
"""

from scipy.optimize import linprog
import numpy as np


class intProgSolver(object):
    def __init__(self, c, A, B, Aeq, beq, x, val, threshold):
        """
        this function initializes the following integer programming problem
        minimize cx
        s.t. A*x <= B, Aeq*x = beq, vlb <= x <= vub, x is an integer vector
        @param c: weight vector forming the objective function
        @param A: weight matrix forming inequality constraints
        @param B: bias vector forming inequality constraints
        @param Aeq: weight matrix forming equality constraints
        @param beq: bias matrix forming equality constraints
        @param x: current best solution
        @param val: current best objective function
        @param threshold: convergence threshold
        """
        self.c = c
        self.A = A
        self.B = B
        self.Aeq = Aeq
        self.beq = beq
        self.best_x = x
        self.best_val = val
        self.best_flag = 100
        self.threshold = threshold

    def intProg(self, bounds):
        """
        this function solves integer programming problem with variables constrained in bounds
        @param bounds: [(lower_bound1, upper_bound_1),(lower_bound2, upper_bound2),...]
        @return return_x: solution under current bounds
        @return return_val: value of objective function
        @return return_flag: flag=1 indicates problem is solvable, problem is unsolvable otherwise
        """
        res = linprog(self.c, self.A, self.B, self.Aeq, self.beq, bounds)
        temp_x = res["x"]
        temp_val = res["fun"]
        status = res["status"]
        if status != 0:  # linear programming is unsolvable
            return_x = temp_x
            return_val = temp_val
            return_flag = -1
            return return_x, return_val, return_flag
        if max(abs(temp_x - np.around(temp_x))) > self.threshold:  # needs more iteration for convergence
            if temp_val > self.best_val:  # pruning: this branch does not contain optimal solution
                return_x = temp_x
                return_val = temp_val
                return_flag = -1
                return return_x, return_val, return_flag
            else:  # otherwise, this branch still needs further exploration (jump out of this if-else judgement)
                pass
        else:  # iteration converged
            if temp_val > self.best_val:  # pruning: this branch does not contain optimal solution
                return_x = temp_x
                return_val = temp_val
                return_flag = -1
                return return_x, return_val, return_flag
            else:  # new solution is optimal, store new solution as the best solution
                self.best_x = temp_x
                self.best_val = temp_val
                self.best_flag = 1
                return_x = temp_x
                return_val = temp_val
                return_flag = 1
                return return_x, return_val, return_flag

        # choose the best dimension for optimization
        ex = np.array(abs(temp_x - np.around(temp_x)))
        dim = np.where(ex > self.threshold)[0][0]
        if bounds[dim][0] <= int(temp_x[dim]):  # update lower bound, split branch
            temp_bounds = bounds.copy()
            temp_bounds[dim] = (bounds[dim][0], int(temp_x[dim]))
            self.intProg(temp_bounds)
        if bounds[dim][1] >= int(temp_x[dim]) + 1:  # update upper bound, split branch
            temp_bounds = bounds.copy()
            temp_bounds[dim] = (int(temp_x[dim]) + 1, bounds[dim][1])
            self.intProg(temp_bounds)
        return_x = self.best_x
        return_val = self.best_val
        return_flag = self.best_flag
        return np.around(return_x), np.around(return_val), return_flag
