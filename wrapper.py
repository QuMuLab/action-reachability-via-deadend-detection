import json
from pddl_parser_2.pond.parser import Problem
from pddl_parser_2.pond.predicate import Predicate
from pddl_parser_2.pond.formula import Formula, And, Primitive, Forall, When, Xor, Not, Oneof, Or
import urllib.request, json, sys, urllib3



def doit2(domain, problem):
    try:
        prob = Problem(domain, problem)
    except Exception:
            print("Failed to parse the problem -- %s\n\n%s" % (str(Exception), prob))
            return (json.dumps({'parse_status': 'err', 
                            'error': "Failed to parse the problem -- %s\n\n%s" % (str(Exception), prob)}))
    new_pred = Predicate("newpred", [])  
    primitive = Primitive(new_pred)
    prob.goal = primitive
    new_eff = And([primitive])

    for act in prob.actions:
        old_eff = act.effect
        try:                       
            act.effect = new_eff
        except Exception:
            print("The new effect doesn't work in this step-- %s\n\n%s" % (str(Exception), act))
        try:
            result_solver = callSolver(prob)
            #check status
            json.dumps({'action_name': act.name, 'find_plan': result_solver})
            print('action_name: ' + act.name + 'find_plan: ' + result_solver)
        except Exception:
            print("callSolver doesn't work-- %s\n\n%s" % (str(Exception), act))
            return (json.dumps({'parse_status': 'err',
                            'error': "The action is not usable in this step-- %s\n\n%s" % (str(Exception), act)}))
        try:
            act.effect = old_eff
            # check whether the action effect changes to its original value (We don't need to list all domains and problems)
            json.dumps({'original_eff': old_eff, 'changed_back_eff': act.effect})
            print('original_eff: ' + old_eff + ' changed_back_eff: ' + act.effect)
        except Exception:
            print("The old effect doesn't return in this step-- %s\n\n%s" % (str(Exception), act))
    

def callSolver(prob):
    prob.export("compiled_domain.pddl", "compiled_problem.pddl")
    data = {'domain': open("compiled_domain.pddl", 'r').read(),
            'problem': open("compiled_problem.pddl", 'r').read()}
    print('export works')

    http = urllib3.PoolManager()

    req = http.request("http://solver.planning.domains/solve")
    
    print("Request works")
    req.add_header('Content-Type', 'application/json')
    print("add_header works")
    resp = json.loads(urllib3.request.urlopen(req, json.dumps(data)).read())
    print('urllib.request.urlopen works')
    
    return resp['status']
  

if __name__ == '__main__':
    print("wrapper starts")
    domain = sys.argv[1]
    problem = sys.argv[2]
    doit2(domain, problem)

    # print the json here or in process_solution.py?
   




