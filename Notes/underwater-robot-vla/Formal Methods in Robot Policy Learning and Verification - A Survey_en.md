# Formal Methods in Robot Policy Learning and Verification: A Survey on Current Techniques and Future Directions

## Topic
Comprehensive survey of formal methods (STL, LTL, CTL, CBFs, CLFs, automata) applied to robot policy learning and post-hoc verification, with a unified taxonomy based on scalability-expressiveness tradeoffs.

## Background
The adoption of deep learning in robotics has produced powerful but opaque neural network policies that lack flexibility, robustness, and interpretability guarantees. Formal methods (FM) offer a principled framework for specifying, guiding, and verifying desired behaviors in robot systems. However, the landscape of FM applications in robotics is fragmented across specification languages, learning paradigms, and verification techniques, making it difficult for practitioners to navigate the available tools and their tradeoffs. This survey, published in TMLR 2026, provides the first systematic organization of this space spanning 19 pages and 6 figures.

## Limitations & Research Problem
- **Limitation:** Neural network policies trained via deep RL or imitation learning are opaque -- they offer no formal guarantees about safety, stability, or task completion, which is unacceptable for safety-critical robot deployments.
- **Limitation:** Existing formal methods research in robotics is scattered across communities (control theory, formal verification, machine learning) with no unified framework for comparing approaches.
- **Limitation:** The scalability-expressiveness tradeoff is poorly understood -- practitioners lack guidance on which FM approach suits their specific needs.
- **Problem:** How to systematically organize and compare the landscape of formal methods for robot policy learning and verification, identify fundamental tradeoffs, and chart future research directions including integration with foundation models?

## Contributions
- First comprehensive survey unifying formal methods across both robot policy learning and verification
- Systematic taxonomy of specification languages (LTL, STL, automata, CBF/CLF) with clear comparison of their expressiveness and computational properties
- Classification of FM-informed learning into online (model-free RL, model-based RL) and offline (inverse RL, behavior cloning, offline RL) paradigms
- Verification taxonomy organized by supported specification complexity: general omega-regular (discrete abstraction), reach-avoid (set propagation, sensitivity analysis, HJ reachability), and safety/guarantee (certificate functions)
- Identification of the fundamental expressiveness-scalability-approximation error tradeoff across verification methods
- Critical analysis of open problems including specification mining, offline learning integration, foundation model verification, and relaxed guarantees

## Methodology

### Specification Languages
- **LTL (Linear Temporal Logic)**: Boolean + temporal operators (next, eventually, always, until). Best for discrete, long-horizon tasks. Supports automaton construction for product MDP formulations.
- **STL (Signal Temporal Logic)**: Extends LTL to continuous-time real-valued signals. Provides quantitative robustness semantics (how much a specification is satisfied/violated). Ideal for continuous dynamical systems. Used directly as differentiable reward/loss signals.
- **Automata Representations**: FSA, Buchi automata, Rabin automata, Limit-Deterministic Buchi Automata (LDBA), and Reward Machines. Enable decomposition of complex temporal tasks into composable sub-policies.
- **Certificate Functions**: Control Barrier Functions (CBFs) for forward invariance, Control Lyapunov Functions (CLFs) for stability, Contraction Metrics for convergence. Computationally efficient but limited to simpler property classes.

### Policy Learning Methods
- **Automata-Theoretic RL**: Constructs product MDPs combining environment and automaton state spaces. Uses Good-for-MDPs automata to handle restricted non-determinism. Supports full omega-regular specifications.
- **Automata-Guided RL**: Decomposes specifications into edge-specific sub-policies composed at execution time. Enables modular learning for complex multi-step tasks.
- **Automata-Free RL**: Directly uses STL/LTL quantitative robustness as shaped reward signals. Avoids combinatorial cost of automaton construction. Most relevant to continuous-domain robotics.
- **Programmatic RL**: Learns interpretable program-like policies via Counter-Example Guided Inductive Synthesis (CEGIS), tree-search, or end-to-end differentiable programs.
- **STL-Guided Offline Methods**: STL-derived loss functions for behavior cloning, STL-guided diffusion policies, and specification-conditioned sequence modeling. Identified as underdeveloped with high potential.

### Verification Methods
- **Discrete Abstraction**: SMC-based methods with discrete environment models. Highest expressiveness (general omega-regular specs) but exponential complexity.
- **Set Propagation**: Over-approximates reachable state sets using polytopes, zonotopes, star sets, or Taylor models. Tools: Verisig, ReachNN, CORA, NNV. Moderate scalability, suffers from wrapping effect in high dimensions.
- **Hamilton-Jacobi Reachability**: Formulates verification as two-player differential games. Neural approximations (DeepReach) and physics-informed approaches improve scalability but introduce training-time safety risks.
- **Certificate Functions (CBF/CLF/Neural Variants)**: Best scalability, model-free with sample access, but restricted to safety/stability properties. Cannot express complex temporal behaviors.
- **Runtime Monitoring**: STL monitors, automata-based monitors, anomaly detection, safety shields. Practical for deployment but reactive rather than proactive.
- **Falsification**: Counterexample search. Weaker guarantees than verification but computationally more tractable.

### Expressiveness-Scalability Tradeoff (Key Finding)
| Method | Spec Complexity | Scalability | Approx. Error |
|--------|----------------|-------------|---------------|
| Discrete Abstraction | General omega-regular | Exponential blowup | Low |
| Set Propagation | Reach-avoid | Moderate | Moderate (wrapping) |
| Sensitivity Analysis | Reach-avoid | Moderate | Moderate |
| HJ Reachability (Neural) | Reach-avoid | High (scalable) | Variable |
| Certificate Functions | Safety/Guarantee only | High | Moderate |

### Experimental Setup
- The survey covers applications across discrete domains (grid navigation, task planning), continuous domains (quadrotor control, autonomous driving, manipulation), and real-world deployments (Unitree Go2 quadruped, PR-2 manipulation, multi-agent coordination). No new experiments are conducted; the contribution is the systematic organization and analysis of existing work.

## Future Directions
- **Specification Mining**: Learning formal specifications from demonstrations or natural language to bridge the intent-specification gap
- **Offline Learning + FM**: Combining formal constraints with offline RL and imitation learning remains largely unexplored
- **Foundation Model Verification**: Verifying large VLA models and vision-based policies is identified as a critical open challenge
- **Relaxed Guarantees**: Trading exact guarantees for probabilistic or bounded-horizon verification to improve scalability
- **Partial Observability**: Extending FM approaches to handle realistic sensor limitations and partial state information
