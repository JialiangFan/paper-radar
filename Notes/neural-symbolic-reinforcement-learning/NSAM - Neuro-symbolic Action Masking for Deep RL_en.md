# NSAM: Neuro-symbolic Action Masking for Deep RL

## Topic
Symbolic Action Masking

## Background
Deep reinforcement learning (DRL) has achieved notable success in complex domains such as autonomous driving, resource management, and algorithmic trading, yet agents frequently explore infeasible actions that violate domain constraints during training and execution. Existing neuro-symbolic RL approaches typically assume a predefined symbolic grounding function that maps high-dimensional states to symbolic representations and rely on manually specified action masking rules, which is often impractical when state spaces are high-dimensional or infinite. Automatically learning symbolic models from raw numerical states and leveraging them to filter unsafe actions therefore remains a critical open challenge.

## Limitations and Research Questions
- **Limitation 1:** Existing methods require a predefined symbolic grounding function, demanding complete prior knowledge of the environment, which is infeasible for high-dimensional or continuous state spaces.
- **Limitation 2:** Obtaining full symbolic supervision (ground-truth symbolic descriptions at every state) is unrealistic in DRL environments, as environments rarely provide such annotations.
- **Limitation 3:** Symbolic reasoning is inherently non-differentiable, conflicting with gradient-based DRL algorithms and preventing end-to-end training.
- **Problem:** How to automatically learn symbolic models under minimal supervision and seamlessly integrate them into gradient-based DRL, enabling end-to-end joint optimization of symbolic grounding and policy learning?

## Contributions
- Proposes NSAM (Neuro-symbolic Action Masking), a framework that automatically learns symbolic models from high-dimensional numerical states to construct action masks, eliminating the need for predefined symbol grounding functions.
- Introduces Probabilistic Sentential Decision Diagrams (PSDDs) as the core symbolic structure: PSDDs inherently satisfy domain constraints while supporting differentiable parameter learning, bridging the gap between symbolic reasoning and gradient-based optimization.
- Designs an end-to-end training framework (Algorithm 1) that alternately updates the gating function (symbolic grounding) and the policy network, enabling mutual reinforcement between the two components.
- Requires only minimal supervision: leverages action explorability feedback tuples (s, a, s', y) for automatic labeling, avoiding the need for full symbolic annotations at each state.
- Conducts systematic experiments on four constrained decision-making domains (Sudoku, N-Queens, Graph Coloring, Visual Sudoku), demonstrating significant improvements over baselines (Rainbow, PPO, PPO-Lagrangian, KCAC, RC-PPO, PLPG) in both sample efficiency and constraint violation rate.

## Methodology
- **Problem Formulation:** Extends the standard MDP with atomic propositions P, action preconditions AP, and a domain constraint phi, where each action's explorability is jointly determined by its precondition and the constraint.
- **Knowledge Compilation:** Compiles the domain constraint phi into a Sentential Decision Diagram (SDD), then parameterizes it as a PSDD. The SDD is a normalized Boolean circuit that guarantees non-zero probability for all constraint-satisfying models and zero probability for violating ones.
- **Learning Symbolic Grounding:** A neural gating function g maps high-dimensional states s to PSDD parameters Theta = g(s), enabling the PSDD to output a probability distribution over symbolic models conditioned on the current state: Pr(m | Theta, m |= phi). Training uses cross-entropy loss against the explorability label y.
- **Symbolic Reasoning and Action Masking:** Performs MAP inference on the PSDD to obtain the most likely symbolic model m-hat for the current state, then evaluates each action's precondition phi via C_phi(m-hat) to construct a symbolic mask. The policy network's output probabilities are multiplied by this mask and renormalized, filtering out infeasible actions.
- **End-to-End Training:** During each episode, the agent collects (s, a, s', y) feedback tuples into a buffer D; the gating function g is periodically updated via sampling from D (Eq. 3), while the policy network is simultaneously updated through masked PPO (Eq. 6). The two modules are alternately optimized, mutually reinforcing each other.
- **Key Design Advantages:** PSDD MAP inference runs in linear time (exploiting decomposability and determinism properties), making real-time action masking feasible in DRL; the 0-1 masking with renormalization preserves valid policy gradients, maintaining theoretical correctness of the optimization.
