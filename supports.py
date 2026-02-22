
from pysat.examples.musx import MUSX
from utils import *
from algorithms import *
from pysat.solvers import Solver
from forgetting import *
from heapq import *
from pysat.examples.optux import OptUx




def get_supports(KB1, KB2, q):
	KB = [list(x) for x in set(map(tuple, KB1)).union(set(map(tuple, KB2)))]

	R = Hitman(solver='m22', htype='maxsat') # Reconciliation formula
	s = []
	S = []

	# Restore consistency if KB_h \cup (KB_a \KB_h) is unsat:
	if not sat(KB, []):
		to_delete = correct_KB(KB1, KB2)
		KB = [k for k in KB if k not in to_delete]

	clauses_lookup = create_clauses_lookup(KB) # create lookup dictionary initialized with KBa_s

	while True:
		C = get_MCS(KB, [], q, s, clauses_lookup)
		# print(C)
		R.hit(list(C))
		seed = R.get()
		s = get_clauses_from_index(seed, clauses_lookup)
		# print(s)
		if skeptical_entailment([], s, q):
			# print(s)
			S.append(s)
			R.block(seed)
			s = []
		elif len(s) == 0:
			return S



# objective function: O(s) = w_l*1/|s| + w_v*|V_s.intersect(V_h)|
def initial_explanation_generation(KB1, KB2, q, V):
	KB = [list(x) for x in set(map(tuple, KB1)).union(set(map(tuple, KB2)))]

	R = Hitman(solver='m22', htype='maxsat')  # Reconciliation formula
	s = []
	S = []
	vars_q = get_vars(q.clauses)

	# Restore consistency if KB_h \cup KB_a is unsat:
	if not sat(KB, []):
		to_delete = correct_KB(KB1, KB2)
		KB = [k for k in KB if k not in to_delete]

	wcnf = WCNF()
	wcnf.extend(KB, weights=[1 for i in range(len(KB))])
	wcnf.extend(q.negate())
	M = LBX(wcnf, use_cld=True, solver_name='g3')
	clauses_lookup = create_clauses_lookup(KB)

	while True:
			mcs = M.compute()
			if not mcs is None:
				M.block(mcs)
				R.hit(list(mcs))
				seed = R.get()

				s = get_clauses_from_index(seed, clauses_lookup)
				if skeptical_entailment([], s, q):
					vars_s_without_q = get_vars(s).difference(vars_q)
					heappush(S, (-(1/len(s)+len(vars_s_without_q.intersection(V))), s))
					s = []
					R.block(seed)
				# else:
				# 	for c in s:
				# 		M.add_clause(c)

			else:
				s = S[0][1]
				key = abs(S[0][0]) - 1 / len(s)
				if key == 0:
					return s, S
				else:
					vars_s_without_q = get_vars(s).difference(vars_q)
					forgets_vars = vars_s_without_q.difference(V)
					return knowledge_forget(s, forgets_vars), S






def getMUS(KB):
	with OptUx(KB) as optux:
		mus = optux.compute()
		# print('mus {0} has cost {1}'.format(mus, optux.cost))
		return [list(KB.soft[m - 1]) for m in mus]







def abstracted_explanation_generation(KB, q, V):
	# KB = [list(x) for x in set(map(tuple, KB1)).union(set(map(tuple, KB2)))]
	# # Restore consistency if KB_h \cup KB_a is unsat:
	# if not sat(KB, []):
	# 	to_delete = correct_KB(KB1, KB2)
	# 	KB = [k for k in KB if k not in to_delete]

	weights = []
	for k in KB:
		w = get_vars([k]).intersection(V)
		weights.append(-(len(w) + 1))

	wcnf = WCNF()
	wcnf.extend(KB, weights=weights)
	wcnf.extend(q.negate())

	while True:
		
		support = getMUS(wcnf)
		# print(support)
		if skeptical_entailment(support, [], q):
			# print(sat(support, []), 'here')
			# print(support)
			vars= get_vars(support)
			key = len(vars.intersection(V))
			if key == 0 or (len(support) <=2):
				return support
			else:
				forgets_vars = vars.difference(V)
				# print(forgets_vars, 'heree')
				return knowledge_forget(support, forgets_vars)



# KB1 = [[1],[-1,2],[3],[-2,-3,4], [6], [-6,2]]
# KB2 = [[7], [-7,8], [-5,-8,9], [-9,4], [-7,-8,-9,10], [-1], [5], [-5,2], [1], [-5,4]]
# q = CNF()
# q.extend([[4]])

# V = set()
# V.add(2)
# V.add(3)
# V.add(4)
# V.add(8)
# V.add(9)
# V.add(7)
# V.add(5)


# KB1 = [[1],[2],[4],[-4,2], [-1,-2,3],[-1,-2,3]]
# q = CNF()
# q.extend([[3]])

# V = set()
# V.add(1)
# V.add(2)
# V.add(4)
# V.add(3)

# e = abstracted_explanation_generation(KB1, q, V)
# print(e)
# print(skeptical_entailment(e, [], q))