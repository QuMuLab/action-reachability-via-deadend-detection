
import sys, json, os

if __name__ == '__main__':
    try:
        domain = sys.argv[1]
        problem = sys.argv[2]
        solution = sys.argv[3]
        solverout = sys.argv[4]
        f = open(solverout, 'r')
        print(f.read())
        f.close()

    except Exception:
        print({"parse_status": "err", "error": "json parse error-- %s\n" % (str(Exception))})

