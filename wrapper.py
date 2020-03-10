import json
from pddl-parser-2.pond.parser import Problem
from pddl-parser-2.pond.formula import Formula, And, Primitive, Forall, When, Xor, Not, Oneof, Or
from process_solution import doit
import urllib3, json, sys



def doit2(domain, problem, solver_output):
    try:
        prob = Problem(domain, problem)
    except Exception:
            return (json.dumps({'parse_status': 'err', 'output': solver_output,
                            'error': "Failed to parse the problem -- %s\n\n%s" % (str(Exception), prob)}))
    print("doit2 starts")
    new_pred =Predicate("newpred")  
    primitive = Primitive(new_pred)
    goal = new_pred 

    for act in prob.actions:
        old_eff = act.effect
        try:            
            new_eff = And(primitive)
            act.effect = new_eff
            solution = callSolver(prob)
        except Exception:
            print(json.dumps({'parse_status': 'err', 'output': solver_output,
                            'error': "The action is not usable in this step-- %s\n\n%s" % (str(Exception), act)}))
        act.effect = old_eff
    
    doit("plan.ipc", solver_output)
    

def callSolver(probData):
    
    req = urllib3.Request("http://solver.planning.domains/solve")
    req.add_header('Content-Type', 'application/json')
    resp = json.loads(urllib3.urlopen(req, json.dumps(data)).read())

    with open("plan.ipc", 'a') as f:
        f.write('\n'.join([act['name'] for act in resp['result']['plan']]))
        print('\n'.join([act['name'] for act in resp['result']['plan']]))
    
    #check status

if __name__ == '__main__':
    print("wrapper starts")
    domain = sys.argv[1]
    problem = sys.argv[2]
    solverout = sys.argv[3]
    doit2(domain, problem, solverout)



