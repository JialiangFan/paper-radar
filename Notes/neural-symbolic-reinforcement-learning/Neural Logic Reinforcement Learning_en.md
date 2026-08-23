# Neural Logic Reinforcement Learning

## Topic
Logic-Based RL Policies

## Background
Deep Reinforcement Learning (DRL) has achieved remarkable success in tasks such as game playing and robotics, yet the learned policies are encoded in opaque neural networks, lacking interpretability and exhibiting poor generalization when the test environment differs from training. Traditional symbolic methods offer interpretability and generalizability but require known system dynamics and scale poorly to complex tasks. Differentiable Inductive Logic Programming (DILP) has demonstrated the ability to combine neural differentiability with first-order logic expressiveness in supervised settings, but had not yet been applied to sequential decision-making.

## Limitations & Research Problem
- **Limitation 1:** Neural-network-based DRL policies are black boxes, precluding system verification, debugging, and compliance checking; they also generalize poorly across environments with different initial states or problem sizes.
- **Limitation 2:** Traditional relational RL methods rely on non-differentiable symbolic reasoning, making them incompatible with modern policy gradient algorithms and limiting their scalability.
- **Problem:** How can RL policies be represented in first-order logic so as to be simultaneously interpretable and generalizable, while remaining trainable end-to-end via gradient-based methods?

## Contributions
- Proposes the Neural Logic Reinforcement Learning (NLRL) framework, the first to integrate DILP into RL, representing policies as first-order logic programs compatible with standard policy gradient methods.
- Introduces the Differentiable Recurrent Logic Machine (DRLM), an improved DILP architecture that assigns trainable weights directly to individual clauses rather than clause combinations, reducing memory consumption, improving scalability, and enabling longer logic chaining.
- Formalizes the MDP with Logic Interpretation as a triple $(M, p_S, p_A)$: a state encoder $p_S$ maps raw states to sets of ground atoms, DRLM performs multi-step differentiable deduction over these atoms, and an action decoder $p_A$ converts action-atom valuations into a probability distribution over actions.
- Empirically demonstrates on Blocks World (STACK, UNSTACK, ON) and Cliff-Walking tasks that NLRL learns near-optimal policies that are human-readable as logic rules and generalize to unseen initial states and larger problem sizes, whereas MLP baselines fail to generalize.

## Methodology
- **DRLM Architecture:** Operates on valuation vectors $e \in [0,1]^{|G|}$ representing confidence in ground atoms. Multi-step deduction is defined recursively as $f_\theta^t(e_0)$; each step aggregates all weighted clause deductions via the probabilistic sum ($a \oplus b = a + b - a \odot b$). Weights are softmax-normalized per predicate and assigned to individual clauses, yielding lower memory cost and support for longer deduction chains compared to the original dILP.
- **MDP with Logic Interpretation:** Defined as $(M, p_S, p_A)$. $p_S$ encodes the raw state into a valuation vector over ground atoms. DRLM performs $t$ steps of differentiable deduction to produce valuations for action atoms. $p_A$ maps these valuations to action probabilities: if the total action valuation $\sigma \geq 1$, each action's probability is proportional to its valuation; if $\sigma < 1$, the residual probability $1 - \sigma$ is distributed uniformly across all actions, promoting exploration and generalization.
- **Training:** Vanilla policy gradient (REINFORCE) with generalized advantage estimation (GAE, $\lambda = 0.95$) and RMSProp optimizer ($lr = 0.001$). The value baseline is a neural network with one 20-unit hidden layer.
- **Rule Templates:** A small, task-agnostic set of rule templates specifying clause arity ($\in \{0, 1, 2\}$), number of existential variables ($\in \{0, 1, 2\}$), and whether invented predicates may appear in clause bodies. The agent autonomously learns auxiliary invented predicates during training, requiring no hand-crafted domain-specific predicates.
- **Experimental Design:** Evaluated on three Blocks World subtasks (STACK, UNSTACK, ON) and Cliff-Walking (including a stochastic windy variant). Generalization is tested by varying initial states, increasing the number of blocks, and enlarging the grid size. Baselines include an MLP agent and a random agent. NLRL achieves near-optimal returns in training environments and maintains strong performance across all generalization tests, while MLP agents fail catastrophically outside their training distribution.
