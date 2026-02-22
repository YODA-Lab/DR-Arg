from supports import *
from pysat.examples.lbx import LBX
from algorithms import sat, skeptical_entailment
from copy import deepcopy
from pysat.examples import models
from pysat.solvers import Minisat22
from DE import *
from itertools import product
import random

def create_literal(variables):
    var = random.choice(variables)
    return var if random.random() < 0.5 else -var

def create_clause(variables, max_clause_size):
    all_literals = [var for var in variables] + [-var for var in variables]
    random.shuffle(all_literals)

    clause_size = random.randint(1, max_clause_size)
    clause = set()
    for literal in all_literals:
        if len(clause) >= clause_size:
            break

        if -literal not in clause:
            clause.add(literal)

    return list(clause)



def create_cnf(variables, num_clauses, max_clause_size):
    cnf = []
    for _ in range(num_clauses):
        clause = create_clause(variables, max_clause_size)
        # if sat(cnf, [clause]):
        if clause not in cnf:
            cnf.append(clause)
    return cnf

def is_clause_non_trivial(clause):
    literals = set(clause)
    for literal in literals:
        if -literal in literals:
            return False
    return True

def is_non_trivial(cnf):
    return all(is_clause_non_trivial(clause) for clause in cnf)



def generate_KBs(num_variables=int, num_clauses = int, max_clause_size = int, conflict_perc = float):

    variables = list(range(1, num_variables + 1))
    
    cnf = create_cnf(variables, num_clauses, max_clause_size)
    while not is_non_trivial(cnf):
        cnf = create_cnf(variables, num_clauses, max_clause_size)
    
    '''print in DIMACS '''
    # print(f"p cnf {num_variables} {num_clauses}")
    # for clause in cnf:
    #     print(" ".join(map(str, clause)) + " 0")



    def get_MCS(KB):
        # Compute minimal hitting set
        wcnf = WCNF()
        for c in KB:
            wcnf.append(c, weight=1)
       
        lbx = LBX(wcnf, use_cld=True, solver_name='g4')
        # Compute mcs and return the clauses indexes
        mcs = lbx.compute()
        return [list(wcnf.soft[m - 1]) for m in mcs]
    

    def create_KBs(cnf):
        
        mcs = get_MCS(cnf)
        KB = []
        for c in cnf:
            if c not in mcs:
                if c not in KB:
                    KB.append(c)

        return KB, mcs
        # KBh = []
        # for m in mcs:
        #     KBh.append(m)
        #     if len(KBh)/len(KBa) > conflict_perc:
        #         break
        
        # for c in KBa:
        #     if sat(KBh, [c]):
        #         KBh.append(c)
        #         if len(KBh)==len(KBa):
        #             break
     
        
        # rand_clauses = random.sample(KBa, round(len(KBa)*kb_perc))
        # to_add = random.sample(rand_clauses, round(len(rand_clauses)*(kb_perc/2)))
        # to_negate = [c for c in rand_clauses if c not in to_add]
    
        # KBh = KBh + CNF(from_clauses=to_negate).negate(topv=max(get_vars(KBa))).clauses
        # return KBa, KBh
            
    KB, mcs = create_KBs(cnf)
    return KB, mcs
