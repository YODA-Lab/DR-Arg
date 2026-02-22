import copy

from unified_planning.model.types import *
from unified_planning.shortcuts import *
from unified_planning.io.pddl_reader import PDDLReader
from unified_planning.engines import CompilationKind

from planning_utils.CNF_Encoder import Encoder
from planning_utils.CNF_Encoder_KBh import Encoder_KBh
up.shortcuts.get_env().credits_stream = None
from DE import *







reader = PDDLReader()
pddl_agent = reader.parse_problem('./blocks/original_domain.pddl', './blocks/prob1.pddl')
pddl_human = reader.parse_problem('./blocks/human.pddl', './blocks/prob1.pddl')


with OneshotPlanner(name="tamer") as planner:
    result = planner.solve(pddl_agent)
    plan = result.plan





def get_ground_fluent(ground_problem):
    ground_fluents = set()
    for f in ground_problem._fluents:
        # print(f)
        if f.arity == 0:
            f_exp = ground_problem._env.expression_manager.FluentExp(f)
            ground_fluents.add(f_exp)
        #     res[f_exp] = self.initial_value(f_exp)
        else:
            ground_size = 1
            domain_sizes = []
            for p in f.signature:
                ds = domain_size(ground_problem, p.type)
                domain_sizes.append(ds)
                ground_size *= ds
            for i in range(ground_size):
                f_exp = ground_problem._get_ith_fluent_exp(f, domain_sizes, i)
                ground_fluents.add(f_exp)
    return ground_fluents




with Compiler(compilation_kind=CompilationKind.GROUNDING) as grounder:
    grounding_result_agent = grounder.compile(pddl_agent, CompilationKind.GROUNDING)
    grounding_result_human = grounder.compile(pddl_human, CompilationKind.GROUNDING)
    ground_problem_agent = grounding_result_agent.problem
    ground_problem_human = grounding_result_human.problem



fluents = [f.name for f in ground_problem_agent.fluents]
inits = list(ground_problem_agent._initial_value.keys())
goals = ground_problem_agent._goals


horizon = len(plan.actions)

KBa, kba_vars = Encoder(ground_problem_agent, horizon).encode()
KBh, kbh_vars = Encoder_KBh(ground_problem_human, horizon, kba_vars).encode()



q = CNF(from_clauses=[[-kba_vars["on_B_A_0"]], [-kba_vars["on_B_A_1"]]])

# print(q.clauses)


wcnf = WCNF()
for c in KBh.all_formulae():
    if c == [12]:
        wcnf.append(c)
    else:
        wcnf.append(c, weight=1)

lbx = LBX(wcnf, use_cld=True, solver_name='g3')

mcs = lbx.compute()
e = [wcnf.soft[m-1] for m in mcs]


kbh = []
for f in KBh.all_formulae():
    if f != e[0]:
        kbh.append(f)


ea = explanation(KBa.all_formulae(), q)

print(ea)


print(map_id_to_vars(KBa, ea))

print(map_id_to_vars(KBa, q.clauses))

# TODO templates for NL


# T = nx.DiGraph() # argumentation tree
# T.add_node(str(ea)+'_agent')
# T.nodes[str(ea)+'_agent']['support'] = ea



# T = arg_sim(KBa.all_formulae(), kbh, ea, 1)
#
# for n in T.nodes:
#     print('parent:',n, 'child:', list(T.successors(n)))
#
#
#
# pos = graphviz_layout(T, prog="dot")
# nx.draw(T, pos, with_labels=True)
# plt.show()
