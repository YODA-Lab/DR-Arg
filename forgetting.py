import copy
import itertools
import math
import random
from pysat.formula import IDPool, CNF
from algorithms import skeptical_entailment
import networkx as nx
import matplotlib.pyplot as plt


def Res(KB, v):
	phi_1 = []
	phi_2 = []
	KB_excluded = []

	for c in KB:
		if not any(i in c or -i in c for i in v):
			KB_excluded.append(c)
			# Phi.append(c)
			# if len(c) == 1: # remove unit clauses
			#     continue
		for i in v:
			if i in c:
				# c.remove(i) # remove positive var in c and add in phi_1
				phi_1.append(c)
			elif -i in c:
				# c.remove(-i) # remove negative var in c and add in phi_2
				phi_2.append(c)

	# Combine phi_1 and phi_2
	resolvents = []
	if phi_1 and phi_2:
		for c1 in phi_1:
			clause1 = copy.deepcopy(c1)
			clause1.remove(v[0])
			for c2 in phi_2:
				clause2 = copy.deepcopy(c2)
				clause2.remove(-v[0])
				if any(-var in clause2 for var in clause1):
					continue
				else:
					r = list(set(clause1 + clause2))
					resolvents.append(r)

	# elif phi_1 and not phi_2:
	#         for c1 in phi_1:
	#             clause1 = copy.deepcopy(c1)
	#             clause1.remove(v[0])
	#             resolvents.append(clause1)
	# elif not phi_1 and phi_2:
	#      for c2 in phi_2:
	#             clause2 = copy.deepcopy(c2)
	#             clause2.remove(v[0])
	#             resolvents.append(clause2)

	# print(resolvents, 'here')
	return resolvents + KB_excluded


def Res_recursive(KB, V):
	if len(V) == 0:
		return KB
	else:
		v = V.pop()
		KB = Res(KB, [v])
		KB_forget = Res_recursive(KB, V)
		return KB_forget


def knowledge_forget(KB, V):
	V_temp = copy.deepcopy(V)
	# Get formulae that do not mention v
	KB_exclude = []
	for c in KB:
		if not any(i in c or -i in c for i in V_temp):
			KB_exclude.append(c)

	KB_to_resolve = [c for c in KB if c not in KB_exclude]
	# print(KB_to_resolve, 'H')
	KB_res = Res_recursive(KB_to_resolve, V_temp)
	return KB_res + KB_exclude


def get_vars(KB):
	vars = set([abs(item) for sublist in KB for item in sublist])
	return vars

