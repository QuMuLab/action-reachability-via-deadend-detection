
import json, requests, json, sys
from pddl_parser_2.pond.parser import Problem
from pddl_parser_2.pond.predicate import Predicate
from pddl_parser_2.pond.formula import Formula, And, Primitive, Forall, When, Xor, Not, Oneof, Or

def doit2(domain, problem):
    try:
        prob = Problem(domain, problem)
    except Exception:
        return (json.dumps({'parse_status': 'err', 
                            'error': "Failed to parse the problem -- %s\n\n%s" % (str(Exception), prob)}))
    new_pred = Predicate("newpred", [])  
    primitive = Primitive(new_pred)
    prob.goal = primitive
    prob.predicates.append(new_pred)
    new_eff = And([primitive])
    tmpindex = 0
    result_list = []

    for act in prob.actions:
        tmpindex += 1
        old_eff = act.effect
        try:                       
            act.effect = new_eff
        except Exception:
        try:
            result_solver = callSolver(prob, tmpindex)
            #check status
            result_list.append([act.name, result_solver])
            
        except Exception:
            
            return (json.dumps({'parse_status': 'err',
                            'error': "The action is not usable in this step-- %s\n\n%s" % (str(Exception), act)}))
        
        act.effect = old_eff
    
    return json.dumps ({'result_list': result_list})


def callSolver(prob, tmpindex):
    prob.export("compiled_domain.pddl", "compiled_problem.pddl")

    # check whether the action effect changes to its original value by listing all domains and problems
    domain_name = 'domain' + str(tmpindex)
    prob_name = 'problem' + str(tmpindex)
    json.dumps = ({domain_name: open("compiled_domain.pddl", 'r').read(), prob_name: open("compiled_problem.pddl", 'r').read()})

    data = {'domain': open("compiled_domain.pddl", 'r').read(),
            'problem': open("compiled_problem.pddl", 'r').read()}

    

    r = requests.post('http://solver.planning.domains/solve', verify=False, json=data)
    resp = r.json()
    # all results are error, something wrong
    
    return resp['status']


if __name__ == '__main__':
    
    domain = sys.argv[1]
    problem = sys.argv[2]
    print(doit2(domain, problem))

    # print the json here or in process_solution.py?
   




