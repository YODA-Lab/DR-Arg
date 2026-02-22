import pandas as pd
from supports import *
from pysat.examples.lbx import LBX
from algorithms import sat, skeptical_entailment
from copy import deepcopy
from pysat.examples import models
from pysat.solvers import Minisat22
from DE import dialogue, Agent, Human
from random_KBs_generator import generate_KBs
import time
import pandas as pd
from itertools import product
from negate_CNF import negate_cnf
import subprocess
import tempfile
import os
from pysat.formula import CNF



'''
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
'''


def is_satisfiable(KB1, KB2):
    # Check if a formula is satisfiable
    s = Solver(name='g4')
    for k in KB1:
    	s.add_clause(k)

    for k in KB2:
    	s.add_clause(k)
    if s.solve():
    	return True
    else:
    	return False

def compute_minimal_retraction_set(KB, clauses_to_add):
    # Compute minimal hitting set to retract from KB to accommodate clauses_to_add
    wcnf = WCNF()
    for c in KB: # add KB clauses as soft constraints (to be removed)
        wcnf.append(c, weight=1)
    for c in clauses_to_add: # add clauses_to_add as hard constraints
        wcnf.append(c)
    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    mcs = lbx.compute()
    return [list(wcnf.soft[m - 1]) for m in mcs]


def revise_knowledge_base(KB, clauses_to_add):
    '''
    Revise the knowledge base KB to incorporate clauses_to_add.
    If KB U clauses_to_add is satisfiable, simply add clauses_to_add to KB.
    Otherwise, retract a minimal set of clauses from KB to make KB U clauses_to_add satisfiable.
    '''
    if is_satisfiable(KB, clauses_to_add):
        return KB + clauses_to_add
    else:
        clauses_to_retract = compute_minimal_retraction_set(KB, clauses_to_add)
        new_KB = []
        for k in KB:
            if k not in clauses_to_retract:
                new_KB.append(k)
        return new_KB + clauses_to_add



def check_query_satisfaction_with_revision(KB, history_D, query):
    '''
    Checks for skeptical entailment of a query q given a KB and a history of dialogues D.
    The KB is updated iteratively with clauses from D, and entailment is checked at each step.
    '''
    updated_KB = deepcopy(KB) # To avoid modifying the original KB
    dialogue_turns = sorted(history_D.keys(), reverse=True) # Process dialogue history from latest to earliest
    num_revisions = 0
    for turn in dialogue_turns:
        clauses_from_dialogue = history_D[turn] # Assuming D[turn] is a list of clauses
        updated_KB = revise_knowledge_base(updated_KB, clauses_from_dialogue)
        num_revisions += 1
        if skeptical_entailment(updated_KB, [], query):
            return updated_KB, num_revisions # Return updated KB and number of revisions

    return None # Return None if query is not entailed after processing all dialogue turns


def compute_prime_implicates(KB, n_models=10000):
    '''
    Computes prime implicates that are unit clauses from a given knowledge base KB.
    It enumerates up to n_models to find prime implicates.
    '''
    assumables = []
    vars_in_kb = get_vars(KB)
    all_vars_up_to_max = range(1, max(vars_in_kb)+1) if vars_in_kb else [] # Handle empty KB case
    for v in all_vars_up_to_max:
        if v not in vars_in_kb:
            assumables.append(v)

    models_found = []
    with Minisat22(bootstrap_with=KB) as solver:
        for model in solver.enum_models(assumptions=assumables):
            models_found.append(model)
            if len(models_found) == n_models:
                break

    prime_implicates_E = set()
    variables_in_KB = get_vars(KB)
    for var in variables_in_KB:
        if all(var in m for m in models_found):
            prime_implicates_E.add(var)
        elif all(-var in m for m in models_found):
            prime_implicates_E.add(-var)
    return prime_implicates_E


def compute_prime_implicates_cadiback(KB):
    """
    Computes prime implicates (unit clauses) of a knowledge base using Cadiback.

    Args:
        KB: A list of clauses representing the knowledge base in CNF.

    Returns:
        A set of prime implicates (unit clauses) as integers.
    """
    # Create a temporary file to store the KB in DIMACS format using PySAT
    cnf = CNF(from_clauses=KB) # Initialize CNF object directly with KB

    with tempfile.NamedTemporaryFile(mode='w', suffix='.cnf', delete=False) as temp_file:
        temp_file_path = temp_file.name
        cnf.to_file(temp_file_path)

    # print(f"CNF File Content for Cadiback:") # Print CNF file content for debugging
    # with open(temp_file_path, 'r') as f:
    #     print(f.read())
    # print(f"Temp file path: {temp_file_path}") # Print temp file path for manual execution

    # Run Cadiback and capture its output
    try:
        cadiback_command = ["./cadiback", temp_file_path, "-q"] # Assuming cadiback is in the same directory and executable
        result = subprocess.run(cadiback_command, capture_output=True, text=True, check=False)
        output_lines = result.stdout.strip().split('\n')
        print(f"Cadiback stdout: {result.stdout}") # Print stdout for debugging
    except subprocess.CalledProcessError as e:
        print(f"Cadiback execution failed: {e}")
        print(f"Cadiback stderr: {e.stderr}") # Print stderr for debugging
        return set() # Return empty set in case of error
    finally:
        os.remove(temp_file_path) # Clean up the temporary file

    prime_implicates = set()
    for line in output_lines:
        if line.startswith("b "): # 'b' indicates unit prime implicates in Cadiback output
            parts = line[2:].strip().split()
            for part in parts:
                try:
                    lit = int(part)
                    if lit != 0:
                        prime_implicates.add(lit)
                except ValueError:
                    pass # Ignore non-integer parts if any

    return prime_implicates


def calculate_understanding_score(KB1, KB2, alpha=0.5, n_models=10000):
    '''
    Calculates an understanding score between two knowledge bases KB1 and KB2.
    The score is a weighted average of semantic and syntactic similarity.
    Semantic similarity is based on the Sorensen-Dice index of prime implicates.
    Syntactic similarity is based on the Sorensen-Dice index of clause overlap.
    '''
    E1 = compute_prime_implicates(KB1, n_models)
    E2 = compute_prime_implicates(KB2, n_models)

    # Semantic Similarity (Sorensen-Dice index on prime implicates)
    E_intersection = E2.intersection(E1)
    semantic_similarity  = (2*len(E_intersection))/(len(E1)+len(E2)) if (len(E1)+len(E2)) > 0 else 0.0 # Avoid division by zero

    # Syntactic Similarity (Sorensen-Dice index on clause overlap)
    KB_intersection = []
    for clause1 in KB1:
        if clause1 in KB2:
            KB_intersection.append(clause1)
    syntactic_similarity = (2*len(KB_intersection))/(len(KB1)+len(KB2)) if (len(KB1)+len(KB2)) > 0 else 0.0 # Avoid division by zero

    return alpha*semantic_similarity + (1-alpha)*syntactic_similarity


def satisfaction_with_understanding(KB_explainer, KB_explainee_initial, dialogue_history_D, query):
    '''
    Evaluates satisfaction and understanding during a dialogue.
    It iteratively revises KB_explainee based on dialogue history and calculates understanding score.
    '''
    updated_clauses_across_dialogue = [] # Clauses added to KB_explainee across dialogue turns
    understanding_scores = [calculate_understanding_score(KB_explainer, KB_explainee_initial)] # Initial understanding score
    KB_explainee_current = deepcopy(KB_explainee_initial) # Start with a copy to avoid modifying the original

    dialogue_turns = sorted(dialogue_history_D.keys(), reverse=True) # Process dialogue history from latest to earliest
    num_dialogue_turns = 0
    for turn in dialogue_turns:
        clauses_from_dialogue = dialogue_history_D[turn]
        if clauses_from_dialogue: # Check if there are clauses in this turn

            KB_explainee_current = revise_knowledge_base(KB_explainee_current, clauses_from_dialogue + updated_clauses_across_dialogue)

            newly_added_clauses = []
            for clause in clauses_from_dialogue:
                if clause not in updated_clauses_across_dialogue and clause not in KB_explainee_current: # Check if clause is really new
                    newly_added_clauses.append(clause)
            updated_clauses_across_dialogue.extend(newly_added_clauses) # Keep track of added clauses

            num_dialogue_turns += 1
            understanding_scores.append(calculate_understanding_score(KB_explainer, KB_explainee_current+updated_clauses_across_dialogue)) # Understanding after revision
            if skeptical_entailment(KB_explainee_current+updated_clauses_across_dialogue, [], query):
                return KB_explainee_current+updated_clauses_across_dialogue, num_dialogue_turns, understanding_scores

    return None # Return None if query is not entailed after all dialogue turns


'''
-------------------------------------------------------------------------------
Main Experiment Script
-------------------------------------------------------------------------------
'''




if __name__ == "__main__":
    # Example KB for testing prime implicate computation
    example_kb = [[4], [-4, -1], [-4, 1, 3], [5], [-5, -2]]  # Example KB in CNF

    print("Example Knowledge Base (KB):")
    print(f"KB: {example_kb}")

    print("\n--- Computing Prime Implicates using Minisat22 ---")
    prime_implicates_minisat = compute_prime_implicates(example_kb, n_models=1000)
    print(f"Prime Implicates (Minisat22): {prime_implicates_minisat}")

    print("\n--- Computing Prime Implicates using Cadiback ---")
    prime_implicates_cadiback_result = compute_prime_implicates_cadiback(example_kb)
    print(f"Prime Implicates (Cadiback): {prime_implicates_cadiback_result}")



