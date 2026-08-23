# SDRL: Interpretable Deep RL with Symbolic Planning

> Lyu, Yang, Liu, Gustafson (2019). AAAI.

## Topic
Symbolic Planning + Hierarchical RL + Interpretability

## Background
Deep reinforcement learning has achieved remarkable success on sequential decision-making from high-dimensional sensory inputs, yet remains criticized for poor interpretability and low data efficiency. Neuroscience evidence suggests humans play video games by constructing object-based deterministic transition models and planning hierarchically, motivating the integration of symbolic planning into DRL. Prior SP+RL integration work (e.g., PEORL) was limited to tabular representations and could not scale to complex domains with pixel-level inputs.

## Limitations & Research Questions
- **Limitation 1:** Standard DRL methods (e.g., DQN) are black-box models whose learned policies are opaque to humans and require millions of samples, especially under sparse rewards and long horizons.
- **Limitation 2:** Existing hierarchical RL approaches (e.g., hDQN, options framework) introduce temporal abstraction but lack interpretability in subtask/option definitions and typically require predefined option sets.
- **Limitation 3:** Previous SP+RL frameworks (e.g., PEORL) rely on tabular state representations and fixed planning goals, preventing them from handling high-dimensional inputs or dynamically adapting plans based on learning feedback.
- **Problem:** How to design a framework that leverages symbolic knowledge for interpretable high-level planning while using DRL to learn low-level control policies from raw pixels, with both components cross-fertilizing to converge to optimality?

## Contributions
- Proposes the SDRL framework, the first to integrate symbolic planning with hierarchical DRL for task-level interpretability over high-dimensional sensory inputs.
- Introduces a **planner--controller--meta-controller** architecture: the planner uses action language BC with the CLINGO answer set solver to generate symbolic plans (subtask sequences); the controller employs DRL to learn sub-policies for each subtask; the meta-controller applies R-learning to evaluate subtask extrinsic rewards and propose new intrinsic goals to the planner.
- Introduces an **intrinsic goal** mechanism (replacing PEORL's fixed goal) that uses plan quality -- the cumulative gain reward of a symbolic plan -- to dynamically update the planning objective based on actual controller performance.
- Maps symbolic transitions to semi-Markov options via a perception module (symbol grounding function F) that bridges symbolic states and high-dimensional sensory states.
- Provides theoretical guarantees: the algorithm terminates if and only if an optimal symbolic plan exists (Theorem 1), and the returned plan is optimal upon convergence (Theorem 2).
- Validates interpretability and data efficiency on the Taxi domain and Montezuma's Revenge.

## Methodology
- **Symbolic Representation:** Domain knowledge is encoded in action language BC, comprising objects, fluents, and causal laws. The action description D is augmented with gain reward fluents $\rho(s,a)$ and a plan quality fluent to quantify plan utility. CLINGO solves the resulting planning problem.
- **Intrinsic Goal:** Defined as a linear constraint $quality > quality(\Pi)$, driving the planner to find strictly better plans each iteration rather than pursuing a fixed designer-specified goal.
- **Symbol Grounding:** A pre-trained perception module $\mathbb{F}: S \times \tilde{S} \to \{t, f\}$ maps high-dimensional sensory states to symbolic states. Each symbolic transition is thereby converted into a semi-Markov option with an initiation set, intra-option policy, and termination condition.
- **Controller (DRL):** Each subtask is learned via Deep Q-learning with intrinsic reward $r_i$: a large bonus $\phi$ upon achieving the subtask goal, and the raw environment reward otherwise.
- **Meta-Controller (R-learning):** Performs R-learning over extrinsic rewards to estimate the long-term average reward of selecting each subtask. The extrinsic reward $r_e(s,g) = f(\epsilon)$ equals the true environmental reward when the sub-policy success ratio $\epsilon \geq 0.9$, and a large penalty $-\psi$ otherwise, to prune unlearnable subtasks.
- **Planning-Learning Loop (Algorithm 1):** In each episode, the planner generates plan $\Pi_t$; the controller trains sub-policies for each subtask; the meta-controller computes extrinsic rewards and updates $R(s,g)$ and $\rho$ values; the intrinsic goal is updated and learned $\rho$ values are fed back into the symbolic formulation to trigger replanning. The three components cross-optimize until the symbolic plan can no longer be improved.
- **Experiments:** On the Taxi domain (5x5 grid, tabular), SDRL is compared against standard PEORL and SR-learner, demonstrating superior policy adaptability via intrinsic goals when reward structures shift. On Montezuma's Revenge (Atari, pixel input), SDRL is compared against hDQN, achieving a cumulative reward of ~400 at 1.5M samples with human-readable subtask decomposition, versus hDQN's ~400 at 2.5M samples with higher variance and less interpretable subtask definitions.
