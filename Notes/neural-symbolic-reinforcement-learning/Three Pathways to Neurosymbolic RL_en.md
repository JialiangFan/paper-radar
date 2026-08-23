# Three Pathways to Neurosymbolic RL

> Graf & Emami, 2024 | Neurosymbolic Artificial Intelligence, IOS Press | NREL

## Topic

Interpretable Neurosymbolic Reinforcement Learning

## Background

Purely data-driven deep RL policies lack interpretability and reliability, limiting their deployment in safety-critical domains. Neurosymbolic AI (NSAI) seeks to integrate the explicit reasoning of symbolic methods with the learnability of neural networks, yet how to systematically embed such integration within RL remains an open challenge. Building energy management (BEM), which naturally relies on rule-based control strategies (e.g., "if temperature > 20C, turn on AC"), serves as an ideal testbed for neurosymbolic RL.

## Limitations and Research Questions

- **Limitation 1:** Standard deep RL policies are black boxes, offering no human-interpretable decision rationale -- a critical barrier in domains such as BEM where trust and verifiability are required.
- **Limitation 2:** Classical symbolic logic is discrete and non-differentiable, preventing direct integration with gradient-based learning frameworks.
- **Limitation 3:** Prior neurosymbolic RL work has largely been confined to toy problems, lacking systematic exploration in realistic control settings.
- **Problem:** How to design policy and model architectures that are simultaneously differentiable (learnable) and interpretable (symbolically meaningful), and how to integrate them into different RL paradigms?

## Contributions

- Proposes three pathways for incorporating differentiable interpretable models into RL: **model-free RL** (DDT as policy), **model-based RL** (LNN-learned symbolic world model + classical planning), and **differentiable predictive control** (LNN policy + differentiable simulation, end-to-end optimization).
- Integrates two neurosymbolic architectures -- **Differentiable Decision Trees (DDTs)** and **Logical Neural Networks (LNNs)** -- into standard RL frameworks and evaluates them on building energy management tasks using the OCHRE/ochre_gym simulation environment.
- Systematically exposes the fundamental tension between differentiability and interpretability: smoother (more learnable) relaxations move further from crisp, interpretable symbolic rules.
- Identifies key open questions concerning scalability, discrete-to-continuous relaxation, warm-start reliability, and the potential role of LLMs in neurosymbolic pipelines.

## Methodology

### Core Architectures

- **Differentiable Decision Tree (DDT):** Replaces hard splits in standard decision trees with sigmoid-based soft splits. Each decision node compares a linear combination of all attributes against a learned threshold via a sigmoid. Leaf nodes output action probabilities. All parameters (weights, thresholds, sigmoid sharpness, leaf probabilities) are learnable via SGD. Continuous actions are produced through "soft actions" -- weighted combinations of discrete action values.
- **Logical Neural Network (LNN):** Implements real-valued logic, where AND/OR connectives are differentiable gates with constrained weights (y = f(w * x - theta)). Weight constraints enforce logical semantics. LNNs learn logical rules from data, automatically zeroing out weights of irrelevant predicates.

### Three Pathways

1. **Pathway 1 -- Model-Free RL with DDT Policy:**
   - Integrates DDT as the actor network within SAC (Soft Actor-Critic) in the stablebaselines3 framework.
   - Evaluated on HVAC control under time-of-use (TOU) pricing in ochre_gym.
   - Supports "warm start" initialization from a known rule-based controller (RBC).
   - **Results:** RBC outperforms DDT and standard DRL overall. Warm-start DDT achieves near-RBC performance on the training month but is unreliable across settings. The cascade of sigmoids in DDTs creates numerical difficulties for stochastic gradient descent. DDT policies demonstrate adaptivity in months where RBC underperforms.

2. **Pathway 2 -- Model-Based RL with LNN World Model and Classical Planning:**
   - Learns action pre- and post-conditions (STRIPS-style symbolic world model) from simulation data using LNNs.
   - Defines a vocabulary mapping continuous simulation states to logical predicates.
   - Converts the learned LNN model into a PDDL planning problem, solved by an off-the-shelf classical planner.
   - **Results:** LNN weights converge to integer values (0 or 1), yielding fully interpretable logical rules. Successfully discovers control rules (e.g., "if cold, pull switch to make it not cold").

3. **Pathway 3 -- Differentiable Predictive Control with LNN Policy:**
   - Implements a differentiable temperature regulation simulation in PyTorch with an LNN-based policy.
   - Unrolls the full episode as a computational graph; LNN parameters are optimized end-to-end via backpropagation (dL/d_theta).
   - Employs smoothness parameter scheduling: begins with smooth sigmoids for stable gradient descent, progressively sharpens toward crisp logical decisions.
   - **Results:** LNN learns interpretable rules (e.g., "if Hot then TurnACOn"; "if Hot AND PowerCheap then TurnACOn"), with spurious predicate weights driven to zero.

### Key Findings and Trade-offs

- **Differentiability vs. Interpretability:** Smoother sigmoids facilitate learning but diverge from discrete, interpretable rules. DDT relaxations are "uncontrolled" (unlike integer programming relaxations with theoretical guarantees), making discretization unreliable.
- **LNN superiority in interpretability:** LNN weights nearly always converge to 0/1 integers, naturally producing interpretable logical expressions. DDT real-valued weights resist clean discretization.
- **Scalability challenges:** DDTs struggle with stochastic gradient descent in dynamic environments. DPC requires a fully differentiable simulator (rare in practice). The model-based pathway faces combinatorial explosion in the number of possible rules.
