"""
@File  :main.py
@Author:Zhichen Zeng
@Date  :2020/12/12 10:26
@Desc  :this python script is the main function of this project
"""
from decompose.Decomposer import Decomposer
from decompose.EqSolver import EqSolver
from tear.TearSolver import TearSolver
from exchanger.HENSolver import HENSolver
from common.EqParse import eqsReformat
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
        fr = open('./examples/' + args.problem_set, 'r+')
        system = eval(fr.read())
        fr.close()
        print('Using Decomposition Solver\n')
        decomposer = Decomposer(system)
        res = decomposer.decompose()
        print('\nOptimal decomposition for system\n' + '%s\n' % system + 'is as follow:')
        if len(res) != 0:
            for item in res:
                print(item)
            print()

    # EqSolver
    elif args.task == 'equation':
        print('Using Equation Solver\n')
        fr = open('./examples/' + args.problem_set, 'r+')
        eq_string = str(fr.read())
        equation = eqsReformat(eq_string)
        fr.close()
        eqsolver = EqSolver(equation)
        res = eqsolver.optimalEq()
        print('\nOptimal solution for equations\n' + '%s\n' % eq_string + 'is as follow:')
        if len(res) != 0:
            for item in res:
                print(item)
            print()

    # TearSolver
    elif args.task == 'tear':
        fr = open('./examples/' + args.problem_set, 'r+')
        print('Using Tear Solver\n')
        system = eval(fr.read())
        fr.close()
        if args.cost != '1' and args.cost != '2':
            print('Invalid cost function type, choose either 1 or 2')
        else:
            tearsolver = TearSolver(system, args.cost)
            res = tearsolver.optimalTear()
            if res != None:
                print('\nOptimal tearing strategy for system\n' + '%s\n' % system + 'is as follow:')
                for item in res:
                    print('%s' % item[0] + ' -> ' + '%s' % item[1])
                print()

    # HENSolver
    elif args.task == 'hen':
        fr = open('./examples/' + args.problem_set, 'r+')
        print('Using HEN Solver\n')
        system = eval(fr.read())
        fr.close()
        hensolver = HENSolver(system)
        res = hensolver.optimalHEN()


    else:
        print('invalid task type!\n')

