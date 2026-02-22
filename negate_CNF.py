from itertools import product


def dnf_to_cnf(dnf_formula):
    cnf_formula = []

    for term_combination in product(*dnf_formula):
        new_clause = []
        for term in term_combination:
            if term not in new_clause and -term not in new_clause:
                new_clause.append(term)
        new_clause.sort(key=lambda x: abs(x))
        if not any(all(lit in existing_clause for lit in new_clause) for existing_clause in cnf_formula):
            cnf_formula.append(new_clause)

    return cnf_formula



def negate_cnf(cnf_formula):
    negated_dnf = []

    for clause in cnf_formula:
        negated_clause = [-literal for literal in clause]
        negated_dnf.append(negated_clause)

    return dnf_to_cnf(negated_dnf)






# if __name__ == "__main__":
#     cnf_formula = [[-1, 2], [3]]   
#     print("CNF formula:", cnf_formula)
#     negated_cnf_formula = negate_cnf(cnf_formula)
#     print("Negated CNF formula:", negated_cnf_formula)



