import json
import requests, json, sys, urllib3
from pddl_parser_2.pond.parser import Problem
from pddl_parser_2.pond.predicate import Predicate
from pddl_parser_2.pond.formula import Formula, And, Primitive, Forall, When, Xor, Not, Oneof, Or

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
    prob.predicates.append(new_pred)
    new_eff = And([primitive])
    tmpindex = 0

    for act in prob.actions:
        tmpindex += 1
        old_eff = act.effect
        try:                       
            act.effect = new_eff
        except Exception:
            print("The new effect doesn't work in this step-- %s\n\n%s" % (str(Exception), act))
        try:
            result_solver = callSolver(prob, tmpindex)
            #check status
            json.dumps({'action_name': act.name, 'find_plan': result_solver})
            print('action_name: ' + act.name + ' find_plan: ' + result_solver)
        except Exception:
            print("callSolver doesn't work-- %s\n\n%s" % (str(Exception), act))
            return (json.dumps({'parse_status': 'err',
                            'error': "The action is not usable in this step-- %s\n\n%s" % (str(Exception), act)}))
        try:
            act.effect = old_eff
        except Exception:
            print("The old effect doesn't return in this step-- %s\n\n%s" % (str(Exception), act))
    

def callSolver(prob, tmpindex):
    prob.export("compiled_domain.pddl", "compiled_problem.pddl")

    # check whether the action effect changes to its original value by listing all domains and problems
    domain_name = 'domain' + str(tmpindex)
    prob_name = 'problem' + str(tmpindex)
    json.dumps = ({domain_name: open("compiled_domain.pddl", 'r').read(), prob_name: open("compiled_problem.pddl", 'r').read()})

    data = {'domain': open("compiled_domain.pddl", 'r').read(),
            'problem': open("compiled_problem.pddl", 'r').read()}

    print('export works')

    r = requests.post('http://solver.planning.domains/solve', verify=False, json=data)
    resp = r.json()
    # all results are error, something wrong
    
    return resp['status']


if __name__ == '__main__':
    print("wrapper starts")
    domain = sys.argv[1]
    problem = sys.argv[2]
    doit2(domain, problem)

    # print the json here or in process_solution.py?
   




