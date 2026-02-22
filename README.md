# Dialectical Reconciliation via Structured Argumentative Dialogues

Code accompanying the KR 2024 paper:

> **Dialectical Reconciliation via Structured Argumentative Dialogues**
> Proceedings of the 21st International Conference on Principles of Knowledge Representation and Reasoning (KR 2024)

## Overview

This repository implements the **DR-AI** (Dialectical Reconciliation via Argumentation-based Interaction) algorithm. DR-AI enables an explainer agent to reconcile differences with an explainee (human) through structured argumentative dialogues. Rather than providing a one-shot explanation, the agents engage in a multi-turn dialogue where:

1. The **Agent** provides an initial explanation (a minimal subset of its knowledge base that entails a query)
2. The **Human** attacks parts of the explanation using counter-arguments from its own knowledge base
3. The agents alternate arguments until reconciliation is reached or no further arguments can be made

Knowledge bases are represented in propositional CNF (conjunctive normal form), and arguments are computed using SAT-based reasoning (MUS/MCS extraction via PySAT).

## Repository Structure

```
.
├── DE.py                    # Main dialectical explanation module (Agent, Human, dialogue)
├── algorithms.py            # Core SAT-based algorithms (entailment, MUS, MCS, explanation)
├── supports.py              # Support/explanation generation with variable abstraction
├── forgetting.py            # Knowledge forgetting via resolution
├── utils.py                 # Planning KB utilities and CNF-to-variable mapping
├── experiments.py           # Benchmark experiment runner
├── random_KBs_generator.py  # Random CNF knowledge base generator
├── negate_CNF.py            # CNF negation via DNF-to-CNF conversion
├── plots.py                 # Plotting scripts for benchmark results
├── new_plots.py             # Additional plotting scripts
├── main.py                  # Planning domain example (blocks world)
├── planning_utils/          # CNF encoders for PDDL planning domains
│   ├── CNF_Encoder.py
│   ├── CNF_Encoder_KBh.py
│   ├── util.py
│   └── modifier.py
├── blocks/                  # PDDL files for blocks world example
│   ├── original_domain.pddl
│   ├── human.pddl
│   └── prob1.pddl
├── benchmarks/              # Benchmark results (KB sizes: 100, 1K, 10K, 50K)
├── requirements.txt
└── .gitignore
```

## Installation

### Prerequisites

- Python >= 3.9

### Install dependencies

```bash
pip install -r requirements.txt
```

### Cadiback (optional, for prime implicates)

The `experiments.py` module can optionally use [Cadiback](https://github.com/arminbiere/cadiback) for computing prime implicates. To use it, clone and build Cadiback, then place the `cadiback` binary in your working directory. If unavailable, the code falls back to Minisat22-based enumeration.

## Usage

### Basic Dialogue Example

```python
from DE import Agent, Human, dialogue
from pysat.formula import CNF

# Define knowledge bases in CNF
KBa = [[1], [2], [-1, -2, 3], [-4]]
KBh = [[4], [-4, -1], [-4, 1, 3], [5], [-5, -2]]

# Define query
q = CNF()
q.append([3])

# Create agents and run dialogue
agent = Agent(KBa, "Agent")
human = Human(KBh, "Human")

D, num_turns = dialogue(agent, human, q, verbose=True)
```

### Computing Explanations

```python
from algorithms import explanation
from pysat.formula import CNF

KB = [[1], [2], [-1, -2, 3]]
q = CNF()
q.append([3])

e = explanation(KB, q)
print("Explanation:", e)  # Minimal subset of KB that entails q
```

### Planning Domain (Blocks World)

The `main.py` script demonstrates dialectical reconciliation in a planning context using PDDL domains. It encodes agent and human planning models as CNF knowledge bases, then runs the argumentation framework. Requires the `unified-planning` package.

## Benchmarks

The `benchmarks/` directory contains experimental results for knowledge bases of varying sizes (100, 1,000, 10,000, and 50,000 clauses). Each experiment includes:
- `KBa.cnf` / `KBh.cnf` — Agent and Human knowledge bases in DIMACS format
- `q.cnf` — Query in DIMACS format
- `results.txt` — Dialogue statistics (turns, time, understanding scores)

## Citation

```bibtex
@inproceedings{vasileiou2024dialectical,
  title={Dialectical Reconciliation via Structured Argumentative Dialogues},
  author={Vasileiou, Stylianos Loukas and Yeoh, William and Tran, Son and Sreedharan, Sarath},
  booktitle={Proceedings of the 21st International Conference on Principles of Knowledge Representation and Reasoning (KR)},
  year={2024}
}
```
