"""
@File  :main.py
@Author:Zhichen Zeng
@Date  :2020/12/12 10:26
@Desc  :this python script is the main function of this project
"""
from decompose.Decompose import Decompose
from decompose.EqSolver import EqSolver
from tear.TearSolver import TearSolver
import argparse
import textwrap

if __name__ == '__main__':  # for test
    parser = argparse.ArgumentParser(description='Configuration file',
                                     usage='use "python %(prog)s --help" for more information',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--task",
        dest="task",
        default="decompose",
        help=textwrap.dedent('''\
        Type of task, options:       
        decompose: decompose a system       
        equation: optimal solution for equations       
        tear: tear a system
        '''))
    parser.add_argument(
        "--example",
        dest="example",
        default="Decompose_ex1.txt",
        help="name of your example file"
    )

    args = parser.parse_args()

    # Decomposition
    if args.task == "decompose":
        fr = open("examples/" + args.example, 'r+')
        system = eval(fr.read())
        fr.close()
        print("Using Decomposition Solver\n")
        decomposer = Decompose(system)
        res = decomposer.decompose()
        print("\nOptimal solution for system\n" + "%s\n" % system + "is as follow:")
        for item in res:
            print(item)
        print()

    # EqSolver
    elif args.task == "equation":
        fr = open("examples/" + args.example, 'r+')
        equation = eval(fr.read())
        fr.close()
        print("Using Equation Solver\n")
        eqsolver = EqSolver(equation)
        res = eqsolver.optimalEq()
        print("\nOptimal solution for equations\n" + "%s\n" % equation + "is as follow:")
        for item in res:
            print(item)
        print()

    # TearSolver
    elif args.task == "tear":
        fr = open("examples/" + args.example, 'r+')
        print("Using Tear Solver\n")
        system = eval(fr.read())
        fr.close()
        tearsolver = TearSolver(system)
        res = tearsolver.optimalTear()
        print("\nOptimal tearing strategy for system\n" + "%s\n" % system + "is as follow:")
        print(res)

    else:
        print("invalid task type!\n")
