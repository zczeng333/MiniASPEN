# coding=utf-8
"""
@File  : MiniASPEN.py
@Author: ZC Zeng
@Date  : 2020/12/12 10:26
@Desc  : this python script is the main function of this project
"""
from decompose.Decomposer import Decomposer
from decompose.EqSolver import EqSolver
from tear.TearSolver import TearSolver
from exchanger.HENSolver import HENSolver
import argparse
import textwrap

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Configuration file',
                                     usage='use "python %(prog)s --help" for more information',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '--task',
        dest='task',
        default='hen',
        help=textwrap.dedent('''\
        type of task, options:       
        decompose: decompose a system       
        equation: optimal solution for equations       
        tear: tear a system
        hen: heat exchange network synthesis
        '''))
    parser.add_argument(
        '--problem_set',
        dest='problem_set',
        default='streams_1.txt',
        help='name of your problem set'
    )
    parser.add_argument(
        '--cost',
        dest='cost',
        default='1',
        help='cost function for tearing'
    )

    args = parser.parse_args()

    # Decomposition
    if args.task == 'decompose':
        print('\nUsing Decomposition Solver\n' + '--------------------------\n')
        fr = open('./examples/' + args.problem_set, 'r+')
        system = eval(fr.read())
        fr.close()
        decomposer = Decomposer(system)
        res = decomposer.decompose()

    # EqSolver
    elif args.task == 'equation':
        print('\nUsing Equation Solver\n' + '---------------------\n')
        fr = open('./examples/' + args.problem_set, 'r+')
        eq_string = str(fr.read())
        fr.close()
        eqsolver = EqSolver(eq_string)
        res = eqsolver.optimalEq()

    # TearSolver
    elif args.task == 'tear':
        print('\nUsing Tear Solver\n' + '-----------------\n')
        fr = open('./examples/' + args.problem_set, 'r+')
        system = eval(fr.read())
        fr.close()
        if args.cost != '1' and args.cost != '2':
            print('Invalid cost function type, choose either 1 or 2')
        else:
            tearsolver = TearSolver(system, args.cost)
            res = tearsolver.optimalTear()

    # HENSolver
    elif args.task == 'hen':
        print('\nUsing HEN Solver\n' + '----------------\n')
        fr = open('./examples/' + args.problem_set, 'r+')
        system = eval(fr.read())
        fr.close()
        hensolver = HENSolver(system)
        hensolver.optimalHEN()

    else:
        print('invalid task type!\n')
