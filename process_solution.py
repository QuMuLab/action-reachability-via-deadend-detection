
import sys, json, os

if __name__ == '__main__':

    domain = sys.argv[1]
    problem = sys.argv[2]
    solution = sys.argv[3]
    solverout = sys.argv[4]

    with open(solverout, 'r') as f:
        print(f.read())

