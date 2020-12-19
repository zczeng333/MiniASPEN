"""
@File  :main.py
@Author:Zhichen Zeng
@Date  :2020/12/12 10:26
@Desc  :this python script is the main function of this project
"""
from decompose.Decompose import Decompose
from decompose.EqSolver import EqSolver
from tear.TearSolver import TearSolver

if __name__ == '__main__':  # for test
    # Decomposition Test
    system = {'A': ['B'], 'B': ['C'], 'C': ['A', 'D', 'E'], 'D': ['B', 'E'], 'E': ['C', 'F'], 'F': 'G', 'G': ['F', 'I'],
              'H': 'B', 'I': []}
    decomposer = Decompose(system)
    res = decomposer.decompose()
    print("optimal solution for system\n" + "%s\n" % system + "is as follow:")
    for item in res:
        print(item)
    print()

    # EqSolver Test
    equation = {'f1': ['x1', 'x4'], 'f2': ['x2', 'x3', 'x4', 'x5'], 'f3': ['x1', 'x2', 'x4'], 'f4': ['x1', 'x4'],
                'f5': ['x1', 'x3', 'x5']}
    eqsolver = EqSolver(equation)
    res = eqsolver.optimalEq()
    print("optimal solution for equations\n" + "%s\n" % equation + "is as follow:")
    for item in res:
        print(item)
    print()

    # TearSolver Test
    system = {"K": ["L"], "L": ["O", "M"], "M": ["L", "S"], "O": ["K", "S"], "S": ["K"]}
    tearsolver = TearSolver(system)
    res = tearsolver.optimalTear()
    print("optimal tearing strategy for system\n" + "%s\n" % system + "is as follow:")
    print(res)
